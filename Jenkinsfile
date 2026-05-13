pipeline {
    agent any

    environment {
        // Docker Hub credentials
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USERNAME = credentials('docker-hub-credentials')
        DOCKER_IMAGE = 'neeraj143/my-app'
        BUILD_TAG = "\${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    pytest test_app.py -v --tb=short
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t \${DOCKER_IMAGE}:\${BUILD_TAG} .
                    docker tag \${DOCKER_IMAGE}:\${BUILD_TAG} \${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                sh '''
                    echo "\${DOCKER_USERNAME_PSW}" | docker login -u "\${DOCKER_USERNAME_USR}" --password-stdin
                    docker push \${DOCKER_IMAGE}:\${BUILD_TAG}
                    docker push \${DOCKER_IMAGE}:latest
                    docker logout
                '''
            }
        }

        stage('Update Config Repository') {
            steps {
                echo 'Updating Kubernetes manifest with new image tag...'
                sh '''
                    # Clone the config repository
                    rm -rf config-repo || true
                    git clone https://github.com/Neeraj-op/my-app-config-repo
                    
                    # Update deployment.yaml with new image tag
                    cd config-repo
                    sed -i "s|image: .*|image: \${DOCKER_IMAGE}:\${BUILD_TAG}|g" manifests/deployment.yaml
                    
                    # Configure git
                    git config user.email "jenkins@example.com"
                    git config user.name "Jenkins CI"
                    
                    # Commit and push
                    git add manifests/deployment.yaml
                    git commit -m "Update image to \${DOCKER_IMAGE}:\${BUILD_TAG} (Build #\${BUILD_NUMBER})"
                    git push origin main || git push origin master
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded!'
            echo "Docker image pushed: \${DOCKER_IMAGE}:\${BUILD_TAG}"
        }
        failure {
            echo '❌ Pipeline failed!'
            echo 'Check logs above for details'
        }
    }
}