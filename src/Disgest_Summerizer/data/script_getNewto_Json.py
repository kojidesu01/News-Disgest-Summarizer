import requests
import json
import os

url = f"https://newsdata.io/api/1/latest?apikey=pub_2faf079e890947eda13836e421edb044&q=nepal"

response = requests.get(url)
data = response.json()

if data.get("status") == "success":
    new_results = data.get("results", [])

    # โหลดข่าวเก่าจากไฟล์ ถ้ามีอยู่
    if os.path.exists("News.json"):
        with open("News.json", "r", encoding="utf-8") as f:
            try:
                old_data = json.load(f)
                old_results = old_data.get("results", [])
            except json.JSONDecodeError:
                old_results = []
    else:
        old_results = []

    # สร้างเซตของลิงก์ข่าวเก่า เพื่อใช้ตรวจสอบความซ้ำ
    existing_links = set(article.get("link") for article in old_results if article.get("link"))

    # คัดข่าวใหม่ที่ไม่ซ้ำ
    unique_new_results = [article for article in new_results if article.get("link") not in existing_links]

    # รวมข่าวทั้งหมด
    combined_results = old_results + unique_new_results

    # เขียนกลับลงไฟล์

    with open("News1.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

