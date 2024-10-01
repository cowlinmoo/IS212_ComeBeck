pipeline {
    agent any

    options {
        githubChecks()
    }

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
                    createGitHubCheck(name: 'Build', status: 'QUEUED')
                    createGitHubCheck(name: 'Publish', status: 'QUEUED')
                    createGitHubCheck(name: 'Deploy', status: 'QUEUED')
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    updateGitHubCheck(name: 'Build', status: 'IN_PROGRESS')
                    try {
                        sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        updateGitHubCheck(name: 'Build', status: 'COMPLETED', conclusion: 'SUCCESS')
                    } catch (Exception e) {
                        updateGitHubCheck(name: 'Build', status: 'COMPLETED', conclusion: 'FAILURE')
                        error("Build stage failed: ${e.message}")
                    }
                }
            }
        }

        stage('Publish') {
            steps {
                script {
                    updateGitHubCheck(name: 'Publish', status: 'IN_PROGRESS')
                    try {
                        sh "echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin"
                        sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}"
                        updateGitHubCheck(name: 'Publish', status: 'COMPLETED', conclusion: 'SUCCESS')
                    } catch (Exception e) {
                        updateGitHubCheck(name: 'Publish', status: 'COMPLETED', conclusion: 'FAILURE')
                        error("Publish stage failed: ${e.message}")
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    updateGitHubCheck(name: 'Deploy', status: 'IN_PROGRESS')
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
                        updateGitHubCheck(name: 'Deploy', status: 'COMPLETED', conclusion: 'SUCCESS')
                    } catch (Exception e) {
                        updateGitHubCheck(name: 'Deploy', status: 'COMPLETED', conclusion: 'FAILURE')
                        error("Deploy stage failed: ${e.message}")
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                updateGitHubCheck(name: 'Build', status: 'COMPLETED', conclusion: currentBuild.currentResult)
                updateGitHubCheck(name: 'Publish', status: 'COMPLETED', conclusion: currentBuild.currentResult)
                updateGitHubCheck(name: 'Deploy', status: 'COMPLETED', conclusion: currentBuild.currentResult)
            }
        }
    }
}

def createGitHubCheck(Map args) {
    githubCheck(
        name: args.name,
        title: "Jenkins ${args.name}",
        summary: "Running ${args.name} stage",
        status: args.status
    )
}

def updateGitHubCheck(Map args) {
    githubCheck(
        name: args.name,
        title: "Jenkins ${args.name}",
        summary: "${args.status == 'COMPLETED' ? (args.conclusion == 'SUCCESS' ? 'Successfully completed' : 'Failed') : 'Running'} ${args.name} stage",
        text: "Build ${env.BUILD_NUMBER}\n\nCheck console output at ${env.BUILD_URL} to view the results.",
        detailsURL: "${env.BUILD_URL}",
        status: args.status,
        conclusion: args.conclusion
    )
}
