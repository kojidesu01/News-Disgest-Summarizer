# 🗞️ News Digest Summarizer

> “Read less, know more.” — AI-powered news digest app that fetches, summarizes, and serves trending headlines in seconds.

---

## Project walkthrough video :
Link : https://drive.google.com/file/d/1XWelyt957LnPKjXjMN2QxgFnhA-lfhhC/view?usp=drive_link

---

## 🌍 Live Demo  
🔗 **[https://news-digest-summarizer.onrender.com](https://news-digest-summarizer.onrender.com)**  
📰 Try the API: [https://news-digest-summarizer.onrender.com/api/articles](https://news-digest-summarizer.onrender.com/api/articles)

---

## 📖 Overview
**News Digest Summarizer** automatically collects breaking news, extracts full text, and summarizes it with a **Hugging Face AI model**.  
The summarized results are stored in **SQLite** and exposed through a lightweight **Flask API**, with a built-in static front-end for demo use.

---

## ✨ Features

✅ **End-to-end pipeline** — Fetch → Scrape → Summarize → Store → Serve  
✅ **Flask REST API** with JSON output and category filtering  
✅ **SQLite database** for persistence (portable, easy to deploy)  
✅ **Hugging Face Summarization Model** (`distilbart-cnn-12-6`)  
✅ **Front-end HTML demo** (`Web/NewWeb.html`)  
✅ **Docker + Render deployment ready**

---

## 🧩 Project Structure
```bash
News-Digest-Summarizer/
├── src/
│   └── Disgest_Summerizer/
│       ├── app.py                # Flask app exposing /api/articles and serving HTML
│       ├── news_articles.db      # SQLite database with summarized news
│       ├── data/
│       │   ├── DataNews.json
│       │   ├── DataNews_source.py
│       │   ├── Web_Scraping_script.py
│       │   └── script_getNewto_Json.py
│       └── Web/
│           └── NewWeb.html       # Static demo webpage
├── tests/                        # Pytest test suite
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 🔹 Requirements
- Python ≥ 3.10  
- pip package manager  
- Internet connection (first run only, to download model)  
- Optional — [GNews API](https://gnews.io/) token for live fetch

### 🔹 Installation
```bash
git clone https://github.com/<your-repo>/News-Digest-Summarizer.git
cd News-Digest-Summarizer
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

---

## ▶️ Run Locally

```bash
python src/Disgest_Summerizer/app.py
```

Visit 👉 [http://127.0.0.1:5000/api/articles](http://127.0.0.1:5000/api/articles)  
or open the front-end 👉 `src/Disgest_Summerizer/Web/NewWeb.html`

> The app automatically loads `news_articles.db` in the same folder.  
> Set a custom path with the environment variable `NEWS_DB_PATH`.

---

## 🔁 Refresh Dataset

### 📰 1. Fetch new headlines  
```bash
python src/Disgest_Summerizer/data/script_getNewto_Json.py
```

### 🧠 2. Summarize & rebuild database  
```bash
python src/Disgest_Summerizer/data/DataNews_source.py
```

🕐 Takes a few minutes — downloads articles, runs summarization, and stores them in SQLite.

---

## 🧠 API Reference

### `GET /api/articles`
Return a list of summarized news articles.

| Parameter | Type | Default | Description |
|------------|------|----------|-------------|
| `category` | str  | all      | Filter by category (`technology`, `sports`, etc.) |

**Example Response**
```json
{
  "articles": [
    {
      "id": 1,
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

## 🧪 Testing
Run all unit tests with **pytest**:
```bash
pytest
```
Tests include API responses, category filtering, and SQLite integration.

---

## 🐳 Docker (Optional)
Build & run the service in a container:
```bash
docker build -t news-digest .
docker run --rm -p 5000:5000 news-digest
```

Mount a custom database:
```bash
docker run --rm -p 5000:5000   -e NEWS_DB_PATH=/data/news_articles.db   -v $(pwd)/news_articles.db:/data/news_articles.db   news-digest
```

---

## 🌐 Deploy on Render

1. Push to GitHub  
2. Create a **Render Web Service**  
3. Build Command → `pip install -r requirements.txt`  
4. Start Command → `python src/Disgest_Summerizer/app.py`  
5. Add Environment Variable  
   ```
   KEY: NEWS_DB_PATH
   VALUE: /opt/render/project/src/src/Disgest_Summerizer/news_articles.db
   ```
6. Wait for “✅ Live” → Open your public URL!

---

## 💻 Front-End Demo
- Uses vanilla JS to fetch from `/api/articles`  
- Dynamic category filter + instant rendering  
- Works with any Flask endpoint or hosted API URL  

To preview:
```bash
open src/Disgest_Summerizer/Web/NewWeb.html
```

---

## 🧰 Troubleshooting

| Problem | Solution |
|----------|-----------|
| **Model download too slow** | Pre-generate summaries on local machine, then upload the ready SQLite DB |
| **Database empty** | Ensure `news_articles.db` has table `articles` with records |
| **Port already used** | Run `python app.py --port 5050` or set `$PORT` |
| **CORS blocked** | `Flask-CORS` already enabled — ensure JS fetches the correct domain |

---

## 👥 Team Members

| Name | Role | Responsibility |
|------|------|----------------|
| **บอส** | Project Manager / CI-CD | Repository setup · GitHub Actions · Render deployment |
| **โชกุน** | Automated Tester / QA | Pytest · Mock API · Lint · Code quality |
| **โฟน** | Core Developer | Flask API · SQLite schema · Hugging Face integration |

---

## 🧩 Evaluation Checklist
✅ API works (GET/POST + error handling)  
✅ Data persisted correctly (SQLite)  
✅ Code follows PEP 8 (Flake8 clean)  
✅ Tests run successfully (pytest)  
✅ CI/CD simulated via Render deploy  
✅ README includes setup + usage guide  
✅ Team roles documented  

---

## 📚 References
- [NewsData.io API](https://newsdata.io/documentation)  
- [Hugging Face Transformers](https://huggingface.co/docs)  
- [Flask Framework](https://flask.palletsprojects.com)  
- [Pytest Docs](https://docs.pytest.org/)  
- [Render Deployment Guide](https://render.com/docs)

---

## 📄 License
This project is open for educational use.  
Add an MIT License if distributing modified versions.

---
> _“Less noise, more insight — stay informed with AI-curated news.”_
