pipeline {
    agent any
    environment {
        SONAR_TOKEN = credentials('SONAR_TOKEN_CRED')
    }
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
                sh '''
                docker run --name test-container fastapi-app:latest python -m pytest --cov=. --cov-report=xml:coverage.xml
                docker cp test-container:/app/coverage.xml .
                docker rm test-container
                '''
            }
        }
        stage('Verificar Reporte') {
            steps {
                sh 'pwd'
                sh 'ls -lh coverage.xml'
            }
        }
        stage('Análisis SonarQube') {
            steps {
                sh '''
                # Creamos la imagen que une el Scanner con tu código
                echo "FROM sonarsource/sonar-scanner-cli" > Dockerfile.sonar
                echo "COPY . /usr/src" >> Dockerfile.sonar
                
                docker build -t sonar-scanner-final -f Dockerfile.sonar .
                
                # Ejecutamos el análisis (sin volúmenes -v, todo está adentro)
                docker run --rm \
                    --network="host" \
                    sonar-scanner-final \
                    -Dsonar.projectKey=Proyecto-FastAPI-Sabana \
                    -Dsonar.sources=/usr/src \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.login=${SONAR_TOKEN} \
                    -Dsonar.python.coverage.reportPaths=/usr/src/coverage.xml \
                    -Dsonar.scm.disabled=true
                    
                # Limpieza
                docker rmi sonar-scanner-final
                rm Dockerfile.sonar
                '''
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
        stage('Despliegue K8s') {
            steps {
                sh '''
                /usr/local/bin/kubectl apply -f k8s/deployment.yaml
                /usr/local/bin/kubectl get pods
                '''
            }
        }
    }
}