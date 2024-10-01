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
        targetBranch: 'main'
      ],
      cancelQueued: true,
      abortRunning: false
    )
  }

  environment {
    BUILD_CONTEXT = "Jenkins: 1. Build"
    PUBLISH_CONTEXT = "Jenkins: 2. Publish"
    DEPLOY_CONTEXT = "Jenkins: 3. Deploy"
    PIPELINE_CONTEXT = "Jenkins: Pipeline"
    GIT_REPO = "cowlinmoo/IS212_ComeBeck"
    GITHUB_TOKEN = credentials('GITHUB_TOKEN')
  }

  stages {
    stage('Checkout SCM') {
      steps {
        script {
          def scmVars = checkout scm
          env.GIT_COMMIT = scmVars.GIT_COMMIT
        }
        githubNotify context: "Jenkins: Checkout", description: "Checked out source code", status: "SUCCESS", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
      }
    }

    stage('Build, Publish, and Deploy') {
      steps {
        withCredentials([
          string(credentialsId: 'ACR_NAME', variable: 'ACR_NAME'),
          string(credentialsId: 'ACR_PASSWORD', variable: 'ACR_PASSWORD'),
          string(credentialsId: 'ACR_USERNAME', variable: 'ACR_USERNAME'),
          string(credentialsId: 'TENANT_ID', variable: 'TENANT_ID'),
          string(credentialsId: 'CONTAINER_APP_NAME', variable: 'CONTAINER_APP_NAME'),
          string(credentialsId: 'RESOURCE_GROUP', variable: 'RESOURCE_GROUP'),
          string(credentialsId: 'IMAGE_NAME', variable: 'IMAGE_NAME')
        ]) {
          script {
            try {
              // Set initial pending status for all steps
              githubNotify context: "${env.BUILD_CONTEXT}", description: "Building Docker image", status: "PENDING", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
              githubNotify context: "${env.PUBLISH_CONTEXT}", description: "Publishing to ACR", status: "PENDING", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
              githubNotify context: "${env.DEPLOY_CONTEXT}", description: "Deploying to Azure", status: "PENDING", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"

              // Execute the shell script
              sh '''#!/bin/bash
set -e

echo "Deleting Old Docker resources..."
docker system prune -af

# Step 1: Build the Docker image
echo "Building Docker image..."
docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} .

# Step 2: Publish to Azure Container Registry
echo "Logging in to Azure Container Registry..."
echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin

echo "Pushing image to Azure Container Registry..."
docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}

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

echo "Script completed successfully."
'''
              // Update success status for all steps
              githubNotify context: "${env.BUILD_CONTEXT}", description: "Docker image built successfully", status: "SUCCESS", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
              githubNotify context: "${env.PUBLISH_CONTEXT}", description: "Image published to ACR successfully", status: "SUCCESS", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
              githubNotify context: "${env.DEPLOY_CONTEXT}", description: "Application deployed to Azure successfully", status: "SUCCESS", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
            } catch (Exception e) {
              // Update failure status for all steps
              githubNotify context: "${env.BUILD_CONTEXT}", description: "Build failed: ${e.message}", status: "FAILURE", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
              githubNotify context: "${env.PUBLISH_CONTEXT}", description: "Publish failed: ${e.message}", status: "FAILURE", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
              githubNotify context: "${env.DEPLOY_CONTEXT}", description: "Deploy failed: ${e.message}", status: "FAILURE", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
              error("Pipeline failed: ${e.message}")
            }
          }
        }
      }
    }
  }

  post {
    success {
      githubNotify context: "${env.PIPELINE_CONTEXT}", description: "All stages completed successfully", status: "SUCCESS", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
    }
    failure {
      githubNotify context: "${env.PIPELINE_CONTEXT}", description: "Pipeline failed", status: "FAILURE", account: 'cowlinmoo', repo: "${GIT_REPO}", token: "${GITHUB_TOKEN}", sha: "${env.GIT_COMMIT}"
    }
  }
}
