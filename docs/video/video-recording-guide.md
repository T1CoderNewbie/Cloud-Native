# Video Recording Guide

This guide shows how to prepare and record the final demonstration video from start to finish.

## 1. Before You Start Recording

Prepare these items before pressing record:

- close unrelated apps and personal tabs
- hide anything that shows private information
- do not open `.env.aws`, `terraform.tfvars`, AWS secret pages, or any screen with keys and passwords
- make sure the live app opens at `https://khanhhoang.page`
- make sure the repository opens at `https://github.com/T1CoderNewbie/Cloud-Native`
- make sure the latest GitHub Actions run is visible and green
- keep the AWS Console signed in if you want to show EKS, RDS, Redis, S3, and Route 53

## 2. Recommended Browser Tabs

Open these tabs before recording:

1. GitHub repository home page
2. `README.md`
3. `main.py`
4. `app/config.py`
5. `app/models/db.py`
6. `app/routes/notes.py`
7. `app/services/notes_service.py`
8. `app/services/cache_service.py`
9. `app/services/event_service.py`
10. `app/services/s3_service.py`
11. `Dockerfile`
12. `docker-compose.yml`
13. `k8s/base/deployment.yaml`
14. `k8s/base/gateway.yaml`
15. `k8s/base/virtualservice.yaml`
16. `terraform/main.tf`
17. `docs/architecture.md`
18. GitHub Actions page
19. live app at `https://khanhhoang.page`
20. live health endpoints

If you want to show AWS Console too, prepare these pages:

- EKS cluster
- RDS database
- ElastiCache Redis
- S3 bucket
- Route 53 hosted zone

## 3. Recording Order

Use this order so the video feels clear and professional:

1. Introduce the project and the assignment goal
2. Show the GitHub repository and folder structure
3. Explain local development
4. Explain Docker and Docker Compose
5. Explain application functionality
6. Explain service-layer design
7. Explain Kubernetes and Istio YAML
8. Explain Terraform and AWS infrastructure
9. Show CI/CD
10. Show the live deployed application
11. Conclude with what the project demonstrates

## 4. What to Avoid

Do not show these things on screen:

- AWS access keys
- secret environment files
- GitHub secrets page
- database passwords
- terminal history with sensitive values
- random personal documents or messages

Do not say these inaccurate statements:

- do not say Kafka is definitely running in the live AWS production path unless you specifically prove it
- do not say Docker Hub is the current live registry if you are explaining the running production image, because the live environment currently runs from AWS ECR

## 5. How to Speak Clearly

Use short sentences and keep the structure simple:

- say what the file does
- say why it matters
- say how it connects to the cloud deployment

A good pattern is:

"This file is responsible for..."
"This matters because..."
"In the deployed architecture, it connects to..."

## 6. Time Management for 22 Minutes

Recommended timing:

- 1 minute opening
- 1.5 minutes repository overview
- 2 minutes local development
- 2 minutes container code
- 4 minutes functionality and services
- 2 minutes frontend flow
- 3 minutes YAML and Istio
- 3 minutes Terraform and AWS
- 1 minute CI/CD
- 2 minutes live demo
- 0.5 minute closing

## 7. Backup Plan During Recording

If something loads slowly:

- keep talking while the page loads
- explain the file or architecture first
- then return to the live page

If the local app is not running:

- do not panic
- explain the local setup from `README`, `main.py`, `config.py`, and `docker-compose.yml`
- then continue with the live cloud deployment, which is the stronger part of the project

If the live app is briefly slow:

- open the health endpoints
- explain that the service is publicly available through the custom domain and AWS architecture

## 8. Final Submission Reminder

Before you finish:

- save the final video file clearly
- place the file inside `docs/video/` if you will upload it directly into GitHub
- or prepare the allowed public video link if your lecturer accepts that format
- make sure the video audio is clear
- make sure the video shows both the code explanation and the working application

## 9. Best Final Ending Line

You can close with this sentence:

"This project demonstrates how a local application can be transformed into a cloud-native system using Docker, Kubernetes, Istio, Terraform, AWS managed services, CI/CD, and a live public deployment."

