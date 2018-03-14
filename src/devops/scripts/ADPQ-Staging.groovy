/*
*    ADPQ-Staging.groovy
*    created by HOTB Software
*
*    This script automates the building and deployment for the staging website: https://adpq-staging.hotbsoftware.com.
*    The following code should execute after each successful pull request gets merged into the staging branch.
*
*/

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
                // Setup Staging Config for Deployment
                sh 'cp /aws/adpq/server/staging/config.json ./src/server/src/config.json' 

                // Build and deploy project to ECS
                deployStaging()

                // Send notification to slack channel
                sendSlackNotification()

                 // Clean Up Workspace
                stage ('Clean Up') {
                    deleteDir()
                }
            } else if (scmVars.GIT_BRANCH == 'origin/master') {
                println "Master Branch, do nothing..."
            }
        }
    }
}

def deployStaging() {
    stage ('Build & Deploy') { // Create New Task Definition and Create/Update ECS Service
        sh "exec bash"
        sh "cd src/devops/scripts && sh deployStaging.sh ${BUILD_NUMBER}"
    }
}

def sendSlackNotification() {
    stage ('Notify') {
        sh "sleep 10 && logs=\$(git log -1 --pretty=%B origin/staging) && node ./src/devops/scripts/slackNotification.js \"SUCCESS\" \"*New Staging Build Available*\nhttp://adpq-staging.hotbsoftware.com\n\n*Build Notes:*\n\$logs\n\n\""

        sh '''
            # Docker Cleanup
            docker rmi -f $(docker images -q) || true
        '''
    }
}