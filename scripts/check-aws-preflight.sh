#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_FILE="${ENV_FILE:-${ROOT_DIR}/.env.aws}"
TFVARS_FILE="${TFVARS_FILE:-${ROOT_DIR}/terraform/terraform.tfvars}"
FAIL_ON_MISSING="${FAIL_ON_MISSING:-true}"

status=0

report_ok() {
  echo "[ok] $1"
}

report_warn() {
  echo "[warn] $1"
  if [[ "${FAIL_ON_MISSING}" == "true" ]]; then
    status=1
  fi
}

check_command() {
  local name="$1"
  if command -v "${name}" >/dev/null 2>&1; then
    report_ok "Found command: ${name}"
  else
    report_warn "Missing command: ${name}"
  fi
}

read_env_value() {
  local name="$1"
  local file="$2"
  local line
  local value

  line="$(grep -E "^${name}[[:space:]]*=" "${file}" | tail -n 1 || true)"
  if [[ -z "${line}" ]]; then
    return 1
  fi

  value="${line#*=}"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  value="${value%\"}"
  value="${value#\"}"
  printf "%s" "${value}"
}

check_env_value() {
  local name="$1"
  local file="$2"
  local value

  if ! value="$(read_env_value "${name}" "${file}")"; then
    report_warn "Missing variable ${name} in ${file}"
    return
  fi

  if [[ -z "${value}" || "${value}" == "CHANGE_ME" || "${value}" == "replace-me" || "${value}" == "your-s3-bucket" ]]; then
    report_warn "Placeholder or empty value for ${name} in ${file}"
    return
  fi

  report_ok "Configured ${name} in ${file}"
}

echo "Checking local AWS deployment prerequisites..."

for tool in docker aws kubectl istioctl terraform; do
  check_command "${tool}"
done

if [[ -f "${ENV_FILE}" ]]; then
  report_ok "Found env file: ${ENV_FILE}"
  for name in DATABASE_URL REDIS_URL KAFKA_BOOTSTRAP_SERVERS AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_REGION AWS_BUCKET_NAME; do
    check_env_value "${name}" "${ENV_FILE}"
  done
else
  report_warn "Missing env file: ${ENV_FILE}"
fi

if [[ -f "${TFVARS_FILE}" ]]; then
  report_ok "Found Terraform vars file: ${TFVARS_FILE}"
  check_env_value "db_password" "${TFVARS_FILE}"
else
  report_warn "Missing Terraform vars file: ${TFVARS_FILE}"
fi

if [[ "${status}" -ne 0 ]]; then
  echo "AWS preflight check did not pass."
  exit "${status}"
fi

echo "AWS preflight check passed."
