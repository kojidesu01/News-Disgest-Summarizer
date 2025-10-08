import os
import sqlite3
import threading
import webbrowser
from pathlib import Path
from flask import Flask, jsonify, request, current_app
from flask_cors import CORS

DEFAULT_DB_NAME = "news_articles.db"


def dict_factory(cursor, row):
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    return conn


def create_app(test_config=None):
    app = Flask(__name__, static_folder="Web", static_url_path="")
    CORS(app)

    # ตั้ง path DB ตามลำดับความสำคัญ
    # 1️⃣ ถ้ามี ENV (Render จะตั้งอัตโนมัติ) → ใช้
    # 2️⃣ ถ้าไม่มี ENV → ใช้ path ในเครื่องของคุณ
    env_db_path = os.getenv(
        "NEWS_DB_PATH",
        r"D:\PROJECT\News-Disgest-Summarizer\src\Disgest_Summerizer\news_articles.db"
    )

    # ตั้งค่า path ให้ Flask ใช้งาน
    app.config["DB_PATH"] = env_db_path

    # Debug log ตอนเริ่มต้น (จะเห็นใน console หรือ Render logs)
    print(f"[BOOT] Using DB_PATH = {env_db_path} | exists = {os.path.exists(env_db_path)}")

    if test_config:
        app.config.update(test_config)

    @app.route('/api/articles', methods=['GET'])
    def get_articles():
        category = request.args.get('category', 'all')
        db_path = current_app.config["DB_PATH"]

        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()

            if category == 'all':
                cursor.execute("SELECT * FROM articles ORDER BY publishedAt DESC")
            else:
                cursor.execute(
                    "SELECT * FROM articles WHERE category = ? ORDER BY publishedAt DESC",
                    (category,)
                )

            articles = cursor.fetchall()

        formatted_articles = [
            {
                'id': article['id'],
                'title': article['title'],
                'author': article['author'],
                'source': {'name': article['source_name']},
                'image': article['image'],
                'url': article['url'],
                'publishedAt': article['publishedAt'],
                'content': article['content'],
                'summary': article['summary'] if article.get('summary') else 'Summary not available.',
                'likes': article['likes'],
                'comments': article['comments'],
                'shares': article['shares'],
                'saved': bool(article['saved']),
                'category': article['category'],
            }
            for article in articles
        ]

        return jsonify({"articles": formatted_articles})
    
    from flask import send_from_directory

    @app.route('/')
    def serve_frontend():
        web_dir = Path(__file__).resolve().parent / "Web"
        return send_from_directory(web_dir, "NewWeb.html")

    return app


app = create_app()
print("--- Attempting to start Flask Server ---")


def open_frontend():
    """Open the frontend HTML file in the default browser once the server is up."""
    frontend_path = Path(__file__).resolve().parent / "Web" / "NewWeb.html"
    if frontend_path.exists():
        webbrowser.open_new_tab(frontend_path.as_uri())
    else:
        print(f"--- Frontend file not found at {frontend_path} ---")


if __name__ == '__main__':
    import os, threading
    from pathlib import Path

    port = int(os.environ.get("PORT", 5000))

    # เปิดหน้าเว็บเฉพาะตอนรันในเครื่อง
    if not os.environ.get("RENDER"):
        def open_frontend():
            web_path = Path(__file__).resolve().parent / "Web" / "NewWeb.html"
            import webbrowser
            if web_path.exists():
                webbrowser.open_new_tab(web_path.as_uri())
        timer = threading.Timer(1.0, open_frontend)
        timer.daemon = True
        timer.start()

    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
