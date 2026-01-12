#!/usr/bin/env python3
"""
Debug script to find the Research mode dropdown trigger button
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def find_button():
    session_dir = Path(__file__).parent / "sessions"
    cookies_file = session_dir / "perplexity_cookies.json"

    with open(cookies_file, 'r') as f:
        cookies = json.load(f)

    print(f"Loaded {len(cookies)} cookies\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        await context.add_cookies(cookies)
        page = await context.new_page()

        print("[1] Going to Perplexity...")
        await page.goto("https://www.perplexity.ai", wait_until="networkidle")
        await asyncio.sleep(3)

        print("[2] Finding search box...")
        search_box = await page.wait_for_selector("div[contenteditable='true']", timeout=10000)

        print("[3] Typing test query...")
        await search_box.click()
        await asyncio.sleep(0.5)
        await search_box.type("test query", delay=50)
        await asyncio.sleep(1)

        print("\n[4] Analyzing all buttons near search box...\n")

        # Get all buttons near the search area
        buttons_info = await page.evaluate("""
            () => {
                const buttons = [];
                const searchBox = document.querySelector('div[contenteditable="true"]');

                if (!searchBox) return buttons;

                // Get parent container
                const container = searchBox.closest('div[class*="search"], div[class*="input"], form');

                // Find all buttons in and around the search area
                const allButtons = document.querySelectorAll('button, [role="button"]');

                allButtons.forEach((btn, idx) => {
                    // Check if button is near the search box
                    const rect = btn.getBoundingClientRect();
                    const searchRect = searchBox.getBoundingClientRect();

                    // If button is within 200px vertically of search box
                    if (Math.abs(rect.top - searchRect.top) < 200) {
                        buttons.push({
                            index: idx,
                            text: btn.textContent?.trim().substring(0, 50),
                            ariaLabel: btn.getAttribute('aria-label'),
                            className: btn.className?.substring(0, 150),
                            id: btn.id,
                            title: btn.title,
                            visible: btn.offsetParent !== null,
                            position: {
                                x: Math.round(rect.left),
                                y: Math.round(rect.top),
                                width: Math.round(rect.width),
                                height: Math.round(rect.height)
                            }
                        });
                    }
                });

                return buttons.filter(b => b.visible);
            }
        """)

        print("BUTTONS NEAR SEARCH BOX:")
        print("="*80)
        for i, btn in enumerate(buttons_info[:20]):
            print(f"\n[{i}] Button #{btn['index']}:")
            if btn['text']:
                print(f"    Text: '{btn['text']}'")
            if btn['ariaLabel']:
                print(f"    Aria-Label: '{btn['ariaLabel']}'")
            if btn['title']:
                print(f"    Title: '{btn['title']}'")
            if btn['className']:
                print(f"    Class: {btn['className'][:100]}")
            print(f"    Position: x={btn['position']['x']}, y={btn['position']['y']}, size={btn['position']['width']}x{btn['position']['height']}")

        print("\n" + "="*80)
        print("\nKEEPING BROWSER OPEN FOR 60 SECONDS")
        print("TRY CLICKING BUTTONS TO SEE WHICH OPENS THE RESEARCH DROPDOWN")
        print("="*80)

        await asyncio.sleep(60)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(find_button())
