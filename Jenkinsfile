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
  }

  stages {
    stage('Checkout SCM') {
      steps {
        checkout scm
        githubNotify context: "Jenkins: Checkout", description: "Checked out source code", status: "SUCCESS"
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
          script {
            try {
              // Set initial pending status for all steps
              githubNotify context: env.BUILD_CONTEXT, description: "Building Docker image", status: "PENDING"
              githubNotify context: env.PUBLISH_CONTEXT, description: "Publishing to ACR", status: "PENDING"
              githubNotify context: env.DEPLOY_CONTEXT, description: "Deploying to Azure", status: "PENDING"

              // Execute the shell script
              sh '''#!/bin/bash
set -e

echo "Deleting Old Docker resource..."
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
              githubNotify context: env.BUILD_CONTEXT, description: "Docker image built successfully", status: "SUCCESS"
              githubNotify context: env.PUBLISH_CONTEXT, description: "Image published to ACR successfully", status: "SUCCESS"
              githubNotify context: env.DEPLOY_CONTEXT, description: "Application deployed to Azure successfully", status: "SUCCESS"
            } catch (Exception e) {
              // Update failure status for all steps
              githubNotify context: env.BUILD_CONTEXT, description: "Build failed: ${e.message}", status: "FAILURE"
              githubNotify context: env.PUBLISH_CONTEXT, description: "Publish failed: ${e.message}", status: "FAILURE"
              githubNotify context: env.DEPLOY_CONTEXT, description: "Deploy failed: ${e.message}", status: "FAILURE"
              error("Pipeline failed: ${e.message}")
            }
          }
        }
      }
    }
  }

  post {
    success {
      githubNotify context: "Jenkins: Pipeline", description: "All stages completed successfully", status: "SUCCESS"
    }
    failure {
      githubNotify context: "Jenkins: Pipeline", description: "Pipeline failed", status: "FAILURE"
    }
  }
}
