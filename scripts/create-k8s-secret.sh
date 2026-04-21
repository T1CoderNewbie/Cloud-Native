#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-cloud-notes}"
SECRET_NAME="${SECRET_NAME:-cloud-notes-secrets}"
ENV_FILE="${ENV_FILE:-}"
APPLY_CHANGES="${APPLY_CHANGES:-false}"

if [[ -n "${ENV_FILE}" ]]; then
  if [[ ! -f "${ENV_FILE}" ]]; then
    echo "Env file not found: ${ENV_FILE}" >&2
    exit 1
  fi

  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
fi

required_vars=(
  DATABASE_URL
  REDIS_URL
  KAFKA_BOOTSTRAP_SERVERS
  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  AWS_BUCKET_NAME
  AWS_REGION
)

for name in "${required_vars[@]}"; do
  if [[ -z "${!name:-}" ]]; then
    echo "Missing required environment variable: ${name}" >&2
    exit 1
  fi
done

cmd=(
  kubectl
  -n "${NAMESPACE}"
  create secret generic "${SECRET_NAME}"
  --from-literal=DATABASE_URL="${DATABASE_URL}"
  --from-literal=REDIS_URL="${REDIS_URL}"
  --from-literal=KAFKA_BOOTSTRAP_SERVERS="${KAFKA_BOOTSTRAP_SERVERS}"
  --from-literal=AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}"
  --from-literal=AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}"
  --from-literal=AWS_BUCKET_NAME="${AWS_BUCKET_NAME}"
  --from-literal=AWS_REGION="${AWS_REGION}"
  --from-literal=S3_ENDPOINT_URL="${S3_ENDPOINT_URL:-}"
  --from-literal=S3_PUBLIC_BASE_URL="${S3_PUBLIC_BASE_URL:-}"
  --dry-run=client
  -o yaml
)

if [[ "${APPLY_CHANGES}" == "true" ]]; then
  "${cmd[@]}" | kubectl apply -f -
else
  "${cmd[@]}"
fi
