#!/usr/bin/env python3
"""
Simple research query with visible browser and guaranteed screenshot
"""
import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

async def simple_research(query: str, wait_time: int = 120):
    """Run a query and screenshot the results - no complex detection"""

    session_dir = Path(__file__).parent / "sessions"
    cookies_file = session_dir / "perplexity_cookies.json"

    # Load cookies
    with open(cookies_file, 'r') as f:
        cookies = json.load(f)

    print(f"[INFO] Loaded {len(cookies)} cookies")
    print(f"[INFO] Query: {query}")
    print(f"[INFO] Will wait {wait_time} seconds for results\n")

    async with async_playwright() as p:
        # Launch in VISIBLE mode
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )

        # Add cookies
        await context.add_cookies(cookies)

        page = await context.new_page()

        print("[1/6] Navigating to Perplexity...")
        await page.goto("https://www.perplexity.ai", wait_until="networkidle")
        await asyncio.sleep(3)

        print("[2/6] Finding search box...")
        search_box = await page.wait_for_selector("div[contenteditable='true']", timeout=10000)

        print("[3/6] Typing query...")
        await search_box.click()
        await asyncio.sleep(0.5)
        await search_box.evaluate("element => element.textContent = ''")
        await search_box.type(query, delay=50)
        await asyncio.sleep(1)

        print("[3.5/6] Activating Research mode...")

        # Click the Research button (segmented control)
        try:
            research_btn = await page.wait_for_selector("button[aria-label='Research']", timeout=3000)
            if research_btn:
                await research_btn.click()
                print("    [OK] Research mode activated!")
                await asyncio.sleep(0.5)
            else:
                print("    [WARN] Could not find Research button - using default mode")
        except Exception as e:
            print(f"    [ERROR] Could not activate Research mode: {e}")

        print("[4/6] Submitting query...")
        await page.keyboard.press("Enter")

        print(f"[5/6] Waiting {wait_time} seconds for Perplexity to generate comprehensive results...")
        print("      (You can watch the browser window to see progress)")

        # Wait in 10-second intervals with progress updates
        for i in range(0, wait_time, 10):
            await asyncio.sleep(10)
            elapsed = i + 10
            remaining = wait_time - elapsed
            print(f"      ... {elapsed}s elapsed, {remaining}s remaining")

        print("\n[6/6] Extracting content and taking screenshot...")

        output_dir = session_dir / "screenshots"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Extract text FIRST (before screenshot which might timeout)
        print("  - Extracting text...")
        full_text = await page.evaluate("document.body.innerText")
        text_path = output_dir / f"research_result.txt"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(f"Query: {query}\n")
            f.write("="*80 + "\n\n")
            f.write(full_text)

        print(f"  [SAVED] Full text: {text_path}")
        print(f"  [INFO] Content length: {len(full_text):,} characters")

        # Try screenshot (may timeout on very long pages)
        print("  - Taking screenshot...")
        try:
            screenshot_path = output_dir / f"research_result.png"
            await page.screenshot(path=str(screenshot_path), full_page=False, timeout=15000)
            print(f"  [SAVED] Screenshot: {screenshot_path}")
        except Exception as e:
            print(f"  [WARN] Screenshot failed (page might be too long): {e}")
            screenshot_path = None

        print(f"\n[SUCCESS] Research complete!")
        print(f"[INFO] Keeping browser open for 30 seconds so you can review...")
        await asyncio.sleep(30)

        await browser.close()

        # Return the paths
        return {
            "screenshot": str(screenshot_path),
            "text": str(text_path),
            "content_length": len(full_text)
        }

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Test query"
    wait_time = int(sys.argv[2]) if len(sys.argv) > 2 else 120

    result = asyncio.run(simple_research(query, wait_time))
    print(f"\nFiles saved:")
    print(f"  Screenshot: {result['screenshot']}")
    print(f"  Text: {result['text']}")
