
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out API Tester CLI repository...'
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'

                bat 'py -3 -m venv venv'

                bat 'venv\\Scripts\\python -m pip install --upgrade pip'

                bat 'venv\\Scripts\\python -m pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                echo 'Running Python unit tests...'

                bat 'venv\\Scripts\\python -m unittest discover -s tests -v'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: All API Tester CLI tests passed!'
        }

        failure {
            echo 'FAILURE: One or more pipeline stages failed.'
        }

        always {
            echo 'Jenkins pipeline execution completed.'
        }
    }
}
