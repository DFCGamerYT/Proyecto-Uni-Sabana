pipeline {
    agent any // ejecutar en cualquier agente disponible
    
    tools {
        dockerTool 'docker-bin' // instalación Docker en Jenkins
    }

    environment {
        DOCKER_USER = 'acmeneses496' // usuario Docker Hub
        IMAGE_NAME = 'fastapi-app' // nombre de la imagen
        IMAGE_TAG = 'latest' // tag por defecto
        FULL_IMAGE_NAME = "${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}" // nombre completo
        SONAR_SERVER = 'sonarqube-server' // nombre del servidor SonarQube en Jenkins
        DOCKER_NETWORK = 'proyecto-uni-sabana_devops-network' // red Docker usada
    }

    stages {
        stage('Checkout Git') {
            steps {
                checkout scm // clonar el repo/commit que disparó el job
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'sonarqube-token', 
                                                passwordVariable: 'SONAR_TOKEN', 
                                                usernameVariable: 'SONAR_USER')]) { // cargar credenciales
                    withSonarQubeEnv('sonarqube-server') { // configurar entorno Sonar
                        sh """
                            docker run --rm \
                            --network proyecto-uni-sabana_devops-network \ # usa la red del proyecto
                            -e SONAR_HOST_URL=http://sonarqube-server:9000 \ # URL interna de Sonar
                            -v proyecto-uni-sabana_jenkins_home:/var/jenkins_home \ # volumen Jenkins
                            sonarsource/sonar-scanner-cli \
                            -Dsonar.projectKey=fastapi-app-andres \
                            -Dsonar.sources=. -Dsonar.projectBaseDir=${WORKSPACE} \
                            -Dsonar.login=${SONAR_TOKEN} # token para autenticar
                        """
                    }
                }
            }
        }

        stage('Crear Imagen Docker') {
            steps {
                sh "docker build -t ${FULL_IMAGE_NAME} ." // construir imagen desde Dockerfile
            }
        }

        stage('Push a Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', 
                                                 usernameVariable: 'USER', 
                                                 passwordVariable: 'PASS')]) { // credenciales Docker Hub
                    sh "echo \$PASS | docker login -u \$USER --password-stdin || docker login -u \$USER -p \$PASS" // login seguro
                    sh "docker push ${FULL_IMAGE_NAME}" // subir imagen
                }
            }
        }

        stage('Desplegar') {
            steps {
                sh 'docker stop api-final || true' // detener si ya existe
                sh 'docker rm api-final || true' // eliminar contenedor previo
                sh "docker run -d --network ${DOCKER_NETWORK} -p 8030:8000 --name api-final ${FULL_IMAGE_NAME}" // ejecutar nuevo contenedor
            }
        }
    }
}