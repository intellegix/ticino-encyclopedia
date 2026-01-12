#!/usr/bin/env python3
"""
Get the latest Perplexity query result
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def get_latest_result():
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

        print("\nWaiting for page to load...")
        await asyncio.sleep(3)

        print("\nLooking for recent queries in sidebar...")

        # Try to find and click the first query in the sidebar
        try:
            # The AI gaming blueprint query should be recent
            query_text = "Blueprint for building an open source AI model"

            # Try to click on the query link
            query_link = await page.get_by_text(query_text,  exact=False).first

            if query_link:
                print(f"Found query link: {query_text[:50]}...")
                await query_link.click()
                print("Clicked on query, waiting for results...")
                await asyncio.sleep(5)

        except Exception as e:
            print(f"Could not click query: {e}")

        # Extract full page content
        print("\nExtracting page content...")
        full_text = await page.evaluate("document.body.innerText")

        # Save to file
        output_dir = session_dir / "screenshots"
        output_dir.mkdir(parents=True, exist_ok=True)

        text_file = output_dir / "latest_result.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(full_text)

        print(f"\n[SAVED] Result text: {text_file}")
        print(f"[INFO] Content length: {len(full_text)} characters")

        # Screenshot
        screenshot = output_dir / "latest_result.png"
        await page.screenshot(path=str(screenshot), full_page=True)
        print(f"[SAVED] Screenshot: {screenshot}")

        # Display first 3000 characters
        print("\n" + "="*80)
        print("RESULT CONTENT (first 3000 chars):")
        print("="*80)
        print(full_text[:3000])
        print("="*80)

        # Try to extract just the answer section
        lines = full_text.split('\n')
        answer_started = False
        answer_lines = []

        for line in lines:
            stripped = line.strip()
            # Look for answer content (skip navigation/UI elements)
            if len(stripped) > 50 and not any(skip in stripped.lower() for skip in ['home', 'discover', 'spaces', 'account', 'upgrade', 'download']):
                answer_lines.append(stripped)

        if answer_lines:
            print("\n" + "="*80)
            print("EXTRACTED ANSWER:")
            print("="*80)
            for line in answer_lines[:50]:  # First 50 substantial lines
                print(line)
            print("="*80)

        print("\nKeeping browser open for 30 seconds for inspection...")
        await asyncio.sleep(30)

        await browser.close()
        print("\n[DONE]")

if __name__ == "__main__":
    asyncio.run(get_latest_result())
