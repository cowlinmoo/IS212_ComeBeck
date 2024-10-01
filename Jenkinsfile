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
        GIT_COMMIT = sh(script: 'git rev-parse HEAD', returnStdout: true).trim()
    }

    stages {
        stage('Debug') {
            steps {
                script {
                    echo "DEBUG: GIT_COMMIT = ${env.GIT_COMMIT}"
                    echo "DEBUG: GITHUB_TOKEN is set: ${env.GITHUB_TOKEN != null}"
                    echo "DEBUG: JOB_NAME = ${env.JOB_NAME}"
                    echo "DEBUG: BUILD_NUMBER = ${env.BUILD_NUMBER}"
                    echo "DEBUG: JENKINS_URL = ${env.JENKINS_URL}"
                }
            }
        }

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
  withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
    def jenkinsUrl = "${env.JENKINS_URL}job/${env.JOB_NAME}/${env.BUILD_NUMBER}/"
    def repoUrl = "https://api.github.com/repos/cowlinmoo/IS212_ComeBeck/statuses/${env.GIT_COMMIT}"

    echo "Updating GitHub status:"
    echo "State: ${state}"
    echo "Description: ${description}"
    echo "Context: ${context}"

    def maxRetries = 3 // Maximum number of retries for rate limiting
    def retryDelay = 10 // Delay (seconds) between retries

    for (int i = 0; i < maxRetries; i++) {
      def curlCommand = """
        curl -v -H 'Authorization: token ${GITHUB_TOKEN}' \
          -X POST \
          -H 'Accept: application/vnd.github.v3+json' \
          ${repoUrl} \
          -d '{"state":"${state}","context":"${context}","description":"${description}","target_url":"${jenkinsUrl}"}'
      """

      def response = sh(script: curlCommand, returnStdout: true).trim()

      echo "Full GitHub API response:"
      echo response

      if (response.contains('"state":"${state}"')) {
        echo "GitHub status updated successfully"
        return // Exit the loop on successful update
      } else if (response.contains('429 Too Many Requests')) {
        echo "Rate limit exceeded. Retrying in ${retryDelay} seconds..."
        sleep(retryDelay * 1000) // Wait before retrying
      } else {
        error("Failed to update GitHub status. Response: ${response}")
        break // Exit the loop on non-retryable error
      }
    }
  }
}
