# Technical Report Outline

GitHub Repository Link: `https://github.com/your-username/cloud-notes-app`

## 1. Introduction

- Briefly describe the real-world problem from Assignment 1.
- Explain the purpose of the Cloud Notes App and who would use it.

## 2. Application Overview

- Summarise the main features of the application.
- Explain how the solution translates the cloud proposal from Assignment 1 into a working implementation.

## 3. Architecture and Design Choices

- Describe the overall cloud architecture.
- Explain why you selected Flask, Docker, EKS, Istio, Terraform, RDS, Redis, and Kafka.
- Discuss trade-offs and alternatives considered.

## 4. Development Approach

- Explain how you built and tested the application.
- Summarise how containerisation, infrastructure-as-code, and CI/CD were applied.
- Reference key folders in the repository such as `app/`, `k8s/`, `terraform/`, and `.github/workflows/`.

## 5. Cloud Deployment

- Describe how the application is deployed to AWS.
- Explain the role of EKS, the Internet-facing load balancer, Route 53, and Istio ingress.
- Describe how the database, cache, and storage services are connected.

## 6. Testing and Validation

- Report the local tests you ran.
- Include evidence of successful deployment and working endpoints.
- Mention any limitations or parts that are optional or environment-dependent.

## 7. Reflection

- Reflect critically on your development process.
- Discuss what worked well, what was challenging, and what you would improve next.
- Explain what you learned about cloud-native development in practice.

## 8. Conclusion

- Summarise the final outcome of the project and how it meets the assignment requirements.

## Submission Reminders

- Keep the GitHub repository public.
- Place the repository link at the beginning of the report.
- Include the demo video file directly in the repository.
- Remove your personal identifiers from source files, comments, and documentation.
- Ensure your commit history is authentic and reflects real development progress.
