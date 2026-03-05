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
        stage('Pruebas y Cobertura') {
            steps {
                sh 'docker run --rm -v $(pwd):/app fastapi-app:latest python -m pytest --cov=. --cov-report=xml:/app/coverage.xml'
            }
        }
        stage('Análisis SonarQube') {
            steps {
                sh """
                docker run --rm \
                    --network="host" \
                    -v "\$(pwd):/usr/src" \
                    sonarsource/sonar-scanner-cli \
                    -Dsonar.projectKey=Proyecto-FastAPI-Sabana \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.login=squ_3549ff877e749663370e5f37693244622cf31901 \
                    -Dsonar.python.coverage.reportPaths=coverage.xml
                """
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