# Use uv's official image for a lean build
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Install dependencies first (cached layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "web:app", "--host", "0.0.0.0", "--port", "8000"]
