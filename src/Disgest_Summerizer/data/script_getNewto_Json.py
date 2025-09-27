import requests
import json


api_key = "pub_d19d4404b0ed4d34a5b25c41f67aeaed"


url = f"https://newsdata.io/api/1/latest?apikey={api_key}"


response = requests.get(url)
data = response.json()


if data.get("status") == "success":
   
    with open("News.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
