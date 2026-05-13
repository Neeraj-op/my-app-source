pipeline {
    agent any

    environment {
        // Docker Hub credentials
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USERNAME = credentials('docker-hub-credentials')
        DOCKER_IMAGE = 'neeraj143/my-app'
        BUILD_TAG = "${BUILD_NUMBER}"
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

                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'

                bat '''
                    python -m pytest test_app.py -v --tb=short
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'

                bat '''
                    docker build -t %DOCKER_IMAGE%:%BUILD_TAG% .
                    docker tag %DOCKER_IMAGE%:%BUILD_TAG% %DOCKER_IMAGE%:latest
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'

                bat '''
                    docker login -u "%DOCKER_USERNAME_USR%" -p "%DOCKER_USERNAME_PSW%"
                    docker push %DOCKER_IMAGE%:%BUILD_TAG%
                    docker push %DOCKER_IMAGE%:latest
                    docker logout
                '''
            }
        }

        stage('Update Config Repository') {
            steps {
                echo 'Updating Kubernetes manifest with new image tag...'

                bat '''
                    REM Delete old repo if exists
                    if exist my-app-config-repo rmdir /s /q my-app-config-repo


                    REM Clone config repo
                    git clone https://github.com/Neeraj-op/my-app-config-repo.git

                    REM Go inside repo
                    cd my-app-config-repo

                    REM Pull latest changes
                    git pull origin mai

                    REM Update deployment.yaml image tag
                    powershell -Command "(Get-Content manifests/deployment.yaml) -replace 'image: .*','image: %DOCKER_IMAGE%:%BUILD_TAG%' | Set-Content manifests/deployment.yaml"

                    REM Configure Git
                    git config user.email "jenkins@example.com"
                    git config user.name "Jenkins CI"

                    REM Commit changes
                    git add manifests/deployment.yaml

                    git commit -m "Update image to %DOCKER_IMAGE%:%BUILD_TAG% (Build #%BUILD_NUMBER%)" || echo No changes to commit

                    REM Push changes
                    git push origin main
                '''
            }
        }
    }

    post {

        success {
            echo '✅ Pipeline succeeded!'
            echo "Docker image pushed: ${DOCKER_IMAGE}:${BUILD_TAG}"
        }

        failure {
            echo '❌ Pipeline failed!'
            echo 'Check logs above for details'
        }
    }
}