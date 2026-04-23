# Technical Report Outline

Use this file as the writing scaffold for the final 2000-2500 word report. Replace bracketed notes with your own wording, and keep the report focused on what this project actually implements.

## Report Header

Start the report with these three lines:

- GitHub Repository: `https://github.com/T1CoderNewbie/Cloud-Native`
- Live Application: `https://khanhhoang.page`
- Demo Video: `[add repo path or OneDrive public link here]`

Suggested title:

`Cloud Notes App: Developing and Deploying a Cloud-Native Notes Platform on AWS`

## 1. Introduction and Project Goals

Suggested target length: 200-250 words.

Cover these points:

- Introduce the project as a cloud-native notes management application.
- Explain the problem the project solves. A simple angle is that users need a lightweight way to create, store, and access notes in a reliable cloud environment rather than only on one local machine.
- State that the project was developed for the Developing for the Cloud assignment.
- Mention that the system supports note CRUD operations, health monitoring, and file upload.
- End the section by summarising the main cloud goal: transforming a local Flask application into a production-style deployment on AWS using containerisation, orchestration, service exposure, and infrastructure-as-code.

Example direction:

"The goal of this project was to design and implement a cloud-based notes application that moves beyond a local prototype and demonstrates practical cloud engineering skills. The final system supports note creation, viewing, updating, deletion, health monitoring, and Amazon S3 file upload. The project was containerised with Docker, provisioned with Terraform, deployed on Amazon EKS, connected to Amazon RDS and Amazon ElastiCache Redis, exposed through Istio and an internet-facing load balancer, and published through Route 53 using the domain khanhhoang.page."

## 2. Link to Assignment 1 Case Study

Suggested target length: 200-250 words.

Cover these points:

- Briefly explain what you proposed in Assignment 1.
- State how this implementation continues that earlier idea.
- If the Assignment 1 case study had a broader real-world scenario, explain which part is now implemented in this working prototype.
- Make it clear that Assignment 2 is the practical development stage of the original concept.

You can adapt this structure:

- Assignment 1 identified the need for a cloud-hosted application in `[your case study area]`.
- The implementation in Assignment 2 focuses on building the core working platform.
- The final system demonstrates the technical feasibility of the earlier proposal by deploying the application on AWS and integrating cloud services.

## 3. Application Features and Functional Scope

Suggested target length: 180-220 words.

Describe the actual features you now have:

- Create notes
- List notes
- Update notes
- Delete notes
- Health endpoints:
  - `/health/live`
  - `/health/ready`
  - `/health/summary`
- File upload to Amazon S3
- Public access through the live domain

Explain that the project supports both local development and cloud deployment. Mention that local development can run with SQLite, while the production deployment uses AWS services such as RDS and Redis.

## 4. System Architecture and Deployment Model

Suggested target length: 350-450 words.

Use [docs/architecture.md](architecture.md) as the basis for this section.

Describe the architecture in flow order:

1. User accesses the application through `https://khanhhoang.page`
2. Route 53 resolves the domain
3. Traffic reaches the internet-facing AWS load balancer
4. Istio ingress gateway receives traffic inside the EKS cluster
5. Requests are routed to the Flask application pods
6. The application stores note data in Amazon RDS PostgreSQL
7. Redis supports caching and readiness behaviour
8. S3 stores uploaded files
9. GitHub Actions supports CI/CD
10. Terraform provisions the AWS infrastructure

Important details to mention:

- The application is deployed on Amazon EKS using Kubernetes manifests in the `k8s/` directory.
- Istio is used as the service mesh and ingress layer.
- The deployment is internet-facing through the load balancer.
- Route 53 provides the public production domain.
- HTTPS is enabled for the production domain.

## 5. Justification of Cloud Services and Technologies

Suggested target length: 350-450 words.

Organise this section by service choice and justification:

- Flask:
  - lightweight and suitable for a small cloud application prototype
- Docker:
  - provides a consistent runtime for local development and cloud deployment
- Docker Compose:
  - simplifies local multi-service development with PostgreSQL, Redis, and Kafka
- Amazon EKS:
  - supports container orchestration, scaling, and production-style deployment
- Istio:
  - provides ingress control and service mesh capabilities required by the assignment
- Amazon RDS PostgreSQL:
  - managed relational database for persistent note data
- Amazon ElastiCache Redis:
  - managed cache and useful support for readiness and performance improvements
- Amazon S3:
  - durable object storage for uploaded files
- Route 53:
  - provides a professional public DNS layer and production domain mapping
- Terraform:
  - enables repeatable infrastructure provisioning as code
- GitHub Actions:
  - supports automated testing and deployment workflow checks
- Kafka:
  - included in the local stack and codebase to demonstrate event-driven integration potential, even if it is not the strongest part of the final cloud deployment
- AWS ECR:
  - used as the current production container registry for the running deployment

## 6. Development and Testing Process

Suggested target length: 250-320 words.

Describe how the project was built and validated:

- local development started with Flask and SQLite
- containerisation was added with Docker and Docker Compose
- supporting services were added locally:
  - PostgreSQL
  - Redis
  - Kafka
- infrastructure definitions were created in Terraform
- Kubernetes and Istio manifests were prepared for EKS deployment
- GitHub Actions was configured for CI
- the application was tested locally with `pytest`
- health endpoints were used to confirm liveness and readiness
- the cloud deployment was verified through the live domain and direct health checks

Specific evidence you can mention:

- tests pass locally
- the production app responds on `https://khanhhoang.page`
- the live health endpoint returns a valid JSON response
- file upload works through S3

## 7. Challenges Encountered and How They Were Addressed

Suggested target length: 250-320 words.

Use real problems from this project. Good examples are:

- configuring Terraform for AWS infrastructure creation
- connecting Kubernetes workloads to AWS services such as RDS and Redis
- exposing the application correctly through Istio and a public load balancer
- configuring Route 53 so the custom domain pointed to the correct AWS endpoint
- enabling HTTPS for the production domain
- handling GitHub Actions failures and fixing CI so the latest runs became successful
- managing cloud credentials and avoiding committing secrets to the repository

For each challenge, write:

- what went wrong
- why it mattered
- how you fixed it
- what you learned

## 8. GenAI Use During Planning

Suggested target length: 100-150 words.

You can adapt this draft:

"Generative AI was used during planning and implementation as a support tool for structuring tasks, clarifying cloud deployment steps, and improving documentation. It helped break down the project into manageable phases, including local development, containerisation, infrastructure provisioning, Kubernetes deployment, Route 53 configuration, and final verification. GenAI was also useful for identifying likely causes of CI/CD failures and suggesting debugging directions for Terraform, GitHub Actions, and Istio ingress configuration. However, all outputs still required manual review, testing, and validation in the actual AWS environment. This was important because cloud deployment work is highly dependent on real infrastructure state, credentials, DNS propagation, and service connectivity, which cannot be trusted without direct verification."

## 9. Reflection and Conclusion

Suggested target length: 180-220 words.

End with:

- what the project achieved technically
- what cloud skills you developed
- what could be improved in a future version
- a short reflection on why the project now meets the main assignment goals

Reasonable future improvements to mention:

- full cloud Kafka deployment
- CloudWatch or Prometheus monitoring
- automated certificate renewal workflow
- autoscaling improvements
- stronger secret management with AWS Secrets Manager

## 10. Suggested Evidence to Include

Add screenshots or figures for:

- GitHub repository front page
- GitHub Actions successful workflow run
- Terraform or AWS infrastructure overview
- EKS or Kubernetes workload status
- live application at `khanhhoang.page`
- health endpoint response
- S3 upload feature
- architecture diagram

## Final Reminder

Before submission, make sure the report matches the real repository contents:

- public GitHub repo
- live domain
- Docker, YAML, and Terraform files included
- video file or allowed public video link included
- no personal identifiers or secrets committed to the repo
