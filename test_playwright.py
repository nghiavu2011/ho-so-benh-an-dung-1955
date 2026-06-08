import asyncio
from playwright.async_api import async_playwright
import time

async def main():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        # Create context
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Enable console log printing
        page.on("console", lambda msg: print(f"Console: {msg.text}"))
        
        # Intercept network requests
        requests_log = []
        page.on("request", lambda request: requests_log.append(f"REQ: {request.method} {request.url}"))
        page.on("response", lambda response: requests_log.append(f"RESP: {response.status} {response.url}"))

        print("Navigating to portal...")
        await page.goto("https://healthy.benhvien108.vn/?docno=27457702&phone=0913327626", wait_until="networkidle")
        
        # Sleep for a bit to let flutter start
        await asyncio.sleep(5)
        
        # Take a screenshot to see if we see text/inputs
        await page.screenshot(path="screenshot_loaded.png")
        print("Page loaded and screenshot saved.")
        
        # Dump page content / body HTML
        body_html = await page.content()
        with open("body_html.txt", "w", encoding="utf-8") as f:
            f.write(body_html)
            
        print("Saved body_html.txt")
        
        # Print captured request URLs to see if we can find API calls
        print("\nCaptured network calls:")
        for log in requests_log[:50]:
            print(log)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
