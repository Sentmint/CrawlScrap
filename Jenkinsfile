// Declarative //
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "${REDDIT_CLIENT_ID}"
                sh "python3 --version"
                sh "pip --version"
                sh "pip install praw"
                sh "pip install pip install python-dotenv"
                dir("reddit"){
                    sh "python3 reddit.py"
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'No deployment logic currently exists.'
            }
        }
    }
}