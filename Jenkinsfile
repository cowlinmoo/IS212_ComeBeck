pipeline {
    agent any

    triggers {
        githubPullRequests(
            spec: '',
            triggerMode: 'HEAVY_HOOKS',
            events: [
                [
                    $class: 'org.jenkinsci.plugins.github.pullrequest.events.impl.GitHubPROpenEvent'
                ],
                [
                    $class: 'org.jenkinsci.plugins.github.pullrequest.events.impl.GitHubPRCommitEvent'
                ]
            ],
            preStatus: true,
            branchRestriction: [
                targetBranch: 'main'
            ],
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
    }

    stages {
        stage('Initialize') {
            steps {
                script {
                    env.BUILD_CONTEXT = "Jenkins: 1. Build"
                    env.PUBLISH_CONTEXT = "Jenkins: 2. Publish"
                    env.DEPLOY_CONTEXT = "Jenkins: 3. Deploy"
                    
                    updateGithubStatus('pending', 'Building Docker image', env.BUILD_CONTEXT)
                    updateGithubStatus('pending', 'Publishing to ACR', env.PUBLISH_CONTEXT)
                    updateGithubStatus('pending', 'Deploying to Azure', env.DEPLOY_CONTEXT)
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    try {
                        sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        updateGithubStatus('success', 'Docker image built successfully', env.BUILD_CONTEXT)
                    } catch (Exception e) {
                        updateGithubStatus('failure', "Failed during: Build", env.BUILD_CONTEXT)
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
                        updateGithubStatus('success', 'Image published to ACR successfully', env.PUBLISH_CONTEXT)
                    } catch (Exception e) {
                        updateGithubStatus('failure', "Failed during: Publish", env.PUBLISH_CONTEXT)
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
                                curl -sL https://aka.ms/InstallAzureCLIDeb | bash
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
                        updateGithubStatus('success', 'Application deployed to Azure successfully', env.DEPLOY_CONTEXT)
                    } catch (Exception e) {
                        updateGithubStatus('failure', "Failed during: Deploy", env.DEPLOY_CONTEXT)
                        error("Deploy stage failed: ${e.message}")
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully"
        }
        failure {
            echo "Pipeline failed"
        }
        always {
            echo "Cleaning up and printing debug information"
            script {
                sh "env | sort"
                echo "GIT_COMMIT: ${env.GIT_COMMIT}"
                echo "GITHUB_TOKEN: ${env.GITHUB_TOKEN != null ? 'Set' : 'Not Set'}"
            }
        }
    }
}

def updateGithubStatus(state, description, context) {
    script {
        def jenkinsUrl = "${env.JENKINS_URL}job/${env.JOB_NAME}/${env.BUILD_NUMBER}/"
        def repoUrl = "https://api.github.com/repos/cowlinmoo/IS212_ComeBeck/statuses/${env.GIT_COMMIT}"
        
        echo "Updating GitHub status:"
        echo "State: ${state}"
        echo "Description: ${description}"
        echo "Context: ${context}"
        echo "Jenkins URL: ${jenkinsUrl}"
        echo "Repo URL: ${repoUrl}"
        
        try {
            def curlCommand = """
                curl -v -s -w "\\n%{http_code}" -H "Authorization: token ${GITHUB_TOKEN}" \
                     -X POST \
                     -H "Accept: application/vnd.github.v3+json" \
                     ${repoUrl} \
                     -d '{"state":"${state}","context":"${context}","description":"${description}","target_url":"${jenkinsUrl}"}'
            """
            echo "Executing curl command (token masked):"
            echo curlCommand.replaceAll(GITHUB_TOKEN, "****")
            
            def response = sh(script: curlCommand, returnStdout: true).trim()

            echo "Full curl response: ${response}"

            def (body, statusCode) = response.tokenize('\n')
            echo "GitHub API response code: ${statusCode}"
            echo "GitHub API response body: ${body}"

            if (statusCode.toInteger() != 201) {
                error("Failed to update GitHub status. Status code: ${statusCode}, Body: ${body}")
            }
        } catch (Exception e) {
            echo "Error updating GitHub status: ${e.message}"
            error("Failed to update GitHub status: ${e.message}")
        }
    }
}
