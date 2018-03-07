node {
    // stage('Clean Up') {
    //     deleteDir()
    // }

    stage('Checkout') {

        // Load Node.js
        def nodeHome = tool 'NodeTool'
        env.PATH="${env.PATH}:${nodeHome}/bin"

        // Checkout Git Source Code
        def scmVars = checkout scm

        // Run job based on current branch
        if (scmVars.GIT_COMMIT == scmVars.GIT_PREVIOUS_SUCCESSFUL_COMMIT) {
            println "Nothing new to commit || Neither the master or staging branch"
        } else {
            if (scmVars.GIT_BRANCH == 'origin/staging') {
                println "Staging Branch"

                sh 'cp /aws/adpq/server/local/config.json ./src/server/src/config.json' // Setup Local Config for Tests
                runStagingTests()

                sh 'cp /aws/adpq/server/staging/config.json ./src/server/src/config.json' // Setup Staging Config for Deployment
                build()
                publish()
                deployStaging()
                sendSlackNotification()
            } else if (scmVars.GIT_BRANCH == 'origin/master') {
                println "Master Branch"
                // sh 'cp /aws/adpq/server/production/config.json ./src/server/src/config.json'
                // println "Copied Production Config.json"
                // build()
                // publish()
                // deployProduction()
            }
        }
    }

    // stage ('Clean Up') { // Clean Up Workspace
    //     // deleteDir()
    // }
}

def build() {
    stage('Build') { // Build Docker Images
        sh 'docker build -t adpq-server ./src/server'
    }
}

def publish() {
    stage ('Publish') { // Publish images to ECR Registry
        sh '''#!/bin/bash
            $(aws ecr get-login --no-include-email --region us-west-1)

            docker tag adpq-server 485490441211.dkr.ecr.us-west-1.amazonaws.com/adpq-server:latest
            docker push 485490441211.dkr.ecr.us-west-1.amazonaws.com/adpq-server:latest

            docker tag adpq-server 485490441211.dkr.ecr.us-west-1.amazonaws.com/adpq-server:v_${BUILD_NUMBER}
            docker push 485490441211.dkr.ecr.us-west-1.amazonaws.com/adpq-server:v_${BUILD_NUMBER}
        '''
    }
}

def runStagingTests() {
    stage('Test') {
        sh '''#!/bin/bash
            # Wait 10 seconds
            sleep 10 &&

            # Clean Up
            rm -rf /var/lib/jenkins/adpq_test_results &&
            mkdir /var/lib/jenkins/adpq_test_results &&

            # Build and run api & db
            /usr/local/bin/docker-compose up --build -d &&

            # Build & run container
            docker build ./src/qa -t adpq_tests &&
            docker run --network='host' -v /var/lib/jenkins/adpq_test_results/reports:/data/reports -e Environment=local --name adpq_tests -i adpq_tests >> /var/lib/jenkins/adpq_test_results/results.xml &&
            docker rm adpq_tests && docker rmi adpq_tests &&

            # Extract test results and save to var RESULTS
            numberOfTests=$(cat /var/lib/jenkins/adpq_test_results/results.xml | cut -d '=' -f 2 | cut -d ' ' -f 1) &&
            errors=$(cat /var/lib/jenkins/adpq_test_results/results.xml | cut -d '=' -f 3 | cut -d ' ' -f 1) &&
            failures=$(cat /var/lib/jenkins/adpq_test_results/results.xml | cut -d '=' -f 4 | cut -d '>' -f 1) &&
            numberOfSuccesses=$(($numberOfTests - $errors - $failures)) &&
            echo "$numberOfSuccesses / $numberOfTests tests ran successfully" > RESULTS &&

            # Create Shield.io badge url & set Slack result type
            testBadge=""
            if [ "$numberOfSuccesses" -lt "$numberOfTests" ]; then
                echo "FAILURE" > RESULT_TYPE
                testBadge=https://img.shields.io/badge/tests-$numberOfSuccesses%2F$numberOfTests-red.svg
            else
                echo "SUCCESS" > RESULT_TYPE
                testBadge=https://img.shields.io/badge/tests-$numberOfSuccesses%2F$numberOfTests-brightgreen.svg
            fi

            # Upload Image Badge to S3
            curl $testBadge >> ./testResultsImg.svg
            aws s3 cp --acl public-read ./testResultsImg.svg s3://adpq-assets/buildAssets/testResults.svg
            rm -rf ./testResultsImg.svg

            docker kill -f $(docker ps -q) || true
            docker rm -f $(docker ps -a -q) || true
            docker rmi -f $(docker images -q) || true
        '''
    }
}

def deployStaging() {
    stage ('Deploy') { // Create New Task Definition and Create/Update ECS Service
        sh "exec bash"

        sh '''#!/bin/bash

            ### Constants
            ECS_REGION=us-west-1
            ECR_REPOSITORY_NAME_SERVER=adpq-server
            ECS_CLUSTER=adpq-staging
            ECS_SERVICE=adpq-staging-service
            ECS_FAMILY=adpq-staging
            ECS_TASK_DEFINITION=adpq-staging

            ### Functions
            function main() {
                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Get Current ECS Status"
                getECSStatus;

                if (( $CURRENT_DESIRED_COUNT>0 )); then
                    echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Update Service - Decrement Current Desired Count By 1"
                    updateECSService ${ECS_FAMILY}:${REVISION_NUMBER} $(expr $CURRENT_DESIRED_COUNT - 1)
                else
                    echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Current Desired Count is 0, set to 1"
                    CURRENT_DESIRED_COUNT=1
                fi

                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Update Task Definition Revision Number"
                updateTaskDefinition;

                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Wait For Existing Task To Stop"
                waitForNumberOfRunningTasks 0

                if [ "$SERVICE_FAILURES" == "" ]; then

                    if [[ $CURRENT_DESIRED_COUNT=0 ]]; then
                        CURRENT_DESIRED_COUNT=1
                    fi

                    echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Update Service With New Task Revision and Set Desired Count To 1 "
                    updateECSService ${ECS_FAMILY}:${REVISION_NUMBER} $CURRENT_DESIRED_COUNT

                else
                    echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - No Existing Service, Creating New Service"
                    createECSService;
                fi

                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Waiting for New Task To Start"
                waitForNumberOfRunningTasks 1

                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Success! New Service is currently running."
            }

            function getECSStatus() {
                DECRIBED_SERVICE=$(aws ecs describe-services --cluster $ECS_CLUSTER \
                                                            --services $ECS_SERVICE \
                                                            --region $ECS_REGION)

                CURRENT_DESIRED_COUNT=$(echo $DECRIBED_SERVICE | jq .services[0].desiredCount)
                CURRENT_TASK_REVISION=$(echo $DECRIBED_SERVICE | jq .services[0].taskDefinition)
                CURRENT_RUNNING_COUNT=$(echo $DECRIBED_SERVICE | jq .services[0].runningCount)
                SERVICE_FAILURES=$(echo $DESCRIBED_SERVICE | jq .failures[])
                REVISION_NUMBER=`aws ecs describe-task-definition --task-definition ${ECS_FAMILY} --region ${ECS_REGION} | jq .taskDefinition.revision`
            }

            function updateECSService() {
                aws ecs update-service --cluster $ECS_CLUSTER \
                                    --service $ECS_SERVICE \
                                    --task-definition $1 \
                                    --desired-count $2 \
                                    --region $ECS_REGION
            }

            function createECSService() {
                aws ecs create-service --service-name ${ECS_SERVICE} \
                            --desired-count 1 \
                            --task-definition ${ECS_FAMILY} \
                            --cluster ${ECS_CLUSTER} \
                            --region ${ECS_REGION}
            }

            function updateTaskDefinition() {
                REPOSITORY_URI_SERVER=$(aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME_SERVER} --region ${ECS_REGION} | jq .repositories[].repositoryUri | tr -d '"')
                REPOSITORY_URI_WEB=$(aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME_WEB} --region ${ECS_REGION} | jq .repositories[].repositoryUri | tr -d '"')

                #Replace the build number and respository URI placeholders with the constants above
                sed -e "s;%ECS_FAMILY%;${ECS_FAMILY};g" -e "s;%BUILD_NUMBER%;${BUILD_NUMBER};g" -e "s;%REPOSITORY_URI_SERVER%;${REPOSITORY_URI_SERVER};g" -e "s;%REPOSITORY_URI_WEB%;${REPOSITORY_URI_WEB};g" src/devops/scripts/taskdef.json > ${ECS_TASK_DEFINITION}-v_${BUILD_NUMBER}.json

                #Register the task definition in the repository
                aws ecs register-task-definition --family ${ECS_FAMILY} \
                                                    --cli-input-json file://${ECS_TASK_DEFINITION}-v_${BUILD_NUMBER}.json \
                                                    --region ${ECS_REGION}
            }

            function waitForNumberOfRunningTasks() {
                for attempt in {1..120}; do
                    getECSStatus
                    if [ $CURRENT_RUNNING_COUNT -ne $1 ]; then
                        echo "waiting... $attempt"
                        sleep 1
                    else
                        return 0
                    fi
                done

                echo -e "\n\n$(date "+%Y-%m-%d %H:%M:%S") Waiting for running count to reach $CURRENT_DESIRED_COUNT took to long. Current running task : $CURRENT_RUNNING_TASK\n\n"
                exit 3
            }


            ### Start
            main;
        '''
    }
}

def sendSlackNotification() {
    stage ('Notify') {
        RESULTS = readFile 'RESULTS'
        RESULT_TYPE = readFile 'RESULT_TYPE'
        sh "sleep 10 && logs=\$(git log -1 --pretty=%B origin/staging) && echo \'$RESULT_TYPE\' && node ./src/devops/scripts/slackNotification.js \'$RESULT_TYPE\' \"*New Staging Build Available*\nhttp://adpq-staging.hotbsoftware.com\n\n*Build Notes:*\n\$logs\n\n\" \'$RESULTS\'"
    }
}

def deployProduction() {
    stage ('Deploy') { // Create New Task Definition and Create/Update ECS Service
        sh "exec bash"

        sh '''#!/bin/bash

            ### Constants
            ECS_REGION=us-west-1
            ECR_REPOSITORY_NAME_SERVER=adpq-server
            ECS_CLUSTER=adpq-production
            ECS_SERVICE=adpq-production-service
            ECS_FAMILY=adpq-production
            ECS_TASK_DEFINITION=adpq-production

            ### Functions
            function main() {
                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Get Current ECS Status"
                getECSStatus;

                if (( $CURRENT_DESIRED_COUNT>0 )); then
                    echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Update Service - Decrement Current Desired Count By 1"
                    updateECSService ${ECS_FAMILY}:${REVISION_NUMBER} $(expr $CURRENT_DESIRED_COUNT - 1)
                else
                    echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Current Desired Count is 0, set to 1"
                    CURRENT_DESIRED_COUNT=1
                fi

                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Update Task Definition Revision Number"
                updateTaskDefinition;

                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Wait For Existing Task To Stop"
                waitForNumberOfRunningTasks 0

                if [ "$SERVICE_FAILURES" == "" ]; then

                    if [[ $CURRENT_DESIRED_COUNT=0 ]]; then
                        CURRENT_DESIRED_COUNT=1
                    fi

                    echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Update Service With New Task Revision and Set Desired Count To 1 "
                    updateECSService ${ECS_FAMILY}:${REVISION_NUMBER} $CURRENT_DESIRED_COUNT

                else
                    echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - No Existing Service, Creating New Service"
                    createECSService;
                fi

                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Waiting for New Task To Start"
                waitForNumberOfRunningTasks 1

                echo "DEBUG:$(date "+%Y-%m-%d %H:%M:%S") - Success! New Service is currently running."
            }

            function getECSStatus() {
                DECRIBED_SERVICE=$(aws ecs describe-services --cluster $ECS_CLUSTER \
                                                            --services $ECS_SERVICE \
                                                            --region $ECS_REGION)

                CURRENT_DESIRED_COUNT=$(echo $DECRIBED_SERVICE | jq .services[0].desiredCount)
                CURRENT_TASK_REVISION=$(echo $DECRIBED_SERVICE | jq .services[0].taskDefinition)
                CURRENT_RUNNING_COUNT=$(echo $DECRIBED_SERVICE | jq .services[0].runningCount)
                SERVICE_FAILURES=$(echo $DESCRIBED_SERVICE | jq .failures[])
                REVISION_NUMBER=`aws ecs describe-task-definition --task-definition ${ECS_FAMILY} --region ${ECS_REGION} | jq .taskDefinition.revision`
            }

            function updateECSService() {
                aws ecs update-service --cluster $ECS_CLUSTER \
                                    --service $ECS_SERVICE \
                                    --task-definition $1 \
                                    --desired-count $2 \
                                    --region $ECS_REGION
            }

            function createECSService() {
                aws ecs create-service --service-name ${ECS_SERVICE} \
                            --desired-count 1 \
                            --task-definition ${ECS_FAMILY} \
                            --cluster ${ECS_CLUSTER} \
                            --region ${ECS_REGION}
            }

            function updateTaskDefinition() {
                REPOSITORY_URI_SERVER=$(aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME_SERVER} --region ${ECS_REGION} | jq .repositories[].repositoryUri | tr -d '"')
                REPOSITORY_URI_WEB=$(aws ecr describe-repositories --repository-names ${ECR_REPOSITORY_NAME_WEB} --region ${ECS_REGION} | jq .repositories[].repositoryUri | tr -d '"')

                #Replace the build number and respository URI placeholders with the constants above
                sed -e "s;%ECS_FAMILY%;${ECS_FAMILY};g" -e "s;%BUILD_NUMBER%;${BUILD_NUMBER};g" -e "s;%REPOSITORY_URI_SERVER%;${REPOSITORY_URI_SERVER};g" -e "s;%REPOSITORY_URI_WEB%;${REPOSITORY_URI_WEB};g" src/devops/scripts/taskdef.json > ${ECS_TASK_DEFINITION}-v_${BUILD_NUMBER}.json

                #Register the task definition in the repository
                aws ecs register-task-definition --family ${ECS_FAMILY} \
                                                    --cli-input-json file://${ECS_TASK_DEFINITION}-v_${BUILD_NUMBER}.json \
                                                    --region ${ECS_REGION}
            }

            function waitForNumberOfRunningTasks() {
                for attempt in {1..120}; do
                    getECSStatus
                    if [ $CURRENT_RUNNING_COUNT -ne $1 ]; then
                        echo "waiting... $attempt"
                        sleep 1
                    else
                        return 0
                    fi
                done

                echo -e "\n\n$(date "+%Y-%m-%d %H:%M:%S") Waiting for running count to reach $CURRENT_DESIRED_COUNT took to long. Current running task : $CURRENT_RUNNING_TASK\n\n"
                exit 3
            }


            ### Start
            main;
        '''
    }

    stage ('Notify') {
        def nodeHome = tool 'NodeTool'
        env.PATH="${env.PATH}:${nodeHome}/bin"

        sh '''#!/bin/bash
            sleep 10
            logs=$(git log -1 --pretty=%B origin/production)
            node ./src/devops/scripts/slackNotification.js "SUCCESS" "*New Production Build Available*:\nhttp://adpq.hotbsoftware.com\n\n*Build Notes:*\n$logs"
        '''
    }
}