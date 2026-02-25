pipeline {
    agent any
    stages {
        stage('Checkout Git'){
            steps{
                checkout scm
            }
        }
        stage('Crear Imagen'){
            steps{
                sh 'docker build -t fastapi-app:latest .'
            }
        }
        stage('Probar Imagen'){
            steps{
                sh 'docker run --rm fastapi-app:latest pytest'
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