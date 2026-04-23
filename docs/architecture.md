# Cloud Notes App Architecture

This document reflects the project as it currently exists in the repository and in the live AWS deployment.

## Production Architecture

```mermaid
flowchart LR
    User["Student / Marker"] --> DNS["Route 53 DNS<br/>khanhhoang.page"]
    DNS --> LB["AWS Internet-facing Load Balancer"]
    LB --> IGW["Istio Ingress Gateway<br/>HTTP to HTTPS redirect + TLS"]
    IGW --> ROUTING["Istio Gateway and VirtualService"]
    ROUTING --> APP["Cloud Notes App<br/>Flask deployment on Amazon EKS"]
    APP --> RDS["Amazon RDS PostgreSQL<br/>persistent note data"]
    APP --> REDIS["Amazon ElastiCache Redis<br/>cache and readiness support"]
    APP --> S3["Amazon S3<br/>file uploads"]
    APP -->|Optional event publishing when configured| KAFKA["Kafka broker or topic"]
```

## Infrastructure Provisioning and Delivery

```mermaid
flowchart LR
    TF["Terraform"] --> VPC["AWS VPC<br/>public and private subnets + NAT"]
    TF --> EKS["Amazon EKS cluster<br/>managed node group"]
    TF --> RDS["Amazon RDS PostgreSQL"]
    TF --> REDIS["Amazon ElastiCache Redis"]
    TF --> S3["Amazon S3 uploads bucket"]
    TF --> DNS["Route 53 hosted zone and alias record"]

    GHA["GitHub Actions CI-CD"] --> CHECKS["Compile, test, terraform validate"]
    GHA --> ECR["Amazon ECR<br/>current live image registry"]
    GHA --> DH["Docker Hub<br/>optional/manual workflow path"]
    ECR --> EKS
    DH --> EKS
```

## Local Development Views

### Quick Local Run

```mermaid
flowchart LR
    Browser["Browser on localhost:5000"] --> Flask["Flask app from main.py"]
    Flask --> SQLite["SQLite database<br/>default local mode"]
```

### Docker Compose Development Stack

```mermaid
flowchart LR
    Browser["Browser on localhost:5000"] --> App["App container"]
    App --> PG["PostgreSQL container"]
    App --> Redis["Redis container"]
    App --> Kafka["Kafka container"]
```

## Architecture Notes

- The live public domain is `https://khanhhoang.page`.
- The live production deployment currently uses Amazon ECR for the running application image.
- Docker Hub is still represented in the repository because the deployment workflow supports that path, but the current live environment is running from ECR.
- Kafka exists in the codebase and local Docker Compose stack. In the application code it is optional and only publishes events when `KAFKA_BOOTSTRAP_SERVERS` is configured.
- Redis and database connectivity are part of the readiness checks, so they are not just diagram components; they are used directly by the running service.
- Istio is implemented through the ingress gateway, Gateway, VirtualService, and DestinationRule manifests in `k8s/`.
