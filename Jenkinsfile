pipeline {
    agent any

    environment {
        PROJECT_DIR = "/home/akku/intern_python_proj"
        COMPOSE_FILE = "compose.yml"
    }

    stages {

        stage('Checkout (Optional)') {
            steps {
                echo "Using existing local project directory"
                // If you want GitHub instead, uncomment below:
                git 'https://github.com/AmalkumarG/todo_python.git'
            }
        }

        stage('Stop Existing Containers') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh 'docker compose -f ${COMPOSE_FILE} down || true'
                }
            }
        }

        stage('Build & Deploy') {
            steps {
                dir("${PROJECT_DIR}") {
                    sh 'docker compose -f ${COMPOSE_FILE} up -d --build'
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'docker ps'
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful! App should be running on port 8000"
        }
        failure {
            echo "❌ Deployment failed. Check logs using: docker logs <container>"
        }
    }
}
