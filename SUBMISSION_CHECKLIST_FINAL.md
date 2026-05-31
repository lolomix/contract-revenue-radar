# Qdrant Final Submission Checklist

Deadline: June 1, 2026 at 11:59 PM Pacific Time.

Official page: https://try.qdrant.tech/hackathon-vsd

## Public Assets

- GitHub repo: https://github.com/lolomix/contract-revenue-radar
- Demo video: https://github.com/lolomix/contract-revenue-radar/releases/download/qdrant-submission-2026/contract_revenue_radar_qdrant_demo.mp4
- Release page: https://github.com/lolomix/contract-revenue-radar/releases/tag/qdrant-submission-2026
- Source archive: https://github.com/lolomix/contract-revenue-radar/releases/download/qdrant-submission-2026/contract-revenue-radar-submission.zip

## Requirement Status

- [x] Qdrant used as primary vector-search backend when installed.
- [x] Project is not a chatbot.
- [x] Public GitHub repository exists.
- [x] README includes install and run instructions.
- [x] Demo video exists and is under 3 minutes.
- [x] MIT license included.
- [x] Tests pass locally.
- [x] Submission form answers prepared.
- [ ] Final Qdrant form submitted.
- [ ] Confirmation saved outside repo.

## Verification Commands

```bash
python -m unittest discover -s tests
./scripts/demo.sh
python scripts/memory_agent_demo.py samples/saas_msa_example.md \
  --memory samples/clause_memory.json \
  --segment "SaaS implementation" \
  --no-qdrant \
  -o examples/reports/memory_agent_report.md
```

Expected:

```text
Ran 9 tests
OK
```

## Submit These Fields

- Project name: `Contract Revenue Radar`
- Repository URL: `https://github.com/lolomix/contract-revenue-radar`
- Demo video URL: `https://github.com/lolomix/contract-revenue-radar/releases/download/qdrant-submission-2026/contract_revenue_radar_qdrant_demo.mp4`
- Description/Qdrant usage: paste from `SUBMISSION_FORM_ANSWERS.md`

## Notes

The repo was cleaned for judge review: core code, tests, samples, demo video, generated example reports, API/tool scripts, and submission docs remain. Non-Qdrant marketing and future-hackathon material was removed from the public repo.
