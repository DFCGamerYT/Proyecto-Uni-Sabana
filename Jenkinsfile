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
        stage('Debug de Montaje') {
            steps {
                echo "--- Verificando qué ve Docker en el Workspace ---"
                sh 'ls -la ${WORKSPACE}'
                
                echo "--- Verificando qué verá el contenedor de Sonar ---"
                sh 'docker run --rm -v "${WORKSPACE}:/data" alpine ls -R /data'
            }
        }
        stage('Análisis SonarQube') {
            steps {
                sh '''
                docker run --rm \
                    --network="host" \
                    -v "/var/jenkins_home/workspace/Proyecto-FastAPI-CD:/usr/src" \
                    sonarsource/sonar-scanner-cli \
                    -Dsonar.projectKey=Proyecto-FastAPI-Sabana \
                    -Dsonar.sources=/usr/src \
                    -Dsonar.projectBaseDir=/usr/src \
                    -Dsonar.host.url=http://localhost:9000 \
                    -Dsonar.login=squ_e150174ee6b2aebb50d51ce4e67b9715d2193cd2 \
                    -Dsonar.python.coverage.reportPaths=/usr/src/coverage.xml \
                    -Dsonar.scm.disabled=true
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
    }
}