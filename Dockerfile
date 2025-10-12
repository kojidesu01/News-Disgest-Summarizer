FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build tooling only for dependency compilation.
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies into a relocatable prefix we can copy into the runtime image.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PORT=5000 \
    NEWS_DB_PATH=/app/src/Disgest_Summerizer/news_articles.db

WORKDIR /app

# Bring the site-packages and scripts installed in the builder stage.
COPY --from=builder /install /usr/local

COPY src ./src

EXPOSE 5000

CMD ["python", "src/Disgest_Summerizer/app.py"]
