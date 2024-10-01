pipeline {
  agent any

  options {
    buildDiscarder(logRotator(daysToKeepStr: '60', numToKeepStr: '10'))
    disableConcurrentBuilds()
  }

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
        targetBranch: 'Jenkinspipeline'
      ],
      cancelQueued: true,
      abortRunning: false
    )
  }

  stages {
    stage('Set Initial Status') {
      steps {
        script {
          updateGitHubStatus('pending', 'Jenkins pipeline started', 'Jenkins: Overall')
        }
      }
    }

        stage('Checkout SCM') {
          steps {
            checkout([$class: 'GitSCM', 
                      branches: [[name: '*/Jenkinspipeline']],
                      userRemoteConfigs: [[url: 'https://github.com/cowlinmoo/IS212_ComeBeck.git']]])
          }
        }

    stage('Build, Publish, and Deploy') {
      steps {
        withCredentials([
          string(credentialsId: 'ACR_NAME', variable: 'ACR_NAME'),
          string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN'),
          string(credentialsId: 'ACR_PASSWORD', variable: 'ACR_PASSWORD'),
          string(credentialsId: 'ACR_USERNAME', variable: 'ACR_USERNAME'),
          string(credentialsId: 'TENANT_ID', variable: 'TENANT_ID')
        ]) {
          sh '''#!/bin/bash
set -e

update_github_status() {
    local state=$1
    local description=$2
    local context=$3

    # Construct the Jenkins build URL
    local jenkins_url="https://jenkins.comebeckwfhtracker.systems/job/comebeckjenkinspipeline/${BUILD_NUMBER}/"

    curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
         -X POST \
         -H "Accept: application/vnd.github.v3+json" \
         https://api.github.com/repos/cowlinmoo/IS212_ComeBeck/statuses/${GIT_COMMIT} \
         -d "{\\"state\\":\\"${state}\\",\\"context\\":\\"${context}\\",\\"description\\":\\"${description}\\",\\"target_url\\":\\"${jenkins_url}\\"}"
}

# Define the contexts
BUILD_CONTEXT="Jenkins: 1. Build"
PUBLISH_CONTEXT="Jenkins: 2. Publish"
DEPLOY_CONTEXT="Jenkins: 3. Deploy"

# Update initial status for all steps
update_github_status "pending" "Building Docker image" "${BUILD_CONTEXT}"
update_github_status "pending" "Publishing to ACR" "${PUBLISH_CONTEXT}"
update_github_status "pending" "Deploying to Azure" "${DEPLOY_CONTEXT}"

# Wrap the entire script in a try-catch block
{
    echo "Deleting Old Docker resources..."
    docker system prune -af

    # Step 1: Build the Docker image
    echo "Building Docker image..."
    docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} .
    update_github_status "success" "Docker image built successfully" "${BUILD_CONTEXT}"

    # Step 2: Publish to Azure Container Registry
    echo "Logging in to Azure Container Registry..."
    echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin

    echo "Pushing image to Azure Container Registry..."
    docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}
    update_github_status "success" "Image published to ACR successfully" "${PUBLISH_CONTEXT}"

    # Step 3: Deploy application to Azure Container Apps
    # Check if Azure CLI is installed
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
    update_github_status "success" "Application deployed to Azure successfully" "${DEPLOY_CONTEXT}"

    echo "Script completed successfully."

} || {
    # This block executes if any command in the try block fails
    failed_step=${FUNCNAME[1]:-UNKNOWN}
    update_github_status "failure" "Failed during: ${failed_step}" "${BUILD_CONTEXT}"
    update_github_status "failure" "Failed during: ${failed_step}" "${PUBLISH_CONTEXT}"
    update_github_status "failure" "Failed during: ${failed_step}" "${DEPLOY_CONTEXT}"
    echo "Script failed"
    exit 1
}'''
        }
      }
    }
  }

  post {
    success {
      script {
        updateGitHubStatus('success', 'Jenkins pipeline succeeded', 'Jenkins: Overall')
      }
    }
    failure {
      script {
        updateGitHubStatus('failure', 'Jenkins pipeline failed', 'Jenkins: Overall')
      }
    }
  }
}

def updateGitHubStatus(state, description, context) {
  withCredentials([string(credentialsId: 'GITHUB_TOKEN', variable: 'GITHUB_TOKEN')]) {
    sh """
      curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
           -X POST \
           -H "Accept: application/vnd.github.v3+json" \
           https://api.github.com/repos/cowlinmoo/IS212_ComeBeck/statuses/${GIT_COMMIT} \
           -d "{\\"state\\":\\"${state}\\",\\"context\\":\\"${context}\\",\\"description\\":\\"${description}\\",\\"target_url\\":\\"${BUILD_URL}\\"}"
    """
  }
}