import io.jsonwebtoken.Jwts
import io.jsonwebtoken.SignatureAlgorithm
import java.security.KeyFactory
import java.security.spec.PKCS8EncodedKeySpec
import java.util.Base64
import java.util.Date

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
        GITHUB_APP_ID = credentials('GITHUB_APP_ID')
        GITHUB_PRIVATE_KEY = credentials('GITHUB_PRIVATE_KEY')
    }

    stages {
        stage('Build') {
            steps {
                script {
                    def checkId = createGitHubCheck('Jenkins: Build', 'Building Docker image')

                    try {
                        sh "docker build -t ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER} ."
                        completeGitHubCheck(checkId, 'success', 'Docker image built successfully')
                    } catch (Exception e) {
                        completeGitHubCheck(checkId, 'failure', 'Docker image build failed')
                        throw e
                    }
                }
            }
        }

        stage('Publish') {
            steps {
                script {
                    def checkId = createGitHubCheck('Jenkins: Publish', 'Publishing to ACR')

                    try {
                        sh "echo ${ACR_PASSWORD} | docker login ${ACR_NAME}.azurecr.io -u ${ACR_USERNAME} --password-stdin"
                        sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${BUILD_NUMBER}"
                        completeGitHubCheck(checkId, 'success', 'Image published to ACR successfully')
                    } catch (Exception e) {
                        completeGitHubCheck(checkId, 'failure', 'Image publish failed')
                        throw e
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def checkId = createGitHubCheck('Jenkins: Deploy', 'Deploying to Azure')

                    try {
                        sh '''
                            if ! command -v az &> /dev/null
                            then
                                curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
                            fi

                            az login --service-principal -u $ACR_USERNAME -p $ACR_PASSWORD --tenant $TENANT_ID
                            az containerapp update \
                              --name $CONTAINER_APP_NAME \
                              --resource-group $RESOURCE_GROUP \
                              --image $ACR_NAME.azurecr.io/$IMAGE_NAME:$BUILD_NUMBER
                            az logout
                        '''
                        completeGitHubCheck(checkId, 'success', 'Application deployed to Azure successfully')
                    } catch (Exception e) {
                        completeGitHubCheck(checkId, 'failure', 'Deployment failed')
                        throw e
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                def buildStatus = currentBuild.result ?: 'SUCCESS'
                def description = "Pipeline finished with result: ${buildStatus}"
                // Optionally update final check status
            }
        }
    }
}

def createGitHubCheck(String name, String description) {
    def jwt = generateJWT()
    def response = sh(script: """
        curl -s -X POST \
        -H "Authorization: Bearer ${jwt}" \
        -H "Accept: application/vnd.github+json" \
        https://api.github.com/repos/cowlinmoo/IS212_ComeBeck/check-runs \
        -d '{
            "name": "${name}",
            "head_sha": "${GIT_COMMIT}",
            "status": "in_progress",
            "external_id": "${env.BUILD_ID}",
            "started_at": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'", TimeZone.getTimeZone('UTC'))}",
            "output": {
                "title": "${name}",
                "summary": "${description}"
            }
        }'
    """, returnStdout: true)

    def jsonResponse = readJSON(text: response)
    return jsonResponse.id
}

def completeGitHubCheck(int checkId, String conclusion, String description) {
    def jwt = generateJWT()
    sh """
        curl -s -X PATCH \
        -H "Authorization: Bearer ${jwt}" \
        -H "Accept: application/vnd.github+json" \
        https://api.github.com/repos/cowlinmoo/IS212_ComeBeck/check-runs/${checkId} \
        -d '{
            "status": "completed",
            "completed_at": "${new Date().format("yyyy-MM-dd'T'HH:mm:ss'Z'", TimeZone.getTimeZone('UTC'))}",
            "conclusion": "${conclusion}",
            "output": {
                "title": "${conclusion.capitalize()}",
                "summary": "${description}"
            }
        }'
    """
}

def generateJWT() {
    def now = System.currentTimeMillis()
    def exp = now + 1200000 // 20 minutes expiration

    def privateKey = GITHUB_PRIVATE_KEY
    def keySpec = new PKCS8EncodedKeySpec(Base64.getDecoder().decode(privateKey
        .replace("-----BEGIN PRIVATE KEY-----", "")
        .replace("-----END PRIVATE KEY-----", "")
        .replaceAll("\\s", "")))
    def keyFactory = KeyFactory.getInstance("RSA")
    def key = keyFactory.generatePrivate(keySpec)

    return Jwts.builder()
        .setIssuer(GITHUB_APP_ID)
        .setIssuedAt(new Date(now))
        .setExpiration(new Date(exp))
        .signWith(SignatureAlgorithm.RS256, key)
        .compact()
}
