# DevOps CI/CD Automation Pipeline (Jenkins)

This repository contains a Jenkins Pipeline that automates common CI/CD quality and security checks, builds a Docker image, and pushes it to Docker Hub.

> **Note:** This README documents how the pipeline is intended to work. If your goal is to trigger Jenkins from **GitHub webhooks**, you must also configure the **Jenkins job** (Build Triggers + SCM setup) in addition to the GitHub webhook settings.

---

## Pipeline Overview

The `Jenkinsfile` performs the following stages:

1. **Clean Workspace** (`cleanWs()`)
2. **Checkout Code** (`checkout scm`)
3. **OWASP Dependency Check**
   - Scans the repository (`additionalArguments: '--scan ./'`)
   - Generates report `dependency-check-report.xml`
4. **SonarQube Analysis**
   - Runs `sonar-scanner` with:
     - `sonar.projectKey=full-stack-1`
     - `sonar.sources=.`
     - `sonar.host.url=http://localhost:9000`
     - `sonar.login=<token>`
5. **Quality Gate**
   - Waits for SonarQube quality gate to pass
6. **Trivy Filesystem Scan**
   - Generates `trivy-report.txt`
7. **Docker Build**
   - Builds image: `${DOCKER_IMAGE}:${IMAGE_TAG}`
8. **Trivy Image Scan**
9. **Docker Push**
   - Pushes image to Docker Hub using `dockerhub-credentials`

---

## Prerequisites

### Jenkins Plugins
- **Pipeline** support
- **Pipeline SCM Step** (or standard Pipeline features)
- **SonarQube Scanner** / SonarQube integration plugin
- **Dependency-Check** plugin
- **Docker** pipeline integration (for `withDockerRegistry`)
- **Trivy** (usually CLI installed on the Jenkins agent)

### Jenkins Credentials / Config
- **SonarQube server** named: `sonarqube`
- **Docker registry credentials**:
  - `dockerhub-credentials`
- Ensure `trivy` and `docker` are installed on the Jenkins agent/node.

---

## Webhook Triggering (GitHub → Jenkins)

GitHub webhook deliveries can succeed (HTTP 200) while Jenkins still won’t start if the **Jenkins job trigger + SCM mapping** is not correct.

### Required Jenkins Job Setup
In your Jenkins **Pipeline job**:
1. Use **Pipeline script from SCM**
2. Configure SCM to point to this repository
3. In **Build Triggers**, enable the GitHub webhook trigger option provided by your Jenkins GitHub plugin (wording varies), often:
   - **GitHub hook trigger for GITScm polling**

### Required GitHub Webhook Setup
In GitHub → Settings → Webhooks:
- Set Payload URL to the Jenkins webhook URL (must match your Jenkins plugin/job endpoint)
- Ensure secret (if used) matches Jenkins plugin configuration
- Select event(s), e.g. **Push events**

---

## Security / Tooling Notes

- **Trivy** scans for vulnerabilities:
  - `trivy fs` for the workspace
  - `trivy image` for the built image
- **OWASP Dependency Check** stops the build on findings if configured by the plugin (`stopbuild:true`).

---

## Environment Variables

The `Jenkinsfile` uses:
- `DOCKER_IMAGE = "dhinesh2001/full-stack-1"`
- `IMAGE_TAG = "${env.BUILD_NUMBER}"`

If you want different images/tags, update these values or parameterize them.

---

## Running Locally (for debugging)

If you have the tools installed, you can mimic parts of the pipeline steps:
- `dependency-check --scan ./`
- `sonar-scanner ...`
- `trivy fs .`
- `docker build -t <image>:<tag> .`
- `trivy image <image>:<tag>`

---

## Files

- `Jenkinsfile` – Jenkins Pipeline definition
- `dependency-check-report.xml` – produced during OWASP Dependency Check
- `trivy-report.txt` – produced during Trivy filesystem scan

---

## Troubleshooting Webhooks

If GitHub delivery shows success but Jenkins doesn’t trigger reliably:
- Check Jenkins system log for webhook reception and payload matching
- Verify the job is the one mapped to that webhook event/repository
- Confirm Jenkins SCM URL matches the repo in the webhook payload
- Confirm secrets match (if a secret is configured)


