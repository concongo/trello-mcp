FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml .
COPY src/ src/

RUN uv venv /app/.venv && \
    uv pip install --python /app/.venv/bin/python .

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ src/

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

CMD ["trello-mcp", "run", "--transport", "sse", "--port", "8000"]
