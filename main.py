import os
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

WORKER_URL = "https://mhwilds-discord.toptoonisgood5.workers.dev"

response = requests.get(WORKER_URL, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

print("✅ HTML 取得成功")

rows = soup.select("tr")

print(f"找到 {len(rows)} 個 tr")

for i, row in enumerate(rows):

    level = row.select_one("td.level")
    title = row.select_one(".title span")
    overview = row.select_one("td.overview")

    if level is None or title is None or overview is None:
        continue

    print("=" * 60)
    print(f"第 {i} 筆")
    print("Level:", level.get_text(strip=True))
    print("Title:", title.get_text(strip=True))
    print("Overview:")
    print(overview.get_text("\n", strip=True))

    # 只印第一筆
    break
