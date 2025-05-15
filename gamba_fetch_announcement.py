import asyncio
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv("GAMBA_EMAIL")
PASSWORD = os.getenv("GAMBA_PASSWORD")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("✅ サイトにアクセス中...")
        await page.goto("https://gamba-osaka-academy.hacomono.jp/home")

        print("✅ ログインボタンをクリック...")
        await page.click("text=ログイン")

        print("✅ ログイン情報を入力中...")
        await page.fill("input[name='mail_address']", EMAIL)
        await page.fill("input[name='password']", PASSWORD)

        print("✅ ログイン送信ボタンを押下...")
        await page.click("div[class*='m_modal'] button[type='submit']")

        print("⏳ 『すべてのお知らせを確認する』ボタンを待機...")
        await page.wait_for_selector("text=すべてのお知らせを確認する", timeout=10000)
        await page.click("text=すべてのお知らせを確認する")

        print("✅ HTMLを保存中...")
        await page.wait_for_timeout(2000)
        content = await page.content()
        with open("gamba_announcement_dynamic.html", "w", encoding="utf-8") as f:
            f.write(content)

        print("✅ お知らせページの動的HTML取得完了！")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())