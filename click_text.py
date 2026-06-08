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

        print("Navigating...")
        await page.goto("https://healthy.benhvien108.vn/?docno=27457702&phone=0913327626", wait_until="networkidle")
        await asyncio.sleep(4)
        
        # Enter code and login
        await page.mouse.click(640, 560)
        await asyncio.sleep(0.5)
        await page.keyboard.type("Oy6E8")
        await asyncio.sleep(0.5)
        await page.mouse.click(640, 650)
        await asyncio.sleep(6)
        
        # Take a screenshot to confirm login
        await page.screenshot(path="screenshot_check.png")
        
        # Let's inspect page elements and try to find anything with text
        # Let's try locating "Hồ sơ sức khỏe"
        try:
            loc = page.locator('text="Hồ sơ sức khỏe"')
            count = await loc.count()
            print(f"Locator 'Hồ sơ sức khỏe' count: {count}")
            if count > 0:
                print("Clicking using locator...")
                await loc.first.click()
                await asyncio.sleep(5)
                await page.screenshot(path="screenshot_profile_text_click.png")
                print("Clicked and saved screenshot.")
                await browser.close()
                return
        except Exception as e:
            print("Locator failed:", e)

        # Let's try finding the coordinates using a grid of clicks or coordinate estimation
        # Let's write a loop to print all text-like elements
        print("Trying coordinate click at different positions...")
        # Maybe x=700, y=360? Or is x=900?
        # Let's look at the columns: 
        # Left boundary of Col 1 is around x=250.
        # Right boundary of Col 4 is around x=950.
        # Let's estimate:
        # Col 1 center: x=300
        # Col 2 center: x=490
        # Col 3 center: x=680
        # Col 4 center: x=870?
        # Let's click at x=870, y=360!
        print("Clicking at x=870, y=360...")
        await page.mouse.click(870, 360)
        await asyncio.sleep(5)
        await page.screenshot(path="screenshot_profile_870.png")
        print("Saved screenshot of 870 click.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
