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
                sh "git pull --ff-only https://github.com/YYKlimenko/EMarketAPI.git master"
                sh """git checkout master && git merge test && git push https://${GIT_TOKEN}@github.com/YYKlimenko/EMarketAPI.git"""
            }
        }
    }
}