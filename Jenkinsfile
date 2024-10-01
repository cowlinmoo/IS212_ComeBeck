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
                githubChecks(context: env.BUILD_CONTEXT, status: 'PENDING')
                sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
            post {
                success {
                    githubChecks(context: env.BUILD_CONTEXT, status: 'SUCCESS')
                }
                failure {
                    githubChecks(context: env.BUILD_CONTEXT, status: 'FAILURE')
                }
            }
        }

        stage('Publish') {
            steps {
                githubChecks(context: env.PUBLISH_CONTEXT, status: 'PENDING')
                sh "echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin"
                sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}"
            }
            post {
                success {
                    githubChecks(context: env.PUBLISH_CONTEXT, status: 'SUCCESS')
                }
                failure {
                    githubChecks(context: env.PUBLISH_CONTEXT, status: 'FAILURE')
                }
            }
        }

        stage('Deploy') {
            steps {
                githubChecks(context: env.DEPLOY_CONTEXT, status: 'PENDING')
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
            post {
                success {
                    githubChecks(context: env.DEPLOY_CONTEXT, status: 'SUCCESS')
                }
                failure {
                    githubChecks(context: env.DEPLOY_CONTEXT, status: 'FAILURE')
                }
            }
        }
    }

    post {
        always {
            githubChecks(context: 'Jenkins: Pipeline', conclusion: currentBuild.resultIsBetterOrEqualTo('SUCCESS') ? 'SUCCESS' : 'FAILURE')
        }
    }
}
