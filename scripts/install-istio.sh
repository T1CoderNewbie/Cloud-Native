#!/usr/bin/env bash
set -euo pipefail

ISTIO_VERSION="${ISTIO_VERSION:-1.24.0}"

curl -L https://istio.io/downloadIstio | ISTIO_VERSION="${ISTIO_VERSION}" sh -
"./istio-${ISTIO_VERSION}/bin/istioctl" install -y --set profile=demo
kubectl apply -f k8s/istio/istio-ingressgateway-service.yaml
