pipeline {
    agent any

    environment {
        HOME = tool 'sonar-scanner'
        IMAGE_NAME = 'samplepython'
        CONTAINER_NAME = 'samplecontainer'
        TRIVY_REPORT_DIR = 'trivy_reports'
        TRIVY_HTML_REPORT = 'trivy_report.html'
        TRIVY_JSON_REPORT = 'trivy_output.json'
        TRIVY_TEMPLATE_URL = 'https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/html.tpl'
    }

    stages {
        stage('Git Checkout') {
            steps {
                git credentialsId: 'github', url: 'https://github.com/Nihal0324/sample-python-app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh "pip install -r requirements.txt"
            }
        }

        stage("Dependency Check OWASP") {
            steps {
                dependencyCheck additionalArguments: '--scan requirements.txt --format HTML', odcInstallation: 'DC'
            }
        }

        stage('Publish Dependency Report') {
            steps {
                dependencyCheckPublisher pattern: '**/dependency-check-report.html'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                        docker stop $CONTAINER_NAME || true
                        docker rm $CONTAINER_NAME || true
                        docker build -t $IMAGE_NAME .
                    '''
                }
            }
        }


        stage('Publish Trivy Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: "$TRIVY_REPORT_DIR",
                    reportFiles: "$TRIVY_HTML_REPORT",
                    reportName: 'Trivy Vulnerability Report'
                ])
            }
        }

        stage('Trivy Vulnerability Trend') {
            steps {
                recordIssues(tools: [trivy(pattern: "$TRIVY_REPORT_DIR/$TRIVY_JSON_REPORT")])
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker run -d --user root --name $CONTAINER_NAME -p 5001:5001 $IMAGE_NAME
                '''
            }
        }
    }

   
}
