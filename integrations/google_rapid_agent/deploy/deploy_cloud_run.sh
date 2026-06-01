#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${PROJECT_ID:-}" ]]; then
  echo "Set PROJECT_ID to your Google Cloud project id." >&2
  exit 1
fi

REGION="${REGION:-us-central1}"
REPOSITORY="${REPOSITORY:-revenue-agent}"
SERVICE="${SERVICE:-revenue-terms-agent-api}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QDRANT_REPO="${QDRANT_REPO:-/home/ubuntu/revenue_5000/qdrant-contract-radar}"
TAG="$(git -C "$QDRANT_REPO" rev-parse --short HEAD 2>/dev/null || date -u +%Y%m%d%H%M%S)"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${SERVICE}:${TAG}"

gcloud config set project "$PROJECT_ID"
gcloud services enable run.googleapis.com artifactregistry.googleapis.com

if ! gcloud artifacts repositories describe "$REPOSITORY" --location "$REGION" >/dev/null 2>&1; then
  gcloud artifacts repositories create "$REPOSITORY" \
    --repository-format docker \
    --location "$REGION" \
    --description "Revenue Terms Agent container images"
fi

gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet
docker build -f "${SCRIPT_DIR}/cloud-run.Dockerfile" -t "$IMAGE" "$QDRANT_REPO"
docker push "$IMAGE"

gcloud run deploy "$SERVICE" \
  --image "$IMAGE" \
  --region "$REGION" \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 3

SERVICE_URL="$(gcloud run services describe "$SERVICE" --region "$REGION" --format 'value(status.url)')"
echo "Cloud Run URL: ${SERVICE_URL}"
echo "Health check: ${SERVICE_URL}/health"
echo "Agent Builder OpenAPI: replace YOUR_CLOUD_RUN_URL in google_rapid_agent_submission/openapi/revenue_terms_agent_openapi.yaml"
