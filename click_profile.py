import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Intercept network responses to capture data
        responses = []
        def handle_response(response):
            url = response.url
            if "benhvien108.vn" in url:
                responses.append(f"RESP: {response.status} {url}")

        page.on("response", handle_response)

        print("Navigating...")
        await page.goto("https://healthy.benhvien108.vn/?docno=27457702&phone=0913327626", wait_until="networkidle")
        await asyncio.sleep(4)
        
        # Enter code and login
        await page.mouse.click(640, 560)
        await asyncio.sleep(0.5)
        await page.keyboard.type("Oy6E8")
        await asyncio.sleep(0.5)
        await page.mouse.click(640, 650)
        await asyncio.sleep(5)
        
        # Click on "Hồ sơ sức khỏe" at (x=690, y=370)
        print("Clicking Ho so suc khoe...")
        await page.mouse.click(690, 370)
        await asyncio.sleep(5)
        
        # Take screenshot of the profile page
        await page.screenshot(path="screenshot_profile.png")
        print("Profile page screenshot saved.")
        
        # Print responses
        print("\nCaptured Responses:")
        for r in responses:
            print(r)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
