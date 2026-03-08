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
        stage('Preparar Manifiesto K8s') {
            steps {
                script {
                    // 1. Extraer el archivo desde la carpeta k8s de la imagen
                    sh 'docker create --name temp-k8s fastapi-test:latest'
                    sh 'docker cp temp-k8s:/app/k8s/deployment.yaml .'
                    sh 'docker rm temp-k8s'
                    
                    // 2. Validar que el archivo ya está en el workspace raíz
                    sh 'ls -la deployment.yaml'
        
                    // 3. Aplicar SED (como hiciste con el coverage)
                    // Esto asegura que el YAML use la imagen local que acabas de validar
                    sh "sed -i 's|image: .*|image: fastapi-app:latest|g' deployment.yaml"
                }
            }
        }
        stage('Despliegue - Kubernetes') {
            steps {
                script {
                    sh "ls -R ${WORKSPACE}"
                    sh """
                        cat deployment.yaml | docker run -i --rm \
                        --network host \
                        -v /var/jenkins_home/.kube:/config \
                        -e KUBECONFIG=/config/config_portable \
                        bitnami/kubectl:latest apply -f - --insecure-skip-tls-verify
                    """
                }
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