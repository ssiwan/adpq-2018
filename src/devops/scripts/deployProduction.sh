#!/bin/bash

#
#    deployProduction.sh
#
#    This script will build and deploy an ECS docker image. Make sure all constants are correct and to pass in a valid build number as an argument.
#
#    Args:
#    $1 = Build Number (ex. 0.0.1)
#  
#    Example Command:
#    sh deployProduction.sh 0.0.1
#

### Constants
BUILD_NUMBER=$1
ECS_REGION=us-west-1
ECR_REPOSITORY_NAME_SERVER=adpq-server
ECS_CLUSTER=adpq-production
ECS_SERVICE=adpq-production-service
ECS_FAMILY=adpq-production
ECS_TASK_DEFINITION=adpq-production

### Build & Tag ECS Docker Image
export NODE_ENV='production'
docker build -t adpq-server ../../server &&
$(aws ecr get-login --no-include-email --region us-west-1) &&

docker tag adpq-server 485490441211.dkr.ecr.us-west-1.amazonaws.com/adpq-server:v_${BUILD_NUMBER}-production &&
docker push 485490441211.dkr.ecr.us-west-1.amazonaws.com/adpq-server:v_${BUILD_NUMBER}-production &&

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
    sed -e "s;%ECS_FAMILY%;${ECS_FAMILY};g" -e "s;%BUILD_NUMBER%;${BUILD_NUMBER}-production;g" -e "s;%REPOSITORY_URI_SERVER%;${REPOSITORY_URI_SERVER};g" -e "s;%REPOSITORY_URI_WEB%;${REPOSITORY_URI_WEB};g" -e "s;%ENVIRONMENT%;${ENVIRONMENT};g" ./taskdef.json > ${ECS_TASK_DEFINITION}-v_${BUILD_NUMBER}-production.json

    echo ${ECS_TASK_DEFINITION}
    echo ${BUILD_NUMBER}
    echo ${ECS_TASK_DEFINITION}-v_${BUILD_NUMBER}-production

    #Register the task definition in the repository
    aws ecs register-task-definition --family ${ECS_FAMILY} \
                                        --cli-input-json file://${ECS_TASK_DEFINITION}-v_${BUILD_NUMBER}-production.json \
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


#############
#   Start   #
#############
main;