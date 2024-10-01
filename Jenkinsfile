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
        stage('Initialize') {
            steps {
                script {
                    notifyGitHub('PENDING', 'Building Docker image', env.BUILD_CONTEXT)
                    notifyGitHub('PENDING', 'Publishing to ACR', env.PUBLISH_CONTEXT)
                    notifyGitHub('PENDING', 'Deploying to Azure', env.DEPLOY_CONTEXT)
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    try {
                        sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        notifyGitHub('SUCCESS', 'Docker image built successfully', env.BUILD_CONTEXT)
                    } catch (Exception e) {
                        notifyGitHub('FAILURE', 'Failed during: Build', env.BUILD_CONTEXT)
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
                        notifyGitHub('SUCCESS', 'Image published to ACR successfully', env.PUBLISH_CONTEXT)
                    } catch (Exception e) {
                        notifyGitHub('FAILURE', 'Failed during: Publish', env.PUBLISH_CONTEXT)
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
                        notifyGitHub('SUCCESS', 'Application deployed to Azure successfully', env.DEPLOY_CONTEXT)
                    } catch (Exception e) {
                        notifyGitHub('FAILURE', 'Failed during: Deploy', env.DEPLOY_CONTEXT)
                        error("Deploy stage failed: ${e.message}")
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                notifyGitHub('SUCCESS', 'Pipeline completed successfully', env.BUILD_CONTEXT)
                notifyGitHub('SUCCESS', 'Pipeline completed successfully', env.PUBLISH_CONTEXT)
                notifyGitHub('SUCCESS', 'Pipeline completed successfully', env.DEPLOY_CONTEXT)
            }
        }
        failure {
            script {
                notifyGitHub('FAILURE', 'Pipeline failed', env.BUILD_CONTEXT)
                notifyGitHub('FAILURE', 'Pipeline failed', env.PUBLISH_CONTEXT)
                notifyGitHub('FAILURE', 'Pipeline failed', env.DEPLOY_CONTEXT)
            }
        }
    }
}

def notifyGitHub(status, description, context) {
    githubNotify account: 'cowlinmoo', 
                 credentialsId: 'GITHUB_TOKEN',
                 description: description, 
                 context: context,
                 sha: env.GIT_COMMIT,
                 repo: env.GITHUB_REPO,
                 status: status
}
