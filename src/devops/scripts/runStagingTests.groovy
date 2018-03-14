node {
    stage('Checkout') {
        checkout scm
        runStagingTests()
        sendSlackNotification()
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

            # Build & run container
            docker build ./src/qa -t adpq_tests &&
            docker run -e Environment=staging -v /var/lib/jenkins/adpq_test_results/reports:/data/reports --name adpq_tests -i adpq_tests >> /var/lib/jenkins/adpq_test_results/results.xml &&
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

def sendSlackNotification() {
    stage ('Notify') {
        RESULTS = readFile 'RESULTS'
        RESULT_TYPE = readFile 'RESULT_TYPE'
        sh "sleep 10 && node ./src/devops/scripts/slackNotification.js \"$RESULT_TYPE\" \"*Nightly Test Results*\" \"$RESULTS\""
    }
}