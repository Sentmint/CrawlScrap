// Declarative //
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo "Installing scraper dependencies"
                sh "python3 --version"
                sh "pip --version"
                sh "pip install python-dotenv"
                sh "pip install praw"
                sh "pip install selenium"
                sh "pip install webdriver_manager"
                sh "pip install chromedriver"
            }
        }
        stage('Test') {
            steps {
                //Running a loop of Reddit scraper
                dir("reddit"){
                    echo "Test case for Reddit Scraper being run"
                    sh "python3 reddit_test.py"
                }
                //Running a loop of Twitter scraper
                dir("twitter"){
                    echo "Test case for Twitter Scraper being run"
                    sh "python3 selenium_twitter_scraper.py"
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'No deployment logic currently exists.'
            }
        }
    }
}