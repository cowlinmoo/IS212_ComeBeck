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
        GITHUB_REPO = "cowlinmoo/IS212_ComeBeck"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    publishChecks name: 'Jenkins: Build',
                                  title: 'Building Docker Image',
                                  summary: 'Building the Docker image for the application',
                                  text: 'This step builds the Docker image using the Dockerfile in the repository.',
                                  status: 'IN_PROGRESS'
                    
                    try {
                        sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        publishChecks name: 'Jenkins: Build',
                                      conclusion: 'SUCCESS',
                                      title: 'Docker Image Built Successfully',
                                      summary: 'The Docker image was built without any issues.'
                    } catch (Exception e) {
                        publishChecks name: 'Jenkins: Build',
                                      conclusion: 'FAILURE',
                                      title: 'Docker Image Build Failed',
                                      summary: 'There was an error while building the Docker image.',
                                      text: "Error: ${e.message}"
                        throw e
                    }
                }
            }
        }

        stage('Publish') {
            steps {
                script {
                    publishChecks name: 'Jenkins: Publish',
                                  title: 'Publishing Docker Image',
                                  summary: 'Publishing the Docker image to Azure Container Registry',
                                  text: 'This step pushes the built Docker image to ACR.',
                                  status: 'IN_PROGRESS'
                    
                    try {
                        sh "echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin"
                        sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}"
                        publishChecks name: 'Jenkins: Publish',
                                      conclusion: 'SUCCESS',
                                      title: 'Docker Image Published Successfully',
                                      summary: 'The Docker image was pushed to ACR without any issues.'
                    } catch (Exception e) {
                        publishChecks name: 'Jenkins: Publish',
                                      conclusion: 'FAILURE',
                                      title: 'Docker Image Publish Failed',
                                      summary: 'There was an error while publishing the Docker image to ACR.',
                                      text: "Error: ${e.message}"
                        throw e
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    publishChecks name: 'Jenkins: Deploy',
                                  title: 'Deploying to Azure Container App',
                                  summary: 'Updating the Azure Container App with the new image',
                                  text: 'This step deploys the new image to Azure Container App.',
                                  status: 'IN_PROGRESS'
                    
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
                            az login --service-principal -u ${ACR_USERNAME} -p ${ACR_PASSWORD} --tenant ${TENANT_ID}

                            echo "Updating Container App..."
                            az containerapp update \
                              --name ${CONTAINER_APP_NAME} \
                              --resource-group ${RESOURCE_GROUP} \
                              --image ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}

                            echo "Logging out from Azure..."
                            az logout
                        '''
                        publishChecks name: 'Jenkins: Deploy',
                                      conclusion: 'SUCCESS',
                                      title: 'Deployment Successful',
                                      summary: 'The application was successfully deployed to Azure Container App.'
                    } catch (Exception e) {
                        publishChecks name: 'Jenkins: Deploy',
                                      conclusion: 'FAILURE',
                                      title: 'Deployment Failed',
                                      summary: 'There was an error while deploying to Azure Container App.',
                                      text: "Error: ${e.message}"
                        throw e
                    }
                }
            }
        }
    }

    post {
        always {
            publishChecks name: 'Jenkins: Pipeline Summary', 
                          title: 'Pipeline Result', 
                          summary: "Pipeline finished with result: ${currentBuild.result}",
                          text: '''This is an overall summary of the pipeline execution.
                                   It includes the Build, Publish, and Deploy stages.''',
                          detailsURL: "${env.BUILD_URL}",
                          actions: [[label: 'Rerun', description: 'Rerun the pipeline', identifier: "rerun_${env.BUILD_NUMBER}"]]
        }
    }
}
