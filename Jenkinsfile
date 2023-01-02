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
                sh "cat Jenkinsfile"
                sh "git checkout master"
                sh "git pull --ff-only https//github.com/YYKlimenko/EMarketAPI.git"
                sh "cat Jenkinsfile"
                sh "git merge test"
                sh "cat Jenkinsfile"
                sh """git checkout master && git merge test && git push https://${GIT_TOKEN}@github.com/YYKlimenko/EMarketAPI.git"""
            }
        }
    }
}