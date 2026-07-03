import os
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

URL = "https://info.monsterhunter.com/wilds/event-quest/zh-hant/schedule"

headers = {
    "User-Agent": "Mozilla/5.0"
}

resp = requests.get(URL, headers=headers)
soup = BeautifulSoup(resp.text, "lxml")

# 找所有週期區塊（本週 / 下週 / 下下週）
sections = soup.find_all("section")

if len(sections) < 3:
    raise Exception("抓不到足夠的週期區塊，網站結構可能改了")

# 👉 只取「下下週」
target = sections[2]

items = target.find_all("li")

results = []

for item in items:
    text = item.get_text("\n", strip=True)
    results.append(text)

message = "📅 下下週限定活動任務\n\n" + "\n\n────────────────\n\n".join(results)

requests.post(
    WEBHOOK,
    json={"content": message}
)
