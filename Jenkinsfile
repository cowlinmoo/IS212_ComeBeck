pipeline {
    agent any

    triggers {
        githubPullRequests(
            spec: '',
            triggerMode: 'HEAVY_HOOKS',
            events: [
                [$class: 'org.jenkinsci.plugins.github.pullrequest.events.impl.GitHubPROpenEvent'],
                [$class: 'org.jenkinsci.plugins.github.pullrequest.events.impl.GitHubPRCommitEvent']
            ],
            branchRestriction: [targetBranch: 'main'],
            cancelQueued: true,
            abortRunning: false
        )
    }

    environment {
        ACR_NAME = credentials('ACR_NAME')
        IMAGE_NAME = credentials('IMAGE_NAME')
        ACR_USERNAME = credentials('ACR_USERNAME')
        ACR_PASSWORD = credentials('ACR_PASSWORD')
        TENANT_ID = credentials('TENANT_ID')
        CONTAINER_APP_NAME = credentials('CONTAINER_APP_NAME')
        RESOURCE_GROUP = credentials('RESOURCE_GROUP')
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')
        GIT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
        BUILD_CONTEXT = "Jenkins: 1. Build"
        PUBLISH_CONTEXT = "Jenkins: 2. Publish"
        DEPLOY_CONTEXT = "Jenkins: 3. Deploy"
        GITHUB_REPO = "cowlinmoo/IS212_ComeBeck"
    }

    stages {
        stage('Build') {
            steps {
                withChecks(name: 'Build', includeStage: true) {
                    sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                }
            }
        }

        stage('Publish') {
            steps {
                withChecks(name: 'Publish', includeStage: true) {
                    sh "echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin"
                    sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy') {
            steps {
                withChecks(name: 'Deploy', includeStage: true) {
                    sh '''#!/bin/bash
                        set -e
                        if ! command -v az &> /dev/null
                        then
                            echo "Azure CLI not found. Installing..."
                            curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
                        else
                            echo "Azure CLI is already installed."
                        fi

                        echo "Logging in to Azure..."
                        az login --service-principal -u ${ACR_USERNAME} -p ${ACR_PASSWORD} --tenant ${TENANT_ID}

                        echo "Updating Container App..."
                        az containerapp update \
                          --name ${CONTAINER_APP_NAME} \
                          --resource-group ${RESOURCE_GROUP} \
                          --image ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}

                        echo "Logging out from Azure..."
                        az logout
                    '''
                }
            }
        }
    }

    post {
        always {
            publishChecks name: 'Pipeline Summary', 
                          title: 'Pipeline Result', 
                          summary: "Pipeline finished with result: ${currentBuild.result}",
                          text: '''This is an overall summary of the pipeline execution.
                                   It includes the Build, Publish, and Deploy stages.''',
                          detailsURL: "${env.BUILD_URL}",
                          actions: [[label: 'Rerun', description: 'Rerun the pipeline', identifier: "rerun_${env.BUILD_NUMBER}"]]
        }
        success {
            publishChecks name: 'Pipeline Status', 
                          conclusion: 'SUCCESS',
                          title: 'Pipeline Succeeded', 
                          summary: 'All stages completed successfully.',
                          text: 'The pipeline has successfully built, published, and deployed the application.'
        }
        failure {
            publishChecks name: 'Pipeline Status', 
                          conclusion: 'FAILURE',
                          title: 'Pipeline Failed', 
                          summary: 'One or more stages failed.',
                          text: 'Please check the Jenkins console output for more details on the failure.'
        }
    }
}
