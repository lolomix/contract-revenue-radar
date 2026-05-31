# Sample DOCX Deliverable

`report.docx` is a generated example of the professional client deliverable created by Contract Revenue Radar.

Generate a fresh DOCX report with:

```bash
.venv/bin/python -m contract_radar.cli \
  samples/saas_msa_example.md \
  --agent-brief \
  --format docx \
  --docx-output report.docx
```

The DOCX is useful for sales credibility and client demos. If the public GitHub repository should stay source-only, regenerate it during demos instead of committing the binary file.
