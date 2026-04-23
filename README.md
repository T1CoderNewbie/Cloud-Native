# Cloud Notes App

Cloud Notes App is a simple cloud-native notes API built for a Developing for the Cloud assignment. The project includes a Flask backend, Docker support, AWS-ready deployment files, and infrastructure templates for EKS, RDS, Istio, and Terraform.

## Project Goal

This project demonstrates how a locally developed application can be prepared for cloud deployment using containerisation, infrastructure-as-code, and Kubernetes-based deployment practices. The application allows users to create, view, update, and delete notes, while also supporting AWS-oriented services such as RDS, S3, Redis, Kafka, EKS, and Istio.

## Live Deployment

The current production deployment is available at:

- Application: `https://khanhhoang.page`
- Live health check: `https://khanhhoang.page/health/live`
- Ready health check: `https://khanhhoang.page/health/ready`
- Public repository: `https://github.com/T1CoderNewbie/Cloud-Native`

The live environment currently runs on AWS with Route 53, an internet-facing load balancer, Istio ingress, Amazon EKS, Amazon RDS, Amazon ElastiCache Redis, and Amazon S3.

## Technology Stack

- Python Flask
- PostgreSQL or SQLite
- Redis
- Kafka
- Amazon S3
- Docker and Docker Compose
- AWS ECR or Docker Hub
- Kubernetes on AWS EKS
- Istio
- Route 53
- Terraform
- GitHub Actions

## Project Structure

```text
cloud-notes-app/
├── app/
├── docs/
├── k8s/
├── scripts/
├── terraform/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── main.py
└── requirements.txt
```

## Setup Instructions

### Option 1: Quick local run with SQLite

```bash
cp .env.example .env
source .venv/bin/activate
python main.py
```

If `.venv` does not exist yet:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Open:

- `http://localhost:5000`
- `http://localhost:5000/health/live`
- `http://localhost:5000/health/summary`
- `http://localhost:5000/notes`

### Option 2: Run the containerised stack with Docker Compose

```bash
docker compose up --build
```

This starts:

- app
- PostgreSQL
- Redis
- Kafka

## Development and Testing

Run the automated tests with:

```bash
source .venv/bin/activate
pytest
```

Useful local checks:

- `http://localhost:5000/health/live` returns a small JSON response to confirm the app is alive.
- `http://localhost:5000/health/ready` checks database and Redis readiness.
- `http://localhost:5000/health/summary` shows readiness details plus the current note count.

Quick manual API test:

```bash
curl -X POST http://localhost:5000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"My first note"}'
```

## Main API Endpoints

- `GET /`
- `GET /health/live`
- `GET /health/ready`
- `GET /notes`
- `POST /notes`
- `PUT /notes/<id>`
- `DELETE /notes/<id>`
- `POST /upload`

## Environment Variables

Basic local setup:

```env
PORT=5000
FLASK_DEBUG=true
ENVIRONMENT=development
DATABASE_URL=sqlite:///data/notes.db
REDIS_URL=redis://localhost:6379/0
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
AWS_BUCKET_NAME=your_bucket_name
AWS_REGION=ap-southeast-1
```

If you want S3 upload to work, add real AWS credentials in `.env`.

## Cloud Deployment Guidance

This repo already includes:

- Docker image setup in `Dockerfile`
- Kubernetes manifests in `k8s/`
- Istio gateway and routing config
- Terraform infrastructure in `terraform/`
- CI/CD workflow in `.github/workflows/ci-cd.yml`

Current production deployment summary:

- Container image hosted in AWS ECR
- Application deployed to Amazon EKS
- Database hosted in Amazon RDS PostgreSQL
- Cache hosted in Amazon ElastiCache Redis
- File upload stored in Amazon S3
- Public DNS managed through Route 53
- Domain exposed at `https://khanhhoang.page`

Basic cloud deployment flow:

1. Build and push Docker image to Docker Hub or AWS ECR.
2. Provision AWS infrastructure with Terraform.
3. Configure `kubectl` for your EKS cluster.
4. Install Istio.
5. Apply Kubernetes manifests.
6. Point Route 53 to the load balancer and enable the production domain.

Deployment-related files:

- `Dockerfile`
- `docker-compose.yml`
- `k8s/`
- `scripts/create-k8s-secret.sh`
- `scripts/apply-k8s.sh`
- `scripts/check-aws-preflight.sh`
- `terraform/`
- `.github/workflows/ci-cd.yml`
- `.github/workflows/deploy-aws.yml`

Workflow note:

- `CI-CD` runs automatically on push and pull request for tests and Terraform validation
- `Deploy AWS` is a separate manual workflow for Docker Hub build and EKS deployment after secrets are configured

GitHub Actions tip:

- Older commits may still show a red `X` if they were pushed before the workflow was fixed.
- You do not need to rewrite history for that. What matters is that your newest commits pass the current `CI-CD` workflow.
- For AWS deployment, open the `Deploy AWS` workflow in GitHub Actions and run it manually after adding the required secrets.

## AWS Deployment Prep

Recommended tools on your local machine:

- Docker
- AWS CLI
- `kubectl`
- `istioctl`
- Terraform

Prepare Terraform values:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Prepare application secrets for Kubernetes:

```bash
cp .env.aws.example .env.aws
```

Run a quick local preflight check before provisioning or deploying:

```bash
bash scripts/check-aws-preflight.sh
```

If you only want to inspect the current state without failing on missing tools yet:

```bash
FAIL_ON_MISSING=false bash scripts/check-aws-preflight.sh
```

After filling in real values inside `.env.aws`, you can create the Kubernetes secret manifest or apply it directly:

```bash
ENV_FILE=.env.aws bash scripts/create-k8s-secret.sh
ENV_FILE=.env.aws APPLY_CHANGES=true bash scripts/create-k8s-secret.sh
```

When you already have an image in Docker Hub, deploy the base manifests and set the image in one go:

```bash
CREATE_K8S_SECRET=true \
SECRET_ENV_FILE=.env.aws \
APP_IMAGE=docker.io/<dockerhub-username>/cloud-notes-app:latest \
bash scripts/apply-k8s.sh
```

GitHub secrets expected by `Deploy AWS`:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `EKS_CLUSTER_NAME`
- `DATABASE_URL`
- `REDIS_URL`
- `KAFKA_BOOTSTRAP_SERVERS`
- `APP_AWS_ACCESS_KEY_ID`
- `APP_AWS_SECRET_ACCESS_KEY`
- `AWS_BUCKET_NAME`
- `S3_ENDPOINT_URL`
- `S3_PUBLIC_BASE_URL`

## Assignment Notes

- Keep the GitHub repository public.
- Put the GitHub link at the beginning of your report.
- Upload your demo video inside `docs/video/`.
- Keep commit history meaningful and authentic.
- Remove personal information before submission.

## Extra Docs

- Architecture: [docs/architecture.md](docs/architecture.md)
- Technical report outline: [docs/technical-report-outline.md](docs/technical-report-outline.md)
