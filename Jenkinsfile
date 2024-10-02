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
                    // Notify GitHub (Status API - for the dot)
                    githubNotify account: 'cowlinmoo', context: 'Jenkins: Build Docker Image', credentialsId: 'githubpat', description: 'Building Docker Image', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'PENDING', targetUrl: "${env.BUILD_URL}"

                    try {
                        sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Build Docker Image', credentialsId: 'githubpat', description: 'Docker Image Built Successfully', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                    } catch (Exception e) {
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Build Docker Image', credentialsId: 'githubpat', description: 'Docker Image Build Failed', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                        throw e
                    }

                    // Publish GitHub Check (Checks API)
                    publishChecks name: 'Jenkins: Build Docker Image',
                                  title: 'Build Result',
                                  summary: 'Build Completed',
                                  text: 'Docker image built',
                                  conclusion: currentBuild.result ?: 'success',
                                  detailsURL: "${env.BUILD_URL}"
                }
            }
        }

        stage('Publish') {
            steps {
                script {
                    githubNotify account: 'cowlinmoo', context: 'Jenkins: Publish Docker Image', credentialsId: 'githubpat', description: 'Publishing Docker Image to registry', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'PENDING', targetUrl: "${env.BUILD_URL}"

                    try {
                        sh "echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin"
                        sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}"
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Publish Docker Image', credentialsId: 'githubpat', description: 'Docker Image Published Successfully', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                    } catch (Exception e) {
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Publish Docker Image', credentialsId: 'githubpat', description: 'Docker Image Publish Failed', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                        throw e
                    }

                    publishChecks name: 'Jenkins: Publish Docker Image',
                                  title: 'Publish Result',
                                  summary: 'Publish Completed',
                                  text: 'Docker image published',
                                  conclusion: currentBuild.result ?: 'success',
                                  detailsURL: "${env.BUILD_URL}"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    githubNotify account: 'cowlinmoo', context: 'Jenkins: Deploy Docker Image', credentialsId: 'githubpat', description: 'Deploying to Azure Container App', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'PENDING', targetUrl: "${env.BUILD_URL}"

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
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Deploy Docker Image', credentialsId: 'githubpat', description: 'Deployment Successful', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'SUCCESS', targetUrl: "${env.BUILD_URL}"
                    } catch (Exception e) {
                        githubNotify account: 'cowlinmoo', context: 'Jenkins: Deploy Docker Image', credentialsId: 'githubpat', description: 'Deployment Failed', repo: 'IS212_ComeBeck', sha: "${GIT_COMMIT}", status: 'FAILURE', targetUrl: "${env.BUILD_URL}"
                        throw e
                    }

                    publishChecks name: 'Jenkins: Deploy Docker Image',
                                  title: 'Deploy Result',
                                  summary: 'Deploy Completed',
                                  text: 'Docker image deployed',
                                  conclusion: currentBuild.result ?: 'success',
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
                              Build Number: ${BUILD_NUMBER}
                              Build URL: ${BUILD_URL}
                              Git Commit: ${GIT_COMMIT}
                              
                              Stages:
                              - Build: ${currentBuild.rawBuild.getExecution().getStages().find { it.name == 'Build' }?.status ?: 'N/A'}
                              - Publish: ${currentBuild.rawBuild.getExecution().getStages().find { it.name == 'Publish' }?.status ?: 'N/A'}
                              - Deploy: ${currentBuild.rawBuild.getExecution().getStages().find { it.name == 'Deploy' }?.status ?: 'N/A'}
                              """,
                              conclusion: buildStatus.toLowerCase(),
                              detailsURL: "${BUILD_URL}",
                              actions: [[label: 'Rerun Pipeline', description: 'Rerun the Jenkins pipeline', identifier: 'rerun_pipeline']]
            }
        }
    }
}
