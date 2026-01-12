#!/usr/bin/env python3
"""
Extract results from current Perplexity page
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def extract_results():
    session_dir = Path(__file__).parent / "sessions"
    cookies_file = session_dir / "perplexity_cookies.json"

    # Load cookies
    with open(cookies_file, 'r') as f:
        cookies = json.load(f)

    print(f"Loaded {len(cookies)} cookies")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Add cookies
        await context.add_cookies(cookies)

        page = await context.new_page()
        print("Going to Perplexity...")
        await page.goto("https://www.perplexity.ai", wait_until="networkidle")

        print("\nPage loaded. Waiting 5 seconds for any dynamic content...")
        await asyncio.sleep(5)

        print("\nExtracting ALL text content from page...")

        # Get all text content
        full_text = await page.evaluate("document.body.innerText")

        # Save to file
        output_dir = session_dir / "screenshots"
        output_dir.mkdir(parents=True, exist_ok=True)

        text_file = output_dir / "page_content.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(full_text)

        print(f"\n[SAVED] Full page text: {text_file}")
        print(f"[INFO] Content length: {len(full_text)} characters")

        # Also get HTML structure
        html_content = await page.content()
        html_file = output_dir / "page_source.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[SAVED] HTML source: {html_file}")

        # Take screenshot
        screenshot = output_dir / "current_page.png"
        await page.screenshot(path=str(screenshot), full_page=True)
        print(f"[SAVED] Screenshot: {screenshot}")

        # Show first 2000 characters
        print("\n" + "="*80)
        print("FIRST 2000 CHARACTERS OF PAGE:")
        print("="*80)
        print(full_text[:2000])
        print("="*80)

        print("\nKeeping browser open for 20 seconds for inspection...")
        await asyncio.sleep(20)

        await browser.close()
        print("\n[DONE] Check the files for full content")

if __name__ == "__main__":
    asyncio.run(extract_results())
