pipeline{
    agent any


    environment{
        DOCKER_IMAGE = "dhinesh2001/full-stack-1"
        IMAGE_TAG = "${env.BUILD_NUMBER}"

    }

    stages{

        stage('Clean Workspace'){
            steps{
                cleanWs()
            }
        }


        stage('Checkout Code'){
            steps{
                checkout scm
            }
        }
        
        stage('SonarQube Analysis'){
            steps{
                withSonarQubeEnv('sonarqube') {
                    def scannerHome = tool 'sonar-scanner'
                    sh '${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=full-stack-1 \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://localhost:9000'
                }
            }
        }

        stage('Quality Gate'){
            steps{
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Trivy Filesystem Scan'){
            steps{
                sh '''
                trivy fs . > trivy-report.txt
                '''
            }
        }

        stage('Docker Build'){
            steps { sh 'docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} .'}
        }

        stage('Trivy Scan'){
            steps { sh 'trivy image ${DOCKER_IMAGE}:${IMAGE_TAG}'}
        }
        
        stage('Docker Push'){
            steps {
                withDockerRegistry([credentialsId: 'dockerhub-credentials',
                url: 'https://index.docker.io/v1/']) {
                    sh "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                    }
            }
        }
    }
}