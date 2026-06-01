#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8765}"

curl -s "${API_URL}/health"
echo
curl -s "${API_URL}/audit" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "sample_sow.md",
    "text": "Payment is Net 90 after customer acceptance. Customer may request unlimited revisions and terminate for convenience on 30 days notice.",
    "no_qdrant": true
  }'
echo
