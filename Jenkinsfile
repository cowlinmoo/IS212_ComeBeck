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
    GITHUB_REPO = "cowlinmoo/IS212_ComeBeck"
  }

  stages {
    stage('Checkout SCM') {
      steps {
        script {
          def scmVars = checkout scm
          env.GIT_COMMIT = scmVars.GIT_COMMIT
          env.GIT_BRANCH = scmVars.GIT_BRANCH
        }
        githubNotify context: "Jenkins: Checkout", description: "Checked out source code", status: "SUCCESS", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
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
              githubNotify context: "${env.BUILD_CONTEXT}", description: "Building Docker image", status: "PENDING", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
              githubNotify context: "${env.PUBLISH_CONTEXT}", description: "Publishing to ACR", status: "PENDING", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
              githubNotify context: "${env.DEPLOY_CONTEXT}", description: "Deploying to Azure", status: "PENDING", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"

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
    
    # Azure CLI installation script
    sudo bash -c '
    set -e
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
    mkdir -p /etc/apt/keyrings
    curl -sLS https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/keyrings/microsoft.gpg
    chmod go+r /etc/apt/keyrings/microsoft.gpg
    CLI_REPO=$(lsb_release -cs)
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $CLI_REPO main" | tee /etc/apt/sources.list.d/azure-cli.list > /dev/null
    apt-get update
    apt-get install -y azure-cli
    '
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
              githubNotify context: "${env.BUILD_CONTEXT}", description: "Docker image built successfully", status: "SUCCESS", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
              githubNotify context: "${env.PUBLISH_CONTEXT}", description: "Image published to ACR successfully", status: "SUCCESS", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
              githubNotify context: "${env.DEPLOY_CONTEXT}", description: "Application deployed to Azure successfully", status: "SUCCESS", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
            } catch (Exception e) {
              // Update failure status for all steps
              githubNotify context: "${env.BUILD_CONTEXT}", description: "Build failed: ${e.message}", status: "FAILURE", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
              githubNotify context: "${env.PUBLISH_CONTEXT}", description: "Publish failed: ${e.message}", status: "FAILURE", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
              githubNotify context: "${env.DEPLOY_CONTEXT}", description: "Deploy failed: ${e.message}", status: "FAILURE", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
              error("Pipeline failed: ${e.message}")
            }
          }
        }
      }
    }
  }

  post {
    success {
      githubNotify context: "${env.PIPELINE_CONTEXT}", description: "All stages completed successfully", status: "SUCCESS", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
    }
    failure {
      githubNotify context: "${env.PIPELINE_CONTEXT}", description: "Pipeline failed", status: "FAILURE", credentialsId: 'githubpat', sha: "${env.GIT_COMMIT}", account: "${GITHUB_REPO.split('/')[0]}", repo: "${GITHUB_REPO.split('/')[1]}", targetUrl: "${env.BUILD_URL}"
    }
  }
}
