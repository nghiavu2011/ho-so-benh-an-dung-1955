import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

URL = "https://healthy.benhvien108.vn/?docno=27457702&phone=0913327626"
OUTPUT_HTML = Path(r'D:/antigravity_scratch/real_estate_scoring/sql/Ho So Benh An Dung 1955/patient_profile.html')
OUTPUT_JSON = Path(r'D:/antigravity_scratch/real_estate_scoring/sql/Ho So Benh An Dung 1955/patient_info.json')

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(URL)
        await page.wait_for_load_state('networkidle')
        # Fill verification code (assumed static here)
        # The page may have a pre‑filled patient id; we only need to click the health record button.
        # Use a robust JS selector that matches the button by its innerText, normalizing Unicode.
        btn = await page.wait_for_selector("xpath=//button[contains(translate(., 'ÁÀÂÃÄÅáàâãäå', 'AAAAAAAAA'), 'HO SO SUC KHOE')]", timeout=15000)
        await btn.click()
        await page.wait_for_timeout(3000)
        # Scroll to load all sections
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)
        html = await page.content()
        OUTPUT_HTML.write_text(html, encoding='utf-8')
        print('Saved HTML to', OUTPUT_HTML)
        # Simple extraction example: grab patient name and id from known selectors
        name_el = await page.query_selector("xpath=//div[contains(@class, 'patient-name')]")
        name = await name_el.text_content() if name_el else ''
        id_el = await page.query_selector("xpath=//div[contains(@class, 'patient-id')]")
        pid = await id_el.text_content() if id_el else ''
        data = {"name": name.strip(), "patient_id": pid.strip()}
        OUTPUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print('Saved extracted info to', OUTPUT_JSON)
        await browser.close()

asyncio.run(main())
