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
    }

    stages {
        stage('Checkout Git') {
            steps {
                checkout scm
            }
        }

        stage('Crear Imagen') {
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

        stage('Limpiar Contenedor antiguo') {
            steps {

                sh 'docker stop api-final || true'
                sh 'docker rm api-final || true'
            }
        }

        stage('Desplegar en Puerto 8030') {
            steps {

                sh "docker run -d -p 8030:8000 --name api-final ${FULL_IMAGE_NAME}"
                echo "Despliegue completado con éxito"
                echo "Accede en: http://localhost:8030"
            }
        }
    }
}