#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${NAMESPACE:-cloud-notes}"

kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/configmap.yaml
kubectl apply -f k8s/base/service.yaml
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/destinationrule.yaml
kubectl apply -f k8s/base/gateway.yaml
kubectl apply -f k8s/base/virtualservice.yaml
kubectl apply -f k8s/base/hpa.yaml
kubectl rollout status deployment/cloud-notes-app -n "${NAMESPACE}"
