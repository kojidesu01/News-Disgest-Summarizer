from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

# ... (โค้ด Flask และฟังก์ชัน dict_factory เดิม) ...
# *************use python app.py run server python flask******************
app = Flask(__name__)
CORS(app) 
DB_NAME = 'news_articles.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/articles', methods=['GET'])
def get_articles():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = dict_factory 
    cursor = conn.cursor()

    category = request.args.get('category', 'all')
    
    # ดึงข้อมูลจากฐานข้อมูล
    if category == 'all':
        query = "SELECT * FROM articles ORDER BY publishedAt DESC"
        cursor.execute(query)
    else:
        query = "SELECT * FROM articles WHERE category = ? ORDER BY publishedAt DESC"
        cursor.execute(query, (category,))
    
    articles = cursor.fetchall()
    conn.close()

    # จัดโครงสร้างข้อมูลให้กลับไปเหมือน JSON เดิมที่ Frontend คาดหวัง
    formatted_articles = [
        {
            'id': article['id'],
            'title': article['title'],
            'author': article['author'],
            # นี่คือส่วนสำคัญที่จัดโครงสร้าง source ใหม่ให้ตรงกับ JS
            'source': {'name': article['source_name']}, 
            'image': article['image'],
            'url': article['url'],
            'publishedAt': article['publishedAt'],
            'content': article['content'],
            'likes': article['likes'],
            'comments': article['comments'],
            'shares': article['shares'],
            'saved': bool(article['saved']),
            'category': article['category'],
        }
        for article in articles
    ]
    
    return jsonify({"articles": formatted_articles}) 
print("--- Attempting to start Flask Server ---") 

if __name__ == '__main__':
    app.run(debug=True, port=5000)