# News Digest Summarizer

An AI-assisted news digest that fetches articles, generates summaries, stores them in SQLite, and serves them through a Flask API with a Tailwind-based front-end.

---

## Live Demo
- Web app: https://news-disgest-summarizer.onrender.com

---

## Key Features
- Automated pipeline: scrape -> summarize (Hugging Face `distilbart-cnn-12-6`) -> persist -> serve
- Flask API (`/api/articles`) with optional `category` filtering
- Built-in responsive front-end (`src/Disgest_Summerizer/Web/NewWeb.html`)
- Ready-to-run Docker image and Render deployment setup
- SQLite database (`news_articles.db`) bundled for quick demos

---

## Project Structure
- `src/Disgest_Summerizer/app.py` - Flask app and API routes
- `src/Disgest_Summerizer/news_articles.db` - bundled SQLite database
- `src/Disgest_Summerizer/data/` - scraping and summarisation scripts
- `src/Disgest_Summerizer/Web/NewWeb.html` - static front-end
- `tests/` - pytest suite
- `Dockerfile`, `requirements.txt`, `README.md`

---

## Getting Started

### Prerequisites
- Python 3.10 or newer
- pip
- (Optional) virtualenv or venv

### Installation
```bash
git clone https://github.com/<your-repo>/News-Digest-Summarizer.git
cd News-Digest-Summarizer
python -m venv .venv
.venv\Scripts\activate           # Windows
# source .venv/bin/activate      # macOS/Linux
pip install -r requirements.txt
```
### Important requirement
- DLL for pytorch : https://gist.github.com/opentechnologist/0fa93f92d4c42535bb8cbe539e36c080

### Run Locally
```bash
python src/Disgest_Summerizer/app.py
```
Visit http://127.0.0.1:5000 for the front-end, or http://127.0.0.1:5000/api/articles for raw JSON.

The app reads `NEWS_DB_PATH` (defaults to `/app/src/Disgest_Summerizer/news_articles.db` inside Docker or the relative path when running locally). Set a custom path if you mount a different database.

---

## Updating the Dataset
1. Fetch fresh headlines:  
   `python src/Disgest_Summerizer/data/script_getNewto_Json.py`
2. Summarise and rebuild SQLite:  
   `python src/Disgest_Summerizer/data/DataNews_source.py`

The generated records are inserted into `news_articles.db` and will be served automatically on next start.

---

## API Reference

### GET `/api/articles`
Returns all articles (latest first by default).

Query params:
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `category` | string | `all` | Filter by category (e.g. `technology`, `sports`) |

Example response:
```json
{
  "articles": [
    {
      "id": "d3d9...",
      "title": "AI Breakthrough in 2025",
      "source": {"name": "TechCrunch"},
      "summary": "AI model achieves new milestone...",
      "category": "technology",
      "publishedAt": "2025-10-08T12:00:00Z"
    }
  ]
}
```

---

## Docker Workflow
The Dockerfile uses a two-stage build. Torch wheels are pulled from the official CPU index to avoid long compile times.

Build and run:
```bash
docker build -t news-digest .
docker run --rm -p 5000:5000 news-digest
```

Mount a custom database:
```bash
docker run --rm -p 5000:5000 ^
  -e NEWS_DB_PATH=/data/news_articles.db ^
  -v %cd%\\news_articles.db:/data/news_articles.db ^
  news-digest
```

Linux/macOS replace the caret lines with `\` and `%cd%` with `$(pwd)`.

---

## Render Deployment Notes
1. Push to GitHub (or connect repo directly).
2. Create a Render Web Service pointing to the repo root.
3. Build command: `docker build -t news-digest .` (Render autodetects Dockerfile).
4. Start command (matching Docker CMD): `python src/Disgest_Summerizer/app.py`
5. Environment variables:
   - `NEWS_DB_PATH=/app/src/Disgest_Summerizer/news_articles.db` (for free tier without persistent disk)
   - Render supplies `PORT`; no need to set manually.
6. Redeploy. Logs show `[BOOT] Using DB_PATH = ... | exists = True` when the database is detected.

If you upgrade to a plan with persistent disk, mount it (for example `/var/data/news_articles.db`) and copy the bundled DB there at startup before launching the app.

---

## Testing
Run the pytest suite:
```bash
pytest
```

---

## Troubleshooting
| Issue | Fix |
|-------|-----|
| Long Docker build times | Torch is pinned to a pre-built wheel via `--index-url`; ensure you have network access. |
| API returns empty list | Confirm `news_articles.db` contains data and `NEWS_DB_PATH` points to it. |
| Front-end cannot fetch in production | The script now auto-detects origin; ensure CORS is enabled (Flask-CORS already configured). |
| Database changes lost on Render free tier | Copy the DB to `/tmp` at start or upgrade to persistent disk. |

---

## License
Educational use only. Add a formal license (e.g. MIT) if you distribute modified versions.

---

_"Read less, know more."_ 
