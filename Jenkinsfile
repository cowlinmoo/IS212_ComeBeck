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
        GIT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
        GITHUB_REPO = "cowlinmoo/IS212_ComeBeck"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo "About to notify GitHub: Build in progress"
                    githubNotify account: 'cowlinmoo', context: 'Jenkins: Build Docker Image', credentialsId: 'githubpat', description: 'Building Docker Image', gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'PENDING', targetUrl: "${env.BUILD_URL}"
                    
                    try {
                        sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        echo "About to notify GitHub: Build successful"
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Build Docker Image', credentialsId: 'githubpat', description: 'Docker Image Built Successfully', gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                    } catch (Exception e) {
                        echo "About to notify GitHub: Build failed"
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Build Docker Image', credentialsId: 'githubpat', description: 'Docker Image Build Failed', gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                        throw e
                    }
                }
            }
        }

        stage('Publish') {
            steps {
                script {
                    echo "About to notify GitHub: Publish in progress"
                    githubNotify account: 'cowlinmoo', context: 'Jenkins: Publish Docker Image', credentialsId: 'githubpat', description: 'Publishing Docker Image to container registry', gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'PENDING', targetUrl: "${env.BUILD_URL}"
                    
                    try {
                        sh "echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin"
                        sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}"
                        echo "About to notify GitHub: Publish successful"
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Publish Docker Image', credentialsId: 'githubpat', description: 'Docker Image Published Successfully', gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                    } catch (Exception e) {
                        echo "About to notify GitHub: Publish failed"
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Publish Docker Image', credentialsId: 'githubpat', description: 'Docker Image Publish Failed', gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                        throw e
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "About to notify GitHub: Deploy in progress"
                    githubNotify account: 'cowlinmoo', context: 'Jenkins: Deploy Docker Image', credentialsId: 'githubpat', description: 'Deploying to Azure Container App', gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'PENDING', targetUrl: "${env.BUILD_URL}"
                    
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
                        echo "About to notify GitHub: Deploy successful"
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Deploy Docker Image', credentialsId: 'githubpat', description: 'Deployment Successful', gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                    } catch (Exception e) {
                        echo "About to notify GitHub: Deploy failed"
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Deploy Docker Image', credentialsId: 'githubpat', description: 'Deployment Failed', gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                        throw e
                    }
                }
            }
        }
    }

    post {
        always {
            echo "About to notify GitHub: Pipeline Summary"
            githubNotify account: 'cowlinmoo', context: 'Jenkins Continuous Integration Pipeline', credentialsId: 'githubpat', description: "Pipeline finished with result: ${currentBuild.result}", gitApiUrl: '', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: "${currentBuild.result == 'SUCCESS' ? 'SUCCESS' : 'FAILURE'}", targetUrl: "${env.BUILD_URL}"
        }
    }
}
