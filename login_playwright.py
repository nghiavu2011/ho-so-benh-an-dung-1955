import asyncio
from playwright.async_api import async_playwright
import time

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Intercept network requests to capture data
        captured_data = []
        def handle_response(response):
            # Check if JSON or text response
            url = response.url
            status = response.status
            if "api" in url or "benhvien108.vn" in url:
                try:
                    # Log response status and URL
                    captured_data.append(f"RESP: {status} {url}")
                except Exception as e:
                    pass

        page.on("response", handle_response)

        print("Navigating...")
        await page.goto("https://healthy.benhvien108.vn/?docno=27457702&phone=0913327626", wait_until="networkidle")
        await asyncio.sleep(5)
        
        # Take pre-login screenshot
        await page.screenshot(path="screenshot_pre_login.png")
        print("Pre-login screenshot saved.")
        
        # Click on "Mã xác nhận" input field at x=640, y=560
        # Let's double check if we can click it
        print("Clicking verification code input...")
        await page.mouse.click(640, 560)
        await asyncio.sleep(1)
        
        # Type the code Oy6E8
        print("Typing verification code...")
        await page.keyboard.type("Oy6E8")
        await asyncio.sleep(1)
        
        # Click the login button at x=640, y=650
        print("Clicking login button...")
        await page.mouse.click(640, 650)
        await asyncio.sleep(5)
        
        # Take post-login screenshot
        await page.screenshot(path="screenshot_post_login.png")
        print("Post-login screenshot saved.")
        
        # Let's print out captured response logs
        print("\nCaptured API Responses:")
        for data in captured_data:
            print(data)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
