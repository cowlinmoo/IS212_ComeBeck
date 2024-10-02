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
        GITHUB_REPO = "IS212_ComeBeck"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    githubNotify account: 'cowlinmoo', context: 'Build Docker Image', credentialsId: 'githubpat', description: 'Building Docker Image In Jenkins', gitApiUrl: '', repo: "${GITHUB_REPO}", sha: "${GIT_COMMIT}", status: 'PENDING', targetUrl: "${env.BUILD_URL}"

                    try {
                        sh "docker build -t ${env.ACR_NAME}.azurecr.io/${env.IMAGE_NAME}:${env.BUILD_NUMBER} ."
                        githubNotify account: 'cowlinmoo', context: 'Build Docker Image', credentialsId: 'githubpat', description: 'Docker Image Built Successfully', gitApiUrl: '', repo: "${GITHUB_REPO}", sha: "${GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                    } catch (Exception e) {
                        githubNotify account: 'cowlinmoo', context: 'Build Docker Image', credentialsId: 'githubpat', description: 'Docker Image Build Failed', gitApiUrl: '', repo: "${GITHUB_REPO}", sha: "${GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                        throw e
                    }

                    publishChecks name: 'Jenkins: Build Docker Image',
                                  title: 'Build Result',
                                  summary: 'Build Completed',
                                  text: 'Docker image built',
                                  conclusion: (currentBuild.result == 'SUCCESS') ? 'SUCCESS' : 'FAILURE',
                                  detailsURL: "${env.BUILD_URL}"
                }
            }
        }

        stage('Publish') {
            steps {
                script {
                    githubNotify account: 'cowlinmoo', context: 'Publish Docker Image', credentialsId: 'githubpat', description: 'Publishing Docker Image to registry', gitApiUrl: '', repo: "${GITHUB_REPO}", sha: "${GIT_COMMIT}", status: 'PENDING', targetUrl: "${env.BUILD_URL}"

                    try {
                        sh "echo ${env.ACR_PASSWORD} | docker login ${env.ACR_NAME}.azurecr.io -u ${env.ACR_USERNAME} --password-stdin"
                        sh "docker push ${env.ACR_NAME}.azurecr.io/${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
                        githubNotify account: 'cowlinmoo', context: 'Publish Docker Image', credentialsId: 'githubpat', description: 'Docker Image Published Successfully', gitApiUrl: '', repo: "${GITHUB_REPO}", sha: "${GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                    } catch (Exception e) {
                        githubNotify account: 'cowlinmoo', context: 'Publish Docker Image', credentialsId: 'githubpat', description: 'Docker Image Publish Failed', gitApiUrl: '', repo: "${GITHUB_REPO}", sha: "${GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                        throw e
                    }

                    publishChecks name: 'Jenkins: Publish Docker Image',
                                  title: 'Publish Result',
                                  summary: 'Publish Completed',
                                  text: 'Docker image published',
                                  conclusion: (currentBuild.result == 'SUCCESS') ? 'SUCCESS' : 'FAILURE',
                                  detailsURL: "${env.BUILD_URL}"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    githubNotify account: 'cowlinmoo', context: 'Deploy Docker Image', credentialsId: 'githubpat', description: 'Deploying to Azure Container App', gitApiUrl: '', repo: "${GITHUB_REPO}", sha: "${GIT_COMMIT}", status: 'PENDING', targetUrl: "${env.BUILD_URL}"

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
                            az login --service-principal -u ${env.ACR_USERNAME} -p ${env.ACR_PASSWORD} --tenant ${env.TENANT_ID}

                            echo "Updating Container App..."
                            az containerapp update \
                              --name ${env.CONTAINER_APP_NAME} \
                              --resource-group ${env.RESOURCE_GROUP} \
                              --image ${env.ACR_NAME}.azurecr.io/${env.IMAGE_NAME}:${env.BUILD_NUMBER}

                            echo "Logging out from Azure..."
                            az logout
                        '''
                        githubNotify account: 'cowlinmoo', context: 'Deploy Docker Image', credentialsId: 'githubpat', description: 'Deployment Successful', gitApiUrl: '', repo: "${GITHUB_REPO}", sha: "${GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                    } catch (Exception e) {
                        githubNotify account: 'cowlinmoo', context: 'Deploy Docker Image', credentialsId: 'githubpat', description: 'Deployment Failed', gitApiUrl: '', repo: "${GITHUB_REPO}", sha: "${GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                        throw e
                    }

                    publishChecks name: 'Jenkins: Deploy Docker Image',
                                  title: 'Deploy Result',
                                  summary: 'Deploy Completed',
                                  text: 'Docker image deployed',
                                  conclusion: (currentBuild.result == 'SUCCESS') ? 'SUCCESS' : 'FAILURE',
                                  detailsURL: "${env.BUILD_URL}"
                }
            }
        }
    }

    post {
        always {
            script {
                def buildStatus = currentBuild.result ?: 'SUCCESS'
                def description = "Pipeline finished with result: ${buildStatus}"

                publishChecks name: 'Jenkins Continuous Integration Pipeline',
                              title: 'Pipeline Result',
                              summary: description,
                              text: """
                              Build Number: ${env.BUILD_NUMBER}
                              Build URL: ${env.BUILD_URL}
                              Git Commit: ${env.GIT_COMMIT}
                              """,
                              conclusion: (buildStatus == 'SUCCESS') ? 'SUCCESS' : 'FAILURE',
                              detailsURL: "${env.BUILD_URL}",
                              actions: [[label: 'Rerun Pipeline', description: 'Rerun the Jenkins pipeline', identifier: 'rerun_pipeline']]
            }
        }
    }
}
