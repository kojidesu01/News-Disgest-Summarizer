import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup
import time # ต้องใช้สำหรับ time.sleep()
from transformers import pipeline

SUMMARIZATION_MODEL = "sshleifer/distilbart-cnn-12-6"

# โหลดโมเดลเมื่อ Server เริ่มทำงาน
try:
    # 'cpu' สำคัญมากสำหรับโน้ตบุ๊ก RAM 8GB
    summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL, device='cpu')
    print(f"✅ AI Summarization model {SUMMARIZATION_MODEL} loaded successfully on CPU.")
except Exception as e:
    print(f"❌ ERROR: Failed to load AI model. Summarization will be skipped. Detail: {e}")
    summarizer = None
def get_ai_summary(text_content):
    """รับเนื้อหาบทความ (content) และส่งคืนบทสรุป"""
    # ตรวจสอบว่าโมเดลโหลดสำเร็จและเนื้อหามีความยาวพอ
    if not summarizer or not text_content or len(text_content) < 50:
        return "Summary not available."
    
    # โมเดลส่วนใหญ่รับ input ได้จำกัด (ประมาณ 1024 tokens หรือ ~4000 อักขระ)
    content_to_summarize = text_content[:4000]

    try:
        summary = summarizer(
            content_to_summarize, 
            max_length=200,  # ความยาวสูงสุดของบทสรุป
            min_length=40,   # ความยาวต่ำสุดของบทสรุป
            do_sample=False
        )
        return summary[0]['summary_text']
    except Exception as e:
        print(f"⚠️ Warning: Error during summarization: {e}") 
        return "Error summarizing article."

DB_NAME = 'news_articles.db'
JSON_FILE = 'data/DataNews.json' 

# ----------------------------------------------------
# A. ฟังก์ชัน Web Scraper
# ----------------------------------------------------
def fetch_article_content(url):
    """ดึงเนื้อหาเต็มของบทความจาก URL ภายนอก"""
    if not url or url == '#':
        return "No content available."

    try:
        # ⚠️ หน่วงเวลาเพื่อป้องกันการถูกบล็อก
        time.sleep(0.5) 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        # ลองหาเนื้อหาในแท็กหลัก ๆ
        article_body = soup.find('article') or soup.find('main') or soup.find('body')
        
        if article_body:
            paragraphs = [p.get_text(strip=True) for p in article_body.find_all('p')]
            # รวมย่อหน้าที่มีความยาวเกิน 50 อักขระ
            full_text = '\n'.join([p for p in paragraphs if len(p) > 50])
            return full_text if full_text else "Content extraction failed."
        
        return "Content extraction failed (no article/main tag found)."

    except requests.exceptions.RequestException as e:
        # print(f"⚠️ Warning: Failed to fetch URL {url}. Error: {e}")
        return "Content fetch error."
    except Exception as e:
        # print(f"⚠️ Warning: Unexpected error during parsing: {e}")
        return "An unexpected error occurred during parsing."

# ----------------------------------------------------
# B. ฟังก์ชันหลักสำหรับนำเข้าข้อมูล (ปรับแก้)
# ----------------------------------------------------
# ในไฟล์ DataNews_source.py

# ... (โค้ด import และฟังก์ชัน get_ai_summary/fetch_article_content) ...

# ----------------------------------------------------
# B. ฟังก์ชันหลักสำหรับนำเข้าข้อมูล (แก้ไขล่าสุด)
# ----------------------------------------------------
def import_data():
    # ตรวจสอบพาธ JSON (ถ้าไฟล์ Importer อยู่ใน data/ ต้องให้ไฟล์ JSON อยู่ใน data/ ด้วย)
    if not os.path.exists(JSON_FILE):
        print(f"❌ Error: JSON file not found at {JSON_FILE}")
        return
    
    # ⚠️ ลบไฟล์เก่าก่อนเพื่อให้มั่นใจว่ากำลังสร้าง DB ใหม่พร้อม summary
    try:
        os.remove(DB_NAME)
        print(f"🗑️ Removed old {DB_NAME} file.")
    except FileNotFoundError:
        pass

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # โค้ดสร้างตาราง ต้องมีคอลัมน์ summary TEXT
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY, title TEXT, author TEXT, source_name TEXT,
            image TEXT, url TEXT, publishedAt TEXT, content TEXT, summary TEXT,
            likes INTEGER, comments INTEGER, shares INTEGER, saved BOOLEAN, category TEXT
        )
    """)
    print("✅ Table 'articles' ensured.")

    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            articles = data.get('articles', data) 
            
    except Exception as e:
        print(f"❌ Error reading or parsing JSON: {e}")
        return

    # 4. แทรกข้อมูลลงในตาราง (พร้อม Scrape และ AI Summarization)
    total_articles = len(articles)
    print(f"Starting scraping and import of {total_articles} articles...")
    
    for i, article in enumerate(articles):
        article_url = article.get('url', '#')
        
        # 1. Scrape เนื้อหาเต็ม
        full_content = fetch_article_content(article_url)
        
        # 2. ⭐⭐ เรียกใช้ AI Summarizer และเก็บค่า ⭐⭐
        
        # ตรวจสอบว่า Scrape สำเร็จและเนื้อหามีความยาวพอ (100 อักขระ)
        if "Content fetch error." in full_content or "Content extraction failed." in full_content or len(full_content) < 100:
            summary_text = "Content too short or fetch failed, cannot summarize."
            print(f"[{i+1}/{total_articles}] ⚠️ Skipping summary for: {article.get('title', 'Untitled')[:30]}...")
        else:
            try:
                # ⚡ นี่คือการเรียกใช้และเก็บค่าที่ถูกต้อง
                summary_text = get_ai_summary(full_content) 
                print(f"[{i+1}/{total_articles}] Scraped: {article.get('title', 'Untitled')[:30]}... -> Summary length: {len(summary_text)} chars.")
            except Exception as e:
                summary_text = "Error during AI summarization."
                print(f"[{i+1}/{total_articles}] ❌ AI Error: {e}")
        
        # 3. กำหนดค่า/แปลงค่า
        article_data = {
            'id': article.get('id') or os.urandom(16).hex(), 
            'title': article.get('title', 'Untitled'),
            'author': article.get('author') or article.get('source', {}).get('name') or 'Unknown',
            'source_name': article.get('source', {}).get('name') or article.get('source') or 'Unknown',
            'image': article.get('urlToImage') or article.get('image') or 'No Image',
            'url': article_url,
            'publishedAt': article.get('publishedAt') or '2023-01-01T00:00:00Z',
            'content': full_content,
            'summary': summary_text, # ✅ ใช้ summary_text ที่มีบทสรุปจาก AI
            'likes': article.get('likes', 0),
            'comments': article.get('comments', 0),
            'shares': article.get('shares', 0),
            'saved': 0, 
            'category': article.get('source', {}).get('category') or article.get('category') or 'news'
        }

        try:
            # 4. INSERT INTO articles
            cursor.execute("""
                INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                article_data['id'], article_data['title'], article_data['author'], article_data['source_name'],
                article_data['image'], article_data['url'], article_data['publishedAt'], article_data['content'], article_data['summary'],
                article_data['likes'], article_data['comments'], article_data['shares'],
                article_data['saved'], article_data['category']
            ))
        except sqlite3.IntegrityError:
            print(f"⚠️ Skipped duplicate ID: {article_data['id']}")
            
    conn.commit()
    conn.close()
    print(f"✅ Data imported successfully! Total articles: {total_articles} in {DB_NAME}")

if __name__ == '__main__':
    import_data()