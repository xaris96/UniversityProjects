# Stage 1: Build dependencies
FROM python:3.12-slim AS builder

WORKDIR /app
COPY . .
RUN python -m venv /venv && /venv/bin/pip install --no-cache-dir .

# Stage 2: Runtime
FROM python:3.12-slim
COPY --from=builder /venv /venv
COPY --from=builder /app /app
WORKDIR /app

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Database directory
RUN mkdir -p /app/data

# Environment variables
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0

EXPOSE 5000
CMD ["/venv/bin/python", "app.py"]
