import os
import sqlite3
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
    app = Flask(__name__, template_folder="Web")
    CORS(app)

    default_db_path = os.path.join(os.path.dirname(__file__), DEFAULT_DB_NAME)
    env_db_path = os.getenv("NEWS_DB_PATH")
    if env_db_path:
        default_db_path = env_db_path
    app.config["DB_PATH"] = default_db_path

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

    return app


app = create_app()
print("--- Attempting to start Flask Server ---")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
