# Qdrant Hackathon Compliance Review

Official page reviewed: https://try.qdrant.tech/hackathon-vsd

## Submission Links

- Repository: https://github.com/lolomix/contract-revenue-radar
- Demo video: https://github.com/lolomix/contract-revenue-radar/releases/download/qdrant-submission-2026/contract_revenue_radar_qdrant_demo.mp4
- Release page: https://github.com/lolomix/contract-revenue-radar/releases/tag/qdrant-submission-2026

## Requirement Check

| Requirement | Status | Evidence |
|---|---|---|
| Use Qdrant as a material part of the project | Met | `src/contract_radar/core.py` uses a Qdrant local-memory backend when `qdrant-client` is installed. |
| Go beyond a simple chatbot | Met | The project is a structured audit engine: ingest, chunk, vector search, scoring, report, API/tool output. |
| GitHub repo with code | Met | Public GitHub repository linked above. |
| README with install/run instructions | Met | `README.md`. |
| Demo video no more than 3 minutes | Met | MP4 in `demo_video/` and GitHub release. |
| Basic code comments/documentation | Met | README, API guide, sample files, typed dataclasses, tests. |
| Team size 1-4 | Assumed solo | No external team files or shared work in repo. |
| Created during hackathon period | Evidence included | Git history starts May 29, 2026 and includes dated May 30-31 implementation commits. |
| Legal/license compliance | Met | MIT `LICENSE`; no secrets or private documents included. |

## Current Local Verification

```bash
python -m unittest discover -s tests
```

Expected:

```text
Ran 9 tests
OK
```

## Notes For Judges

Contract Revenue Radar uses Qdrant for vector search over contract sections, not conversational retrieval. The user receives a deterministic audit packet with exact excerpts and business actions. The MemoryAgent prototype shows how approved fallback positions can be recalled by risk class and segment without turning the product into a chatbot.
