pipeline {
    agent any
    stages {
        stage('Checkout'){
            steps{
                checkout scm
            }
        }
        stage('Build Image'){
            steps{
                sh 'docker build -t fastapi-app:latest .'
            }
        }
        stage('Test Image'){
            steps{
                sh 'docker run --rm fastapi-app:latest pytest'
            }
        }
    }
}