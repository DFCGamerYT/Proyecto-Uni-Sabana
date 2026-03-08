pipeline {
    agent any
    environment {
        SNYK_TOKEN = credentials('SNYK_TOKEN') 
        SONAR_TOKEN = credentials('SONAR_TOKEN')
    }
    stages {
        stage('Ejecutar Tests y Coverage') {
            steps {
                script {
                    sh 'docker build -t fastapi-test:latest .'
                    sh 'docker run --name test-container fastapi-test:latest pytest --cov=. --cov-report=xml:coverage.xml'
                    sh 'docker cp test-container:/app/coverage.xml .'
                    sh 'docker rm test-container'
                    sh "sed -i 's|/app|/usr/src|g' coverage.xml"
                    sh "grep '/usr/src' coverage.xml"
                    sh "ls -la main.py"
                }
            }
        }
        stage('Calidad - SonarQube') {
            steps {
                script {
                    // 1. Limpieza preventiva
                    sh "docker rm -f sonar_data || true"
                    
                    // 2. Crear el contenedor de datos (Nota: es -v con un solo guion)
                    sh "docker create -v /usr/src --name sonar_data alpine"
                    
                    // 3. Copiar código y coverage al volumen
                    sh "docker cp . sonar_data:/usr/src"
                    
                    // 4. Ejecutar el scanner usando los volúmenes de 'sonar_data'
                    sh """
                        docker run --rm \
                        --volumes-from sonar_data \
                        -e SONAR_HOST_URL="http://172.17.0.1:9000" \
                        -e SONAR_TOKEN=${SONAR_TOKEN} \
                        sonarsource/sonar-scanner-cli \
                        -Dsonar.projectKey=FastAPI \
                        -Dsonar.sources=/usr/src \
                        -Dsonar.python.coverage.reportPaths=/usr/src/coverage.xml \
                        -Dsonar.projectBaseDir=/usr/src \
                        -Dsonar.scm.disabled=true
                    """
                    
                    // 5. Limpiar el contenedor temporal
                    sh "docker rm -f sonar_data"
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
                    // Usamos una imagen oficial de Snyk para escanear tu imagen local
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
        stage('Configurar Monitoreo (Prometheus & Grafana)') {
            steps {
                script {
                    sh 'docker stop prometheus grafana || true'
                    sh 'docker rm prometheus grafana || true'
                    
                    sh 'docker run -d --name prometheus -p 9090:9090 prom/prometheus'
                    sh 'docker cp ./prometheus.yml prometheus:/etc/prometheus/prometheus.yml'
                    sh 'docker restart prometheus'

                    sh 'docker run -d --name grafana -p 3000:3000 -v grafana-data:/var/lib/grafana grafana/grafana-oss'
                    
                    echo 'Infraestructura de Monitoreo Completa'
                    echo 'Prometheus: http://localhost:9090'
                    echo 'Grafana: http://localhost:3000'
                }
            }
        }
    }
}