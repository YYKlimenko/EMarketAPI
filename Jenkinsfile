pipeline {
    agent any

    stages {

        stage("Up docker-compose file") {
            steps {
                sh "cd docker && docker-compose up --build -d"
            }
        }

         stage("Test backend app") {
            steps {
                sh "docker exec -i docker_backend_1 sh -c 'python -m pytest .'"
            }
        }

        stage("Merge in master branch") {
            steps {
                sh "git log --oneline"
                sh "git branch -v"

                sh "git checkout master"
                sh "git merge test"

                sh """git push https://${GIT_TOKEN}@github.com/YYKlimenko/EMarketAPI.git"""
            }
        }
    }
}