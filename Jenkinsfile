pipeline{
    agent any

    triggers {
        githubPush()
    }

    environment{
        DOCKER_IMAGE = "dhinesh2001/full-stack-1"
        IMAGE_TAG = "${env.BUILD_NUMBER}"

    }

    stages{
        stage('Clean Workspace'){
            steps{ cleanWs()}
        }
    }

    stages{
        stage('Checkout Code'){
            steps{
                git branch : 'main', url: 'https://github.com/Yomi-coder/DevOps-CI-CD-Automation-Pipeline.git'
            }
        }
        stage('OWASP Dependency Check'){
            steps{ 
                dependencyCheck additionalArguments: '--scan ./' ,
                odcPublisher patern: '**/dependency-check-report.xml'}
        }
        stage('SonarQube Analysis'){
            steps{
                withSonarQubeEnv('sonarqube') {
                    sh 'sonar-scanner \
                        -Dsonar.projectKeys=full-stack-1 \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://localhost:9000 \
                        -Dsonar.login=squ_8cf442819d824a72acf72b49ff5e23d87ee8b1ff'
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
                withDockerRegistry(credentialsId: 'dockerhub-credentials') {
                    sh 'docker push ${DOCKER_IMAGE}:${IMAGE_TAG}'
                }
            }
        }
    }
}