# Cloud Notes App

Cloud Notes App is a simple cloud-native notes API built for a Developing for the Cloud assignment. The project includes a Flask backend, Docker support, AWS-ready deployment files, and infrastructure templates for EKS, RDS, Istio, and Terraform.

## Project Goal

This project demonstrates how a locally developed application can be prepared for cloud deployment using containerisation, infrastructure-as-code, and Kubernetes-based deployment practices. The application allows users to create, view, update, and delete notes, while also supporting AWS-oriented services such as RDS, S3, Redis, Kafka, EKS, and Istio.

## Technology Stack

- Python Flask
- PostgreSQL or SQLite
- Redis
- Kafka
- Amazon S3
- Docker and Docker Compose
- Kubernetes on AWS EKS
- Istio
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

Basic cloud deployment flow:

1. Build and push Docker image to Docker Hub.
2. Provision AWS infrastructure with Terraform.
3. Configure `kubectl` for your EKS cluster.
4. Install Istio.
5. Apply Kubernetes manifests.
6. Point Route 53 to the load balancer if needed.

Deployment-related files:

- `Dockerfile`
- `docker-compose.yml`
- `k8s/`
- `terraform/`
- `.github/workflows/ci-cd.yml`

Workflow note:

- `CI-CD` runs automatically on push and pull request for tests and Terraform validation
- `Deploy AWS` is a separate manual workflow for Docker Hub build and EKS deployment after secrets are configured

GitHub Actions tip:

- Older commits may still show a red `X` if they were pushed before the workflow was fixed.
- You do not need to rewrite history for that. What matters is that your newest commits pass the current `CI-CD` workflow.
- For AWS deployment, open the `Deploy AWS` workflow in GitHub Actions and run it manually after adding the required secrets.

## Assignment Notes

- Keep the GitHub repository public.
- Put the GitHub link at the beginning of your report.
- Upload your demo video inside `docs/video/`.
- Keep commit history meaningful and authentic.
- Remove personal information before submission.

## Extra Docs

- Architecture: [docs/architecture.md](docs/architecture.md)
