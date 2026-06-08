import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

URL = "https://healthy.benhvien108.vn/?docno=27457702&phone=0913327626"
VERIFICATION_CODE = "Oy6E8"
OUTPUT_HTML = Path(r"D:/antigravity_scratch/real_estate_scoring/sql/Ho So Benh An Dung 1955/patient_profile.html")
OUTPUT_SCREENSHOT = Path(r"D:/antigravity_scratch/real_estate_scoring/sql/Ho So Benh An Dung 1955/patient_profile.png")

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL)
        # Wait for verification code input – try common selectors
        try:
            await page.wait_for_selector("input[type='text'], input[type='tel'], textarea", timeout=5000)
        except Exception:
            pass
        # Fill verification code – many sites have placeholder or label 'Mã xác minh'
        # Attempt to fill the first visible input with the code
        inputs = await page.query_selector_all("input")
        if inputs:
            await inputs[0].fill(VERIFICATION_CODE)
        # Click login/submit button – look for button containing 'Xác nhận' or 'Đăng nhập'
        try:
            await page.click("button:has-text('Xác nhận')")
        except Exception:
            try:
                await page.click("button:has-text('Đăng nhập')")
            except Exception:
                pass
        # Wait for navigation after login
        await page.wait_for_load_state('networkidle')
        # Click the "Hồ sơ sức khỏe" button – text match
        try:
            await page.click("text='Hồ sơ sức khỏe'")
        except Exception:
            # fallback using partial match
            await page.click("text='Hồ sơ' >> nth=0")
        await page.wait_for_timeout(3000)
        # Capture page content
        content = await page.content()
        OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_HTML.write_text(content, encoding='utf-8')
        # Capture screenshot
        await page.screenshot(path=str(OUTPUT_SCREENSHOT))
        print('Saved patient profile HTML and screenshot')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
