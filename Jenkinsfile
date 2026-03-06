pipeline {
    agent any
    environment {
        SNYK_TOKEN = credentials('SNYK_TOKEN') 
        SONAR_TOKEN = credentials('SONAR_TOKEN')
    }
    stages {
        stage('Checkout Git') {
            steps {
                git branch: 'master', url: 'https://github.com/DFCGamerYT/Proyecto-Uni-Sabana.git'
            }
        }
        stage('Calidad - SonarQube') {
            steps {
                script {
                    sh """
                        docker run --rm \
                        -e SONAR_HOST_URL="http://172.17.0.1:9000" \
                        -e SONAR_TOKEN=${SONAR_TOKEN} \
                        -v \$(pwd):/usr/src \
                        sonarsource/sonar-scanner-cli \
                        -Dsonar.projectKey=Proyecto-FastAPI \
                        -Dsonar.sources=.
                    """
                }
            }
        }
        stage('Crear Imagen'){
            steps{
                sh 'docker build -t fastapi-app:latest .'
            }
        }
        stage('Seguridad - Snyk Scan') {
            steps {
                script {
                    sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        -e SNYK_TOKEN=${SNYK_TOKEN} \
                        snyk/snyk:docker snyk container test fastapi-app:latest --severity-threshold=high"
                }
            }
        }
        stage('Limpiar Imagen antigua'){
            steps{
                sh 'docker stop api-final || true'
                sh 'docker rm api-final || true'
            }
        }
        stage('Desplegar Imagen'){
            steps{
                sh 'docker run -d -p 8000:8000 --name api-final fastapi-app:latest'
                echo 'Despliegue completado en http://localhost:8000'
            }
        }
    }
}