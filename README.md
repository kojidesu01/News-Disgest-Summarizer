# 📰 News Digest Summarizer

Collect, clean, and summarize the latest news into a compact dataset and a simple REST API that any front-end can consume.  
The project integrates **web scraping**, the **GNews API**, and a **Hugging Face transformer summarizer**, then serves curated stories from a **SQLite** database through a **Flask backend**.

---

## 🚀 Features

- **End-to-end pipeline** — fetch raw headlines, scrape full articles, generate AI summaries, and persist results.  
- **REST API** powered by Flask, with optional category filtering.  
- **SQLite Database** (`news_articles.db`) pre-seeded with sample data.  
- **Utility Scripts** for regenerating datasets (`script_getNewto_Json.py`) and rebuilding the database (`DataNews_source.py`).  
- **Static Front-End Demo** (`Web/NewWeb.html`) — adaptable into a complete UI.

---

## 📂 Project Structure

```text
src/Disgest_Summerizer/
├── app.py                   # Flask REST API
├── data/
│   ├── DataNews.json        # Sample article payload
│   ├── DataNews_source.py   # Imports JSON into SQLite with summaries
│   ├── Web_Scraping_script.py
│   └── script_getNewto_Json.py
├── news_articles.db         # SQLite store used by the API
└── Web/
    └── NewWeb.html          # Prototype front-end
```

---

## 🧰 Requirements

- **Python** 3.10 or newer  
- **Dependencies**  
  ```bash
  pip install flask flask-cors requests beautifulsoup4 transformers torch sentencepiece huggingface-hub
  ```
- Internet access required for the first model download (~1 GB, when loading `sshleifer/distilbart-cnn-12-6`)

> 💡 Tip: Create a virtual environment before installing
> ```bash
> python -m venv .venv
> .venv\Scripts\activate
> ```

---

## ⚡ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/kojidesu01/News-Disgest-Summarizer
   cd News-Disgest-Summarizer
   ```

2. **Set up the environment**
   - Activate the virtual environment and install dependencies (see above).

3. **(Optional) Fetch new articles**
   - Open `src/Disgest_Summerizer/data/script_getNewto_Json.py`
   - Add your GNews API key (`api_key`) or use environment variable:
     ```python
     import os
     api_key = os.getenv("GNEWS_API_KEY")
     ```
   - Run:
     ```bash
     python src/Disgest_Summerizer/data/script_getNewto_Json.py
     ```
   - Update `DataNews.json` or point `DataNews_source.py` to your new JSON.

4. **Rebuild the SQLite database**
   ```bash
   python src/Disgest_Summerizer/data/DataNews_source.py
   ```
   This script:
   - Loads article JSON  
   - Scrapes article body text  
   - Generates AI summaries  
   - Inserts all into `news_articles.db`

5. **Run the API**
   ```bash
   python src/Disgest_Summerizer/app.py
   ```

6. **Test the API**
   ```bash
   curl "http://127.0.0.1:5000/api/articles?category=technology"
   ```

---

## 🔗 API Reference

### `GET /api/articles`

| Parameter | Type | Default | Description |
|------------|------|----------|-------------|
| `category` | string | `"all"` | Filter results by article category |

**Response Example**
```json
{
  "articles": [
    {
      "id": "abc123",
      "title": "Headline text",
      "author": "Byline or Unknown",
      "source": { "name": "Reuters" },
      "image": "https://...",
      "url": "https://...",
      "publishedAt": "2025-10-07T12:00:00Z",
      "content": "Full scraped body ...",
      "summary": "Short AI-generated digest ...",
      "likes": 0,
      "comments": 0,
      "shares": 0,
      "saved": false,
      "category": "technology"
    }
  ]
}
```
> 🧠 If summarization fails, `"summary": "Summary not available."`

---

## 🧪 Data Pipeline Overview

| Script | Purpose |
|--------|----------|
| **`script_getNewto_Json.py`** | Fetch top headlines from [GNews API](https://gnews.io/) and save as JSON |
| **`Web_Scraping_script.py`** | Extract full article text from URLs |
| **`DataNews_source.py`** | Scrape → Summarize → Store into `news_articles.db` |
| **`app.py`** | Serve REST API endpoint |
| **`Web/NewWeb.html`** | Minimal front-end that fetches data from API |

⚙️ The summarizer uses Hugging Face model  
`sshleifer/distilbart-cnn-12-6` (DistilBART).

---

## 💻 Front-End Prototype

- Open `src/Disgest_Summerizer/Web/NewWeb.html` in a browser.
- Ensure the Flask API is running at `http://127.0.0.1:5000/api/articles`.
- Adjust the URL in JS fetch calls if needed.

---

## 🧩 Troubleshooting

| Issue | Possible Fix |
|--------|---------------|
| **Model download stuck** | Check internet & run `transformers-cli download` |
| **OSError: [Errno 98] Address already in use** | Change Flask port |
| **Scraping error** | Reduce request frequency / change User-Agent |
| **Torch install error** | Install correct PyTorch wheel from [pytorch.org](https://pytorch.org/get-started/locally/) |

---

## 📚 Contributing

This project was developed as coursework for  
**CP352301 – Script Programming**

Contributions are welcome!  
Fork the repo, make your changes, and open a pull request with:
- Short description of changes  
- Note any new dependencies

---

## 🗂 Repository Snapshot

```
News-Disgest-Summarizer/
├─ .git/
├─ .gitignore
├─ README.md
└─ src/
   └─ Disgest_Summerizer/
      ├─ app.py
      ├─ data/
      │  ├─ DataNews.json
      │  ├─ DataNews_source.py
      │  ├─ script_getNewto_Json.py
      │  └─ Web_Scraping_script.py
      ├─ news_articles.db
      └─ Web/
         └─ NewWeb.html
```

---

🧾 **License:** MIT (if applicable)
