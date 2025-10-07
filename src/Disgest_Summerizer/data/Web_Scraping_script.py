import requests
from bs4 import BeautifulSoup
import time
import json


JSON_FILE = 'data/DataNews.json'

def fetch_article_content(url):
    """
    ดึงเนื้อหาเต็มของบทความจาก URL ภายนอก
    """
    if not url or url == '#':
        return "No content available."

    try:
        # ⭐ สำคัญ: การตั้งเวลาหน่วง (Sleep) เพื่อไม่ให้ถูกบล็อกโดยเว็บไซต์
        time.sleep(1) # หน่วง 1 วินาทีต่อบทความ
        
        # ตั้ง User-Agent เพื่อปลอมตัวเป็นเบราว์เซอร์จริง
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise exception สำหรับ HTTP error (4xx or 5xx)

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 💡 Web Scraping Tips: 
        # ส่วนใหญ่เนื้อหาหลักจะอยู่ในแท็ก <p> ภายในแท็กหลัก (main, article)
        
        # ลองหาเนื้อหาในแท็กหลัก ๆ ที่คนส่วนใหญ่ใช้
        article_body = soup.find('article') or soup.find('main') or soup.find('body')
        
        if article_body:
            # ดึงข้อความทั้งหมดจากแท็ก <p> และรวมเข้าด้วยกัน
            paragraphs = [p.get_text(strip=True) for p in article_body.find_all('p')]
            
            # กรองย่อหน้าสั้น ๆ ที่อาจเป็นแค่ captions หรือเมนู
            full_text = '\n'.join([p for p in paragraphs if len(p) > 50])
            
            if full_text:
                return full_text
        
        return "Content extraction failed (generic)."

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Warning: Failed to fetch URL {url}. Error: {e}")
        return "Content fetch error."
    except Exception as e:
        return "An unexpected error occurred during parsing."



with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            urls = data.get('url', data) 

for url in urls:
     fetch_article_content(url)

