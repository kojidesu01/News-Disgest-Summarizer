

# News Disgest Summarizer

โปรแกรม **News Disgest Summarizer** เป็นโปรแกรมรันบน Command Line สำหรับรวบรวมข่าว และสรุปข่าว

โปรเจกต์นี้เป็นงาน **Final Project** ของรายวิชา **CP352301 Script Programming** ภาคเรียนที่ 1 ปีการศึกษา 2568  

---

## 📌 ฟีเจอร์ (Features)
- ใส่ข้อมูลเพิ่มเติม

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```bash
NEWS-DISGEST-SUMMERIZER/
├── docs/ # เอกสารโปรเจกต์
│ ├── PLAN.md # แผนงาน (สัปดาห์/ฟีเจอร์)
│ └── PROGRESS.md # ความคืบหน้า/Log การพัฒนา
│
├── src/ # ซอร์สโค้ดหลัก
│ ├── main.py # entry point ของโปรแกรม
│ ├── News_source.py # ฟังก์ชันในการดึงข้อมูลของข่าวจาก News.json
│ └── data/
│      └── News.json # ไฟล์ json ที่ราบรวมข่าว
│      └── script_requestNewTo_Json.py # ฟังก์ชันในการดึงข้อมูลจาก Newsdata.io API
│
├── .gitignore # รายการไฟล์/โฟลเดอร์ที่ไม่ต้อง track ด้วย Git
└── README.md # คำอธิบายโปรเจกต์ (วิธีใช้งาน, ฟีเจอร์ ฯลฯ)
```

---

## ⚙️ วิธีการติดตั้งและใช้งาน (Installation & Usage)

### 1. โคลนโปรเจกต์จาก GitHub
```bash
git clone https://github.com/kojidesu01/News-Disgest-Summarizer
cd NEWS-DISGEST-SUMMERIZER
```
### 2. รันโปรแกรมหลัก
```bash
python main.py
```

### 3. เมนูโปรแกรม
 * กด 1 → สุ่มข้อความและเริ่มทดสอบการพิมพ์
 * กด 2 → ออกจากโปรแกรม

---

## 👨‍💻 ผู้พัฒนา (Contributors)

- นายปวริศช์ ประมวล 673380278-9 sec1  
- นายธนภูมิ จันทรา 673380272-1 sec1  
- นายธีรเมธ สายคำ 673380273-9 sec1  


