pipeline {
    agent any
    environment {
        // Sustituye 'tu_usuario' por tu nombre real de Docker Hub
        DOCKER_USER = 'tu_usuario'
        IMAGE_NAME = 'fastapi-app'
        REPO_NAME = "${DOCKER_USER}/${IMAGE_NAME}"
    }
    stages {
        stage('Checkout Git'){
            steps {
                checkout scm
            }
        }
        stage('Crear Imagen'){
            steps {
                sh "docker build -t ${REPO_NAME}:latest ."
            }
        }
        stage('Probar Imagen'){
            steps {
                sh "docker run --rm ${REPO_NAME}:latest pytest"
            }
        }
        stage('Push a Docker Hub'){
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', 
                                                 passwordVariable: 'DOCKER_HUB_PASSWORD', 
                                                 usernameVariable: 'DOCKER_HUB_USER')]) {
                    sh "echo \$DOCKER_HUB_PASSWORD | docker login -u \$DOCKER_HUB_USER --password-stdin"
                    sh "docker push ${REPO_NAME}:latest"
                }
            }
        }
        stage('Limpiar Imagen antigua'){
            steps {
                sh 'docker stop api-final || true'
                sh 'docker rm api-final || true'
            }
        }
        stage('Desplegar Imagen Local'){
            steps {
                sh "docker run -d -p 8000:8000 --name api-final ${REPO_NAME}:latest"
                echo 'Despliegue completado en http://localhost:8000'
            }
        }
    }
}