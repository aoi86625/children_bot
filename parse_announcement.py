from bs4 import BeautifulSoup

with open("gamba_announcement.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
base_url = "https://gamba-osaka-academy.hacomono.jp"
results = []

cards = soup.select("a[href^='/announcement/']")

for card in cards:
    title_tag = card.select_one(".card_title")
    date_tag = card.select_one(".card_date")

    if not (title_tag and date_tag):
        continue

    title = title_tag.text.strip()
    published_at = date_tag.text.strip()
    url = base_url + card["href"]

    results.append({
        "title": title,
        "published_at": published_at,
        "url": url
    })

# 出力確認
for item in results:
    print("📌", item["published_at"], "-", item["title"])
    print("🔗", item["url"])
    print()
