#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${NAMESPACE:-cloud-notes}"
APP_IMAGE="${APP_IMAGE:-}"
CREATE_K8S_SECRET="${CREATE_K8S_SECRET:-false}"
SECRET_ENV_FILE="${SECRET_ENV_FILE:-}"

kubectl apply -f k8s/base/namespace.yaml

if [[ "${CREATE_K8S_SECRET}" == "true" ]]; then
  ENV_FILE="${SECRET_ENV_FILE}" APPLY_CHANGES=true NAMESPACE="${NAMESPACE}" \
    "${SCRIPT_DIR}/create-k8s-secret.sh"
fi

kubectl apply -f k8s/base/configmap.yaml
kubectl apply -f k8s/base/service.yaml
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/destinationrule.yaml
kubectl apply -f k8s/base/gateway.yaml
kubectl apply -f k8s/base/virtualservice.yaml
kubectl apply -f k8s/base/hpa.yaml

if [[ -n "${APP_IMAGE}" ]]; then
  kubectl -n "${NAMESPACE}" set image deployment/cloud-notes-app cloud-notes-app="${APP_IMAGE}"
fi

kubectl rollout status deployment/cloud-notes-app -n "${NAMESPACE}"
