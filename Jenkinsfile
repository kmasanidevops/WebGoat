pipeline {
   agent any

   tools {
      // Install the Maven version configured as "M3" and add it to the path.
      maven "M3"
   }

   stages {
      stage('Build') {
         steps {
            // Get some code from a GitHub repository
            git 'https://github.com/kiransre/WebGoat.git'

            // Run Maven on a Unix agent.
            sh "cd $WORKSPACE/webgoat-server"
            //sh "mvn -Dmaven.test.failure.ignore=true clean package"
            sh "mvn -Dmaven.test.failure.ignore=true clean compile"
         
            // To run Maven on a Windows agent, use
            // bat "mvn -Dmaven.test.failure.ignore=true clean package"
         }
      }
      stage('Scans: Master') {
         when { branch 'master' }
         steps {
            parallel(
               SonarQube: {
                  // sh "mvn sonar:sonar"
                  echo "Getting the analysis results .. "
                  // sh "/Users/kiran/anaconda3/bin/python3 /Users/kiran/parse_sonar.py --path $WORKSPACE/target/sonar/report-task.txt"
               },
               NexusLifeCycle: {
                  sh "echo 'hello world'"
               }
            )
         }
      }

      stage('Scans: Dev') {
         when { not { branch 'master' } }
         steps {
            // sh "mvn sonar:sonar"
            echo "Getting the analysis results .. "
            // sh "/usr/bin/python /opt/devops/scripts/parse_sonar.py --path $WORKSPACE/target/sonar/report-task.txt"
         }
      }

      stage('Nexus Repo') {
         steps {
            sh "echo 'HELLO WORLD'"
         }
      }

      stage('Docker Build') {
         steps {
            sh "echo 'Running Docker build ..' "
            script {
              SHORT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
              DOCKER_RELEASE_TAG = "MYAPP-${SHORT_HASH}"
            }
            echo "DOCKER_RELEASE_TAG:  $DOCKER_RELEASE_TAG"
            sh "cd $WORKSPACE/webgoat-flaskapp && /usr/bin/docker build -t kmasani/myapp:${DOCKER_RELEASE_TAG} ."
         }
      }

      stage('Container Scan') {

         steps {
            sh "echo 'Running Container scan .. ' "
            // sh "cd $WORKSPACE && /opt/devops/tools/inline_scan-v0.6.0 scan -r kmasani/myapp:${DOCKER_RELEASE_TAG}"
            // sh "/usr/bin/python /opt/devops/scripts/parse_anchore_analysis.py --outfile $WORKSPACE/anchore-reports/webgoat-local_latest-vuln.json"

            sh "echo 'Pushing Docker .. ' "
            sh "docker push kmasani/myapp:${DOCKER_RELEASE_TAG}"
         }
      }

      stage('Deploy: DEV') {
         steps {
            sh "echo 'Deploying Docker ..' "
            sh "/usr/bin/python /opt/devops/scripts/deploy_runner.py ${DOCKER_RELEASE_TAG}"
         }
      }      

   }
}
