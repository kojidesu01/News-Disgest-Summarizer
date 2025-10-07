# News Digest Summarizer

News Digest Summarizer collects breaking headlines, scrapes full-text articles, generates abstractive summaries with a Hugging Face model, and serves the curated dataset through a lightweight Flask API. The project also ships with helper scripts to rebuild the SQLite database and a static HTML demo that can consume the API.

---

## Features

- End-to-end workflow: ingest JSON news payloads, scrape missing content, run transformer-based summarization, and persist results in SQLite.
- REST API built with Flask, including category-based filtering and serialization compatible with front-end clients.
- Optional automation scripts for fetching new articles from the GNews API and rebuilding the local database.
- Dockerfile for containerized deployment plus a minimal static front-end (`src/Disgest_Summerizer/Web/NewWeb.html`).

---

## Project Structure

```text
News-Disgest-Summarizer/
|-- src/
|   `-- Disgest_Summerizer/
|       |-- app.py                  # Flask app exposing /api/articles
|       |-- data/
|       |   |-- DataNews.json       # Sample dataset used to seed the database
|       |   |-- DataNews_source.py  # Imports JSON, scrapes content, runs summarization, writes SQLite
|       |   |-- Web_Scraping_script.py
|       |   `-- script_getNewto_Json.py
|       |-- news_articles.db        # Generated SQLite database (ignored by git)
|       `-- Web/
|           `-- NewWeb.html         # Simple front-end demo
|-- tests/                          # Pytest suite for the API
|-- requirements.txt
|-- Dockerfile
`-- README.md
```

---

## Requirements

- Python 3.10 or newer
- pip (or another Python package manager)
- Internet access on first run so `transformers` can download the `sshleifer/distilbart-cnn-12-6` model (~1 GB)
- Optional: [GNews API](https://gnews.io/) token for refreshing the dataset

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

Creating a virtual environment is recommended:

```bash
python -m venv .venv
.venv\Scripts\activate  # PowerShell / cmd on Windows
source .venv/bin/activate  # bash/zsh on Linux or macOS
```

---

## Local Setup

1. (Optional) Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Ensure `news_articles.db` exists. If you're starting from scratch, see **Refresh the dataset** below.
4. Run the API:
   ```bash
   python src/Disgest_Summerizer/app.py
   ```
   By default, the app looks for `news_articles.db` inside `src/Disgest_Summerizer`. Override the location by setting the `NEWS_DB_PATH` environment variable before starting the server.
5. Visit `http://127.0.0.1:5000/api/articles` or use `curl` to verify the API:
   ```bash
   curl "http://127.0.0.1:5000/api/articles?category=technology"
   ```

When run for the first time, the Hugging Face model will be downloaded and cached automatically.

---

## Refresh the Dataset

There are two main scripts under `src/Disgest_Summerizer/data/`:

- `script_getNewto_Json.py` fetches fresh headlines from the GNews API.
  1. Provide a valid token by editing the script or exporting `GNEWS_API_KEY`.
  2. Run `python src/Disgest_Summerizer/data/script_getNewto_Json.py`.
  3. The script writes a timestamped JSON file containing the fetched articles.

- `DataNews_source.py` reads `DataNews.json` (or another JSON file), scrapes any missing article body text, generates summaries, and stores everything in SQLite.
  ```bash
  python src/Disgest_Summerizer/data/DataNews_source.py
  ```
  The script creates or updates `news_articles.db`. Set `NEWS_DB_PATH` to write to a custom location:
  ```powershell
  $env:NEWS_DB_PATH = "C:\path\to\news.db"
  python src/Disgest_Summerizer/data/DataNews_source.py
  ```
  Expect each run to take a few minutes while scraping and summarizing articles.

---

## API Reference

### `GET /api/articles`

List articles sorted by `publishedAt` descending. Optional query parameters:

| Parameter | Type   | Default | Description                            |
|-----------|--------|---------|----------------------------------------|
| `category`| string | `all`   | Filter by category (e.g. `technology`) |

Successful responses return:

```json
{
  "articles": [
    {
      "id": "article-1",
      "title": "First headline",
      "author": "Author One",
      "source": {"name": "Source A"},
      "image": "https://example.com/image.jpg",
      "url": "https://example.com/1",
      "publishedAt": "2025-01-01T10:00:00Z",
      "content": "Full article text...",
      "summary": "AI generated summary...",
      "likes": 5,
      "comments": 1,
      "shares": 0,
      "saved": false,
      "category": "technology"
    }
  ]
}
```

If no summary is available, the API returns `"Summary not available."` for that article.

---

## Testing

Run the automated tests with:

```bash
pytest
```

The test suite spins up the Flask app against an in-memory SQLite database populated with fixtures and verifies sorting, filtering, and default summary behaviour.

---

## Docker

Build and run the service in a container:

```bash
docker build -t news-digest .
docker run --rm -p 5000:5000 news-digest
```

Mount a custom database by binding a volume and setting `NEWS_DB_PATH`:

```bash
docker run --rm -p 5000:5000 ^
  -e NEWS_DB_PATH=/data/news_articles.db ^
  -v C:\path\to\local.db:/data/news_articles.db ^
  news-digest
```

---

## Front-End Demo

- Start the Flask API.
- Open `src/Disgest_Summerizer/Web/NewWeb.html` in a browser.
- Confirm the JavaScript fetch URL points to your running API (defaults to `http://127.0.0.1:5000/api/articles`).

---

## Troubleshooting

- **Model download hangs**: verify your internet connection and rerun the script; the first download can take several minutes.
- **`transformers` or `torch` installation issues**: install the appropriate wheel from [pytorch.org](https://pytorch.org/get-started/locally/).
- **Scraping errors**: some publishers block automated requests. Reduce frequency or adjust the User-Agent header in `fetch_article_content`.
- **Port already in use**: start Flask on another port, e.g. `python src/Disgest_Summerizer/app.py --port 5050` after updating the script or using `flask run`.

---

## Contributing

Bug reports, feature requests, and pull requests are welcome. Please describe the change, include relevant tests when possible, and call out any new dependencies.

No explicit license is currently included; add one if you plan to distribute modifications.
