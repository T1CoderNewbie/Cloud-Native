# Demo Video Script

Use this script for a video of about 20-22 minutes. You do not need to read every line word-for-word, but this gives you a safe English structure that matches the current repository and the live deployment.

## Video Goal

By the end of the recording, the marker should clearly see that:

- the project has local development support
- the project is containerised
- the project has Kubernetes and Istio YAML
- the application has real functionality
- the service structure is modular and explainable
- the AWS architecture is real and working
- the public deployment is accessible through the live domain

## Suggested Duration

- Total target: 20 to 22 minutes
- If you speak a little slowly and explain while showing code, this script is long enough

## 0:00 - 1:00 Opening

### What to show

- GitHub repository home page
- Repository name
- README top section

### What to say

"Hello, in this video I will demonstrate my cloud-native application called Cloud Notes App. This project was developed for the Developing for the Cloud assignment. In this demonstration, I will explain the application from local development, containerisation, Kubernetes YAML configuration, core functionality, service architecture, and AWS deployment architecture. I will also show the live production deployment running on AWS through my public domain."

## 1:00 - 2:30 Repository Overview

### What to show

- Repository root
- Folders: `app`, `k8s`, `terraform`, `scripts`, `docs`, `tests`

### What to say

"This is the public GitHub repository for the project. The code is organised into clear sections. The `app` folder contains the Flask application code. The `k8s` folder contains Kubernetes and Istio YAML files. The `terraform` folder contains the infrastructure-as-code files for AWS. The `scripts` folder contains helper scripts for deployment and secret creation. The `tests` folder contains automated tests. The `docs` folder contains the architecture diagram and reporting support files."

## 2:30 - 4:30 Local Development

### What to show

- [main.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/main.py)
- [app/config.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/app/config.py)
- [app/models/db.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/app/models/db.py)
- [README.md](/Users/khanhbao/Desktop/Cloud%20Native%20App/README.md) local setup section

### What to say

"I will start with local development. The application entry point is `main.py`. This file creates the Flask application, loads environment variables, initialises the database, and registers the route blueprints for health checks, notes management, and file upload."

"The configuration is separated into `app/config.py`, where the application reads environment variables such as the environment name, port, database URL, Redis URL, Kafka bootstrap servers, AWS region, and S3 bucket settings."

"The database layer is implemented in `app/models/db.py`. This file defines the `notes` table using SQLAlchemy and supports both SQLite for local development and PostgreSQL for cloud deployment. If no external database URL is provided, the project uses a local SQLite file. This gives the project a simple local development experience while still supporting a production database in AWS."

"This means the same application can be developed locally first and then moved to cloud infrastructure later, which is one of the main goals of the assignment."

## 4:30 - 6:30 Container Code

### What to show

- [Dockerfile](/Users/khanhbao/Desktop/Cloud%20Native%20App/Dockerfile)
- [docker-compose.yml](/Users/khanhbao/Desktop/Cloud%20Native%20App/docker-compose.yml)

### What to say

"Next, I will show the containerisation layer. The `Dockerfile` builds the application from a Python 3.12 slim image. It sets a working directory, installs dependencies from `requirements.txt`, copies the source code, exposes port 5000, defines a health check, and starts the application with Gunicorn. This is important because it makes the runtime consistent between local development, CI, and cloud deployment."

"For local multi-service development, I use `docker-compose.yml`. This file defines the application container together with PostgreSQL, Redis, and Kafka containers. The app container is configured to connect to those services through environment variables. This setup makes local development much closer to the cloud environment, because the application can already interact with a relational database, a cache, and an event streaming component."

"So in summary, the project supports two local modes: a simple local mode with SQLite, and a more complete container-based mode using Docker Compose."

## 6:30 - 10:30 Functionality and Service Deep Dive

### What to show

- [app/routes/notes.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/app/routes/notes.py)
- [app/routes/health.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/app/routes/health.py)
- [app/routes/upload.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/app/routes/upload.py)
- [app/services/notes_service.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/app/services/notes_service.py)
- [app/services/cache_service.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/app/services/cache_service.py)
- [app/services/event_service.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/app/services/event_service.py)
- [app/services/s3_service.py](/Users/khanhbao/Desktop/Cloud%20Native%20App/app/services/s3_service.py)

### What to say

"The main business functionality is implemented through Flask routes and service modules. In `app/routes/notes.py`, the application supports creating notes, listing notes, searching notes, limiting results, exporting notes as JSON, viewing note statistics, showing recent notes, updating notes, and deleting notes. Input validation is also handled here, for example title length and content length limits."

"In `app/routes/health.py`, the application exposes cloud-friendly health endpoints. The `/health/live` endpoint checks whether the application is alive. The `/health/ready` endpoint checks whether important dependencies such as the database and Redis are ready. The `/health/summary` endpoint combines readiness information with note count information. These endpoints are important both for Kubernetes probes and for production monitoring."

"In `app/routes/upload.py`, the application supports file upload to Amazon S3. This allows the project to demonstrate object storage integration in addition to note CRUD functionality."

"The route files stay relatively thin because the actual business logic is pushed into the service layer. In `app/services/notes_service.py`, the application performs database operations, cache invalidation, note statistics, recent note listing, and event publishing. This gives the codebase a modular structure and makes it easier to explain the system in layers."

"The cache layer is implemented in `app/services/cache_service.py`. This file reads from Redis when available and safely falls back if Redis is not configured. That means the application can still run locally without Redis, but it can use Redis in production for cached note data and readiness behaviour."

"The event layer is implemented in `app/services/event_service.py`. This publishes note events to Kafka when Kafka bootstrap servers are configured. This is optional, so the application remains stable if Kafka is not active."

"The S3 integration is implemented in `app/services/s3_service.py`. This service creates the S3 client, generates safe object keys, uploads the file, and returns a public URL for the uploaded object."

"This layered structure is useful because it separates API handling, business logic, cache logic, event logic, and cloud storage logic."

## 10:30 - 12:30 Frontend and User Interaction

### What to show

- [templates/index.html](/Users/khanhbao/Desktop/Cloud%20Native%20App/templates/index.html)
- homepage in browser

### What to say

"Although this is mainly a backend and cloud deployment project, there is also a simple web interface in `templates/index.html`. This page allows the user to create notes, edit notes, delete notes, search notes, export JSON, view note statistics, view recent activity, and upload files to S3."

"The frontend communicates with the backend using `fetch` calls to the same API endpoints. This means the browser UI is directly connected to the Flask API, which makes it useful for demonstration purposes in the final video."

## 12:30 - 15:30 Kubernetes and YAML Code

### What to show

- [k8s/base/deployment.yaml](/Users/khanhbao/Desktop/Cloud%20Native%20App/k8s/base/deployment.yaml)
- [k8s/base/service.yaml](/Users/khanhbao/Desktop/Cloud%20Native%20App/k8s/base/service.yaml)
- [k8s/base/configmap.yaml](/Users/khanhbao/Desktop/Cloud%20Native%20App/k8s/base/configmap.yaml)
- [k8s/base/gateway.yaml](/Users/khanhbao/Desktop/Cloud%20Native%20App/k8s/base/gateway.yaml)
- [k8s/base/virtualservice.yaml](/Users/khanhbao/Desktop/Cloud%20Native%20App/k8s/base/virtualservice.yaml)
- [k8s/base/destinationrule.yaml](/Users/khanhbao/Desktop/Cloud%20Native%20App/k8s/base/destinationrule.yaml)
- [k8s/base/hpa.yaml](/Users/khanhbao/Desktop/Cloud%20Native%20App/k8s/base/hpa.yaml)
- [k8s/istio/istio-ingressgateway-service.yaml](/Users/khanhbao/Desktop/Cloud%20Native%20App/k8s/istio/istio-ingressgateway-service.yaml)

### What to say

"The Kubernetes layer is defined in YAML files under the `k8s` folder. The deployment file creates the application pods, sets resource requests and limits, injects configuration and secrets, and defines liveness and readiness probes. The application is deployed with two replicas in order to demonstrate basic high availability."

"The service file creates a ClusterIP service so that internal traffic inside the cluster can reach the application."

"The ConfigMap provides non-sensitive runtime configuration such as environment name, port, cache TTL, AWS region, and Kafka topic. Sensitive values such as database URL and AWS credentials are handled separately through Kubernetes secrets."

"The project also includes Istio resources. The Gateway exposes the application through the Istio ingress gateway, supports HTTPS, and redirects HTTP to HTTPS for the public domain. The VirtualService routes requests from the gateway to the application service. The DestinationRule enables Istio mutual TLS inside the service mesh."

"The ingress service in `k8s/istio/istio-ingressgateway-service.yaml` is configured as an internet-facing AWS load balancer. This is the part that exposes the cluster to the internet."

"There is also an HPA definition, which shows the intention to support autoscaling based on CPU utilisation."

## 15:30 - 18:30 Terraform and AWS Architecture

### What to show

- [terraform/main.tf](/Users/khanhbao/Desktop/Cloud%20Native%20App/terraform/main.tf)
- [terraform/variables.tf](/Users/khanhbao/Desktop/Cloud%20Native%20App/terraform/variables.tf)
- [terraform/outputs.tf](/Users/khanhbao/Desktop/Cloud%20Native%20App/terraform/outputs.tf)
- [docs/architecture.md](/Users/khanhbao/Desktop/Cloud%20Native%20App/docs/architecture.md)

### What to say

"Now I will explain the AWS architecture. The infrastructure is provisioned using Terraform. In `terraform/main.tf`, the project creates a VPC with both public and private subnets. It also creates a NAT gateway, which allows private workloads to access required external services."

"The project provisions an Amazon EKS cluster with a managed node group. The application pods run on EKS worker nodes inside the private subnets. This gives the application a production-style orchestration environment."

"For persistent relational storage, the project provisions Amazon RDS PostgreSQL. For caching and readiness support, it provisions Amazon ElastiCache Redis. For file uploads, it provisions an Amazon S3 bucket together with an IAM policy that allows the application to store and retrieve uploaded files."

"The project also provisions Route 53 resources so the public domain can point to the AWS load balancer. In the live deployment, this results in the public domain `khanhhoang.page`."

"This architecture is shown in the updated architecture document in the `docs` folder. The production traffic flow is: user to Route 53, Route 53 to the internet-facing load balancer, load balancer to the Istio ingress gateway, Istio routing to the Flask application on EKS, and then from the application to RDS, Redis, and S3."

## 18:30 - 19:30 CI/CD

### What to show

- [.github/workflows/ci-cd.yml](/Users/khanhbao/Desktop/Cloud%20Native%20App/.github/workflows/ci-cd.yml)
- [.github/workflows/deploy-aws.yml](/Users/khanhbao/Desktop/Cloud%20Native%20App/.github/workflows/deploy-aws.yml)
- GitHub Actions runs page

### What to say

"The repository also includes CI/CD support through GitHub Actions. The `CI-CD` workflow runs on push and pull request. It installs dependencies, compiles the Python files, runs the automated tests, checks Terraform formatting, and validates the Terraform configuration."

"There is also a separate AWS deployment workflow that supports building and pushing a container image and deploying the manifests to EKS. This shows that the project is not only manually deployable, but also structured for automated cloud delivery."

## 19:30 - 21:30 Live Demo

### What to show

- [https://khanhhoang.page](https://khanhhoang.page)
- [https://khanhhoang.page/health/live](https://khanhhoang.page/health/live)
- [https://khanhhoang.page/health/ready](https://khanhhoang.page/health/ready)
- create a note
- search for a note
- upload a file

### What to say

"Finally, I will demonstrate the live production environment. This is the deployed application running on AWS under my public domain."

"First, I will open the homepage. Next, I will open the liveness endpoint, which shows that the service is alive. Then I will open the readiness endpoint, which confirms that the application is connected to the database and Redis."

"I will now create a note through the user interface. After saving it, the note appears in the saved notes list. I can also search for the note, and the statistics and recent activity sections update accordingly."

"Next, I will test the S3 upload feature by selecting a file and uploading it. The application returns a URL for the uploaded object, which shows that cloud storage integration is working in the deployed environment."

## 21:30 - 22:00 Closing

### What to say

"In conclusion, this project demonstrates a full cloud-native workflow. It starts with local development, supports container-based development, uses modular application code, includes Kubernetes and Istio configuration, provisions AWS infrastructure through Terraform, and is deployed publicly through Route 53 and HTTPS. This shows how the original cloud development concept was translated into a working application."

