pipeline {
    agent any

    stages {

        stage('Up docker-compose file') {
            steps {
                sh 'cd docker && docker-compose up --build -d'
            }
        }

         stage('Test') {
            steps {
                sh "docker exec -i docker_backend_1 sh -c 'python -m pytest .'"
            }
        }
    }
}