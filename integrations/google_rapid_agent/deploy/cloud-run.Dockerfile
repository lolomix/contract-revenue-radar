FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY scripts ./scripts
COPY samples ./samples

RUN pip install --no-cache-dir -e ".[qdrant]"

EXPOSE 8080

CMD ["sh", "-c", "python scripts/serve_agent_api.py --host 0.0.0.0 --port ${PORT:-8080}"]
