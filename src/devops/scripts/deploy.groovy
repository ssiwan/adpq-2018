node {
    stage('Checkout') {

        // Load Node.js
        def nodeHome = tool 'NodeTool'
        env.PATH="${env.PATH}:${nodeHome}/bin"

        // Checkout Git Source Code
        def scmVars = checkout scm

        // Run job based on current branch
        if (scmVars.GIT_COMMIT == scmVars.GIT_PREVIOUS_SUCCESSFUL_COMMIT) {
            println "Nothing new to commit || Neither the master nor staging branch..."
        } else {
            // Build and deploy to staging
            if (scmVars.GIT_BRANCH == 'origin/staging') {
                sh 'cp /aws/adpq/server/staging/config.json ./src/server/src/config.json' // Setup Staging Config for Deployment
                deployStaging()
                runStagingTests()
                sendSlackNotification()
            } else if (scmVars.GIT_BRANCH == 'origin/master') {
                println "Master Branch, do nothing..."
            }
        }
    }

    // stage ('Clean Up') { // Clean Up Workspace
    //     // deleteDir()
    // }
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
            rm -rf ./testResultsImg.svg || true
            curl $testBadge >> ./testResultsImg.svg
            aws s3 cp --acl public-read --cache-control no-cache ./testResultsImg.svg s3://adpq-assets/buildAssets/testResults.svg
            
            # Wait
            sleep 2

            # Docker Cleanup
            docker system prune -f
        '''
    }
}

def deployStaging() {
    stage ('Deploy') { // Create New Task Definition and Create/Update ECS Service
        sh "exec bash"
        sh "cd src/devops/scripts && sh deployStaging.sh ${BUILD_NUMBER}"
    }
}

def sendSlackNotification() {
    stage ('Notify') {
        // RESULTS = readFile 'RESULTS'
        // RESULT_TYPE = readFile 'RESULT_TYPE'
        sh "sleep 10 && logs=\$(git log -1 --pretty=%B origin/staging) && node ./src/devops/scripts/slackNotification.js \"SUCCESS\" \"*New Staging Build Available*\nhttp://adpq-staging.hotbsoftware.com\n\n*Build Notes:*\n\$logs\n\n\""

        // Cleanup
        sh '''
            # Docker Cleanup
            docker kill -f $(docker ps -q) || true
            docker rm -f $(docker ps -a -q) || true
            docker rmi -f $(docker images -q) || true
        '''
    }
}