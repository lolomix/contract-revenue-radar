# GitHub Publishing Checklist

Status: published.

- Repository: https://github.com/lolomix/contract-revenue-radar
- Visibility: public
- Default branch: `main`
- License: MIT
- Release: https://github.com/lolomix/contract-revenue-radar/releases/tag/qdrant-submission-2026

## Final Local Checks

```bash
git status --short --branch
python -m unittest discover -s tests
./scripts/demo.sh
```

## Push Updates

```bash
git add .
git commit -m "Finalize Qdrant submission presentation"
git push origin main
```

## Submission Links

Use these in the Qdrant form:

```text
https://github.com/lolomix/contract-revenue-radar
https://github.com/lolomix/contract-revenue-radar/releases/download/qdrant-submission-2026/contract_revenue_radar_qdrant_demo_final.mp4
```
