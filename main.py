import os
import requests

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

message = """📅 本週限定活動任務

★4　在晚飯之時點火
原野：天塹沙原
承接／參加條件：HR 9 以上
完成條件：狩獵炎尾龍
發佈開始時間：2026.07.01 08:00
發佈結束時間：2026.07.08 07:59
"""

requests.post(
    WEBHOOK,
    json={
        "content": message
    }
)
