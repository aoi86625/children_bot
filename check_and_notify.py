import json
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_BROADCAST_URL = "https://api.line.me/v2/bot/message/broadcast"

LAST_FILE = "last_announcement.json"
CURRENT_FILE = "gamba_announcement_dynamic.html"

# HTMLから最新お知らせを抽出
def extract_latest_announcement(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    card = soup.select_one("a[href^='/announcement/']")
    if not card:
        return None

    title_tag = card.select_one(".card_title")
    date_tag = card.select_one(".card_date")
    if not title_tag or not date_tag:
        return None

    return {
        "title": title_tag.text.strip(),
        "published_at": date_tag.text.strip(),
        "url": "https://gamba-osaka-academy.hacomono.jp" + card["href"]
    }

# Broadcastで通知送信
def send_line_broadcast(announcement):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [
            {
                "type": "text",
                "text": f"📢 新着お知らせ！\n{announcement['title']}\n{announcement['published_at']}\n{announcement['url']}"
            }
        ]
    }
    response = requests.post(LINE_BROADCAST_URL, headers=headers, json=data)
    print("✅ LINE Broadcast通知送信", response.status_code)

# 差分チェックと保存
def main():
    new_announcement = extract_latest_announcement(CURRENT_FILE)
    if not new_announcement:
        print("⚠️ お知らせが見つかりませんでした")
        return

    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, "r", encoding="utf-8") as f:
            old_announcement = json.load(f)
    else:
        old_announcement = {}

    if new_announcement != old_announcement:
        print("🔔 新着あり → 通知＆保存")
        send_line_broadcast(new_announcement)
        with open(LAST_FILE, "w", encoding="utf-8") as f:
            json.dump(new_announcement, f, ensure_ascii=False, indent=2)
    else:
        print("✅ お知らせは更新されていません")

if __name__ == "__main__":
    main()
