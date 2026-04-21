pipeline {
    agent { label 'node1' }

    environment {
        PROJECT_DIR = "/home/$USER/intern_python_proj"
        COMPOSE_FILE = "compose.yml"
    }

    stages {

        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/AmalkumarG/todo_python.git'
            }
        }

        stage('Deploy') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh '''
                    docker compose -f ${COMPOSE_FILE} down || true
                    docker compose -f ${COMPOSE_FILE} up -d --build
                    '''
                }
            }
        }

        stage('Verify') {
            steps {
                sh 'docker ps'
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful"
        }
        failure {
            echo "❌ Deployment failed"
        }
    }
}
