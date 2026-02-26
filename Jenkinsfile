pipeline {
    agent any
    
    tools {
        dockerTool 'docker-bin' 
    }

    environment {
        DOCKER_USER = 'acmeneses496'
        IMAGE_NAME = 'fastapi-app'
        IMAGE_TAG = 'latest'
        FULL_IMAGE_NAME = "${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
        SONAR_SERVER = 'sonarqube-server'
    }

    stages {
        stage('Checkout Git') {
            steps {
                checkout scm
            }
        }

        stage('SonarQube Analysis') {
            steps {

                withCredentials([usernamePassword(credentialsId: 'sonarqube-token', 
                                                passwordVariable: 'SONAR_TOKEN', 
                                                usernameVariable: 'SONAR_USER')]) {
                                withSonarQubeEnv('sonarqube-server') { 
                                                sh """
                                                    docker run --rm \
                                                    --network proyecto-uni-sabana_devops-network \
                                                    -e SONAR_HOST_URL=http://sonarqube-server:9000 \
                                                    -v \$(pwd):/usr/src \
                                                    sonarsource/sonar-scanner-cli \
                                                    -Dsonar.projectKey=fastapi-app-andres \
                                                    -Dsonar.sources=. \
                                                    -Dsonar.login=${SONAR_TOKEN}
                                                """
                                            }
                }
            }
        }

        stage('Crear Imagen Docker') {
            steps {
                sh "docker build -t ${FULL_IMAGE_NAME} ."
            }
        }

        stage('Push a Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', 
                                 usernameVariable: 'USER', 
                                 passwordVariable: 'PASS')]) {
                    sh "echo \$PASS | docker login -u \$USER --password-stdin"
                    sh "docker push ${FULL_IMAGE_NAME}"
                }
            }
        }

        stage('Desplegar') {
            steps {
                sh 'docker stop api-final || true'
                sh 'docker rm api-final || true'
                sh "docker run -d -p 8030:8000 --name api-final ${FULL_IMAGE_NAME}"
            }
        }
    }
}