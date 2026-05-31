#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p examples/reports

if [[ -x ".venv/bin/contract-radar" ]]; then
  .venv/bin/contract-radar samples/acme_services_agreement.md -o examples/reports/qdrant_demo_report.md
else
  PYTHONPATH=src python3 -m contract_radar.cli --no-qdrant samples/acme_services_agreement.md -o examples/reports/demo_report.md
fi

REPORT="examples/reports/qdrant_demo_report.md"
if [[ ! -f "$REPORT" ]]; then
  REPORT="examples/reports/demo_report.md"
fi

sed -n '1,90p' "$REPORT"
