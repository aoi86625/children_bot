from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv

# .envから環境変数を読み込む
load_dotenv()
EMAIL = os.getenv("GAMBA_EMAIL")
PASSWORD = os.getenv("GAMBA_PASSWORD")

if not EMAIL or not PASSWORD:
    print("⚠️ .envからGAMBA_EMAIL または GAMBA_PASSWORD が取得できません。")
    exit()

LOGIN_URL = "https://gamba-osaka-academy.hacomono.jp/home"
ANNOUNCEMENT_URL = "https://gamba-osaka-academy.hacomono.jp/announcement"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("✅ サイトにアクセス中...")
    page.goto(LOGIN_URL)

    page.click("text=ログイン")
    page.wait_for_selector("input[type='email']", timeout=10000)
    print("✅ ログイン情報を入力中...")
    page.fill("input[type='email']", EMAIL)
    page.fill("input[type='password']", PASSWORD)

    print("✅ ログインボタンをクリック...")
    page.evaluate("""
        () => {
            const btn = document.querySelector('button[type="submit"]');
            if (btn) btn.click();
        }
    """)

    print("⏳ お知らせリンクの出現を待機中...")
    page.wait_for_timeout(5000)

    print("📄 お知らせページへ移動中...")
    page.goto(ANNOUNCEMENT_URL)
    page.wait_for_load_state("networkidle")

    html = page.content()
    with open("gamba_announcement_dynamic.html", "w", encoding="utf-8") as f:
        f.write(html)

    page.screenshot(path="gamba_announcement_dynamic.png")
    print("✅ お知らせページの動的HTML取得完了！")

    browser.close()
