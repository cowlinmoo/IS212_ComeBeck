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
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    githubNotify context: env.BUILD_CONTEXT, description: 'Building Docker image', status: 'PENDING'
                    githubNotify context: env.PUBLISH_CONTEXT, description: 'Publishing to ACR', status: 'PENDING'
                    githubNotify context: env.DEPLOY_CONTEXT, description: 'Deploying to Azure', status: 'PENDING'
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    try {
                        sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        githubNotify context: env.BUILD_CONTEXT, description: 'Docker image built successfully', status: 'SUCCESS'
                    } catch (Exception e) {
                        githubNotify context: env.BUILD_CONTEXT, description: 'Failed during: Build', status: 'FAILURE'
                        error("Build stage failed: ${e.message}")
                    }
                }
            }
        }

        stage('Publish') {
            steps {
                script {
                    try {
                        sh "echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin"
                        sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}"
                        githubNotify context: env.PUBLISH_CONTEXT, description: 'Image published to ACR successfully', status: 'SUCCESS'
                    } catch (Exception e) {
                        githubNotify context: env.PUBLISH_CONTEXT, description: 'Failed during: Publish', status: 'FAILURE'
                        error("Publish stage failed: ${e.message}")
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
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
                        githubNotify context: env.DEPLOY_CONTEXT, description: 'Application deployed to Azure successfully', status: 'SUCCESS'
                    } catch (Exception e) {
                        githubNotify context: env.DEPLOY_CONTEXT, description: 'Failed during: Deploy', status: 'FAILURE'
                        error("Deploy stage failed: ${e.message}")
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                githubNotify context: env.BUILD_CONTEXT, description: 'Pipeline completed successfully', status: 'SUCCESS'
                githubNotify context: env.PUBLISH_CONTEXT, description: 'Pipeline completed successfully', status: 'SUCCESS'
                githubNotify context: env.DEPLOY_CONTEXT, description: 'Pipeline completed successfully', status: 'SUCCESS'
            }
        }
        failure {
            script {
                githubNotify context: env.BUILD_CONTEXT, description: 'Pipeline failed', status: 'FAILURE'
                githubNotify context: env.PUBLISH_CONTEXT, description: 'Pipeline failed', status: 'FAILURE'
                githubNotify context: env.DEPLOY_CONTEXT, description: 'Pipeline failed', status: 'FAILURE'
            }
        }
    }
}
