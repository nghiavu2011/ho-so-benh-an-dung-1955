import asyncio
from playwright.async_api import async_playwright
import json
import re

# Store captured response data
captured_bodies = []

async def capture_response(response):
    url = response.url
    # Only capture API calls, not assets
    if any(x in url for x in ["vimes.System", "Execute", "Auth"]):
        try:
            body = await response.body()
            captured_bodies.append({"url": url, "body": body.hex()})
        except:
            pass

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        page.on("response", capture_response)

        print("Navigating to portal...")
        await page.goto("https://healthy.benhvien108.vn/?docno=27457702&phone=0913327626", wait_until="networkidle")
        await asyncio.sleep(5)

        # Screenshot 1: Before login
        await page.screenshot(path="step01_before_login.png")
        print("Step 1: Initial load done.")

        # Tab to reach the verification code field
        # Flutter renders a canvas but also has accessibility elements
        # Let's try: click on the center of the dialog form, then tab to reach code field
        # Dialog appears to be at y=100 to y=600
        # The "Mã xác nhận" field is the 3rd field
        # Click on verification field area
        await page.mouse.click(640, 405)
        await asyncio.sleep(0.5)
        await page.screenshot(path="step02_clicked_code_field.png")
        print("Step 2: Clicked verification code field area.")

        # Type the verification code
        await page.keyboard.type("Oy6E8")
        await asyncio.sleep(0.5)
        await page.screenshot(path="step03_typed_code.png")
        print("Step 3: Typed verification code.")

        # Click the login button (the green button at bottom of dialog)
        await page.mouse.click(640, 467)
        await asyncio.sleep(6)
        await page.screenshot(path="step04_after_login_click.png")
        print("Step 4: Clicked login button, waited 6s.")

        # Check if login succeeded - look for user name change
        # If still "Quý khách", login failed; if shows patient name, it worked
        # Let's click on "Hồ sơ sức khỏe" which is top-right card in main menu
        # Row 1 of cards: y is approx 270
        # Col 4 (rightmost): x is approx 888
        print("Clicking Ho so suc khoe button at 888, 270...")
        await page.mouse.click(888, 270)
        await asyncio.sleep(5)
        await page.screenshot(path="step05_after_click_profile.png")
        print("Step 5: Clicked health profile.")

        # Try scrolling down to see more content
        await page.keyboard.press("PageDown")
        await asyncio.sleep(2)
        await page.screenshot(path="step06_scrolled.png")
        print("Step 6: Scrolled down.")

        # Write captured bodies to file
        with open("captured_responses.json", "w", encoding="utf-8") as f:
            json.dump(captured_bodies, f, indent=2)
        print(f"Saved {len(captured_bodies)} captured API responses.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
