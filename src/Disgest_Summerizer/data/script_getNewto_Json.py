import requests
import json
import datetime

# 📰 ตั้งค่า API
api_key = "d3356e6e783319a0e277a3b83962d0a6"
category = "entertainment"  # หมวดข่าว เช่น: world, business, technology, sports, etc.
language = "en"
max_results = 6  # จำนวนข่าวสูงสุดที่จะดึงมา

# 🔗 URL API
url = f"https://gnews.io/api/v4/top-headlines?token={api_key}&topic={category}&lang={language}&max={max_results}"

# 📡 ดึงข้อมูลจาก API
response = requests.get(url)
data = response.json()

if response.status_code == 200:
    articles = data.get("articles", [])
    print(f"✅ ได้ข่าวทั้งหมด {len(articles)} ข่าว")

    # 🕒 ตั้งชื่อไฟล์ใหม่ทุกครั้งตามวันเวลา (เช่น News_2025-10-05_1930.json)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"News_{category}_{timestamp}.json"

    # 💾 บันทึกข่าวลงไฟล์ใหม่
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"articles": articles}, f, ensure_ascii=False, indent=2)

    print(f"💾 สร้างไฟล์ใหม่ชื่อ {filename} เรียบร้อยแล้ว")

else:
    print(f"❌ ดึงข้อมูลล้มเหลว (HTTP {response.status_code})")
    print("ข้อความตอบกลับ:", data)
