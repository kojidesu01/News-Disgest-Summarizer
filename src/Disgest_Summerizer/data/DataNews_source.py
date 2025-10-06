import sqlite3
import json
import os

DB_NAME = 'news_articles.db'
JSON_FILE = 'data/DataNews.json' 

def import_data():
    if not os.path.exists(JSON_FILE):
        print(f"❌ Error: JSON file not found at {JSON_FILE}")
        return

    # 1. เชื่อมต่อฐานข้อมูล (ถ้าไม่มีไฟล์นี้จะถูกสร้างขึ้นมาใหม่)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 2. สร้างตาราง articles
    # เราจะเก็บข้อมูลที่ซับซ้อน (เช่น source, likes, category) เป็น JSON string
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            author TEXT,
            source_name TEXT,
            image TEXT,
            url TEXT,
            publishedAt TEXT,
            content TEXT,
            likes INTEGER,
            comments INTEGER,
            shares INTEGER,
            saved BOOLEAN,
            category TEXT
        )
    """)
    print("✅ Table 'articles' ensured.")

    # 3. อ่านและโหลดข้อมูล JSON
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # ตรวจสอบว่าโครงสร้าง JSON มี key 'articles' หรือไม่
            articles = data.get('articles', data) 
            
    except Exception as e:
        print(f"❌ Error reading or parsing JSON: {e}")
        return

    # 4. แทรกข้อมูลลงในตาราง
    for article in articles:
        # กำหนดค่าเริ่มต้น/แปลงค่าให้พร้อมสำหรับ SQLite
        article_data = {
            'id': article.get('id') or os.urandom(16).hex(), # ใช้ ID หรือสร้างใหม่
            'title': article.get('title', 'Untitled'),
            'author': article.get('author') or article.get('source', {}).get('name') or 'Unknown',
            'source_name': article.get('source', {}).get('name') or article.get('source') or 'Unknown',
            'image': article.get('urlToImage') or article.get('image') or 'No Image',
            'url': article.get('url', '#'),
            'publishedAt': article.get('publishedAt') or '2023-01-01T00:00:00Z',
            'content': article.get('content') or article.get('description') or 'No content available.',
            # สามารถกำหนดค่าเริ่มต้นสำหรับตัวเลขได้
            'likes': article.get('likes', 0),
            'comments': article.get('comments', 0),
            'shares': article.get('shares', 0),
            'saved': 0, # ใช้ 0/1 สำหรับ Boolean ใน SQLite
            'category': article.get('source', {}).get('category') or article.get('category') or 'news'
        }

        try:
            cursor.execute("""
                INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article_data['id'], article_data['title'], article_data['author'], article_data['source_name'],
                article_data['image'], article_data['url'], article_data['publishedAt'], article_data['content'],
                article_data['likes'], article_data['comments'], article_data['shares'],
                article_data['saved'], article_data['category']
            ))
        except sqlite3.IntegrityError:
            print(f"⚠️ Skipped duplicate ID: {article_data['id']}")
            
    conn.commit()
    conn.close()
    print(f"✅ Data imported successfully! Total articles: {len(articles)} in {DB_NAME}")

if __name__ == '__main__':
    import_data()