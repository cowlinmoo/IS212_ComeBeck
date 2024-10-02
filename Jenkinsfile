pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        ACR_NAME = credentials('ACR_NAME')
        IMAGE_NAME = credentials('IMAGE_NAME')
        ACR_USERNAME = credentials('ACR_USERNAME')
        ACR_PASSWORD = credentials('ACR_PASSWORD')
        TENANT_ID = credentials('TENANT_ID')
        CONTAINER_APP_NAME = credentials('CONTAINER_APP_NAME')
        RESOURCE_GROUP = credentials('RESOURCE_GROUP')
        GIT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
        GITHUB_REPO = "IS212_ComeBeck"
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')
    }

    stages {
        stage('Build') {
            steps {
                script {
                    updateGitHubStatus('pending', 'Building Docker image', 'Jenkins: 1. Build')

                    try {
                        sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        updateGitHubStatus('success', 'Docker image built successfully', 'Jenkins: 1. Build')
                    } catch (Exception e) {
                        updateGitHubStatus('failure', 'Docker image build failed', 'Jenkins: 1. Build')
                        throw e
                    }
                }
            }
        }

        stage('Publish') {
            steps {
                script {
                    updateGitHubStatus('pending', 'Publishing to ACR', 'Jenkins: 2. Publish')

                    try {
                        sh "echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin"
                        sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}"
                        updateGitHubStatus('success', 'Image published to ACR successfully', 'Jenkins: 2. Publish')
                    } catch (Exception e) {
                        updateGitHubStatus('failure', 'Image publish failed', 'Jenkins: 2. Publish')
                        throw e
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    updateGitHubStatus('pending', 'Deploying to Azure', 'Jenkins: 3. Deploy')

                    try {
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
                            az login --service-principal -u $ACR_USERNAME -p $ACR_PASSWORD --tenant $TENANT_ID

                            echo "Updating Container App..."
                            az containerapp update \
                              --name $CONTAINER_APP_NAME \
                              --resource-group $RESOURCE_GROUP \
                              --image $ACR_NAME.azurecr.io/$IMAGE_NAME:$BUILD_NUMBER

                            echo "Logging out from Azure..."
                            az logout
                        '''
                        updateGitHubStatus('success', 'Application deployed to Azure successfully', 'Jenkins: 3. Deploy')
                    } catch (Exception e) {
                        updateGitHubStatus('failure', 'Deployment failed', 'Jenkins: 3. Deploy')
                        throw e
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                def buildStatus = currentBuild.result ?: 'SUCCESS'
                def description = "Pipeline finished with result: ${buildStatus}"
            }
        }
    }
}

def updateGitHubStatus(String state, String description, String context) {
    sh """
        curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
             -X POST \
             -H "Accept: application/vnd.github.v3+json" \
             https://api.github.com/repos/cowlinmoo/IS212_ComeBeck/statuses/${GIT_COMMIT} \
             -d "{\\"state\\":\\"${state}\\",\\"context\\":\\"${context}\\",\\"description\\":\\"${description}\\",\\"target_url\\":\\"${env.BUILD_URL}\\"}"
    """
}
