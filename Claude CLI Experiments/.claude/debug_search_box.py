#!/usr/bin/env python3
"""
Debug script to find the correct search box selector
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def find_search_box():
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
        await page.goto("https://www.perplexity.ai", wait_until="networkidle")

        print("\n[OK] Page loaded. Waiting for elements to stabilize...")
        await asyncio.sleep(5)

        print("\n[ANALYZING] Looking for search/input elements...")

        # Find all possible search elements
        search_info = await page.evaluate("""
            () => {
                const info = {
                    textareas: [],
                    inputs: [],
                    contentEditables: []
                };

                // All textareas
                document.querySelectorAll('textarea').forEach((el, idx) => {
                    info.textareas.push({
                        index: idx,
                        placeholder: el.placeholder,
                        name: el.name,
                        id: el.id,
                        class: el.className?.substring(0, 100),
                        visible: el.offsetParent !== null,
                        value: el.value?.substring(0, 50)
                    });
                });

                // All text inputs
                document.querySelectorAll('input[type="text"], input:not([type])').forEach((el, idx) => {
                    info.inputs.push({
                        index: idx,
                        placeholder: el.placeholder,
                        name: el.name,
                        id: el.id,
                        class: el.className?.substring(0, 100),
                        visible: el.offsetParent !== null,
                        value: el.value?.substring(0, 50)
                    });
                });

                // Content editable elements
                document.querySelectorAll('[contenteditable="true"]').forEach((el, idx) => {
                    info.contentEditables.push({
                        index: idx,
                        tag: el.tagName,
                        class: el.className?.substring(0, 100),
                        ariaLabel: el.getAttribute('aria-label'),
                        visible: el.offsetParent !== null
                    });
                });

                return info;
            }
        """)

        print("\n[RESULTS] Search Elements Found:\n")

        if search_info['textareas']:
            print("[TEXTAREAS]")
            for ta in search_info['textareas']:
                print(f"\n  Textarea #{ta['index']}:")
                print(f"    Visible: {ta['visible']}")
                if ta['placeholder']:
                    print(f"    Placeholder: {ta['placeholder']}")
                if ta['id']:
                    print(f"    ID: {ta['id']}")
                if ta['class']:
                    print(f"    Class: {ta['class']}")
                if ta['name']:
                    print(f"    Name: {ta['name']}")

        if search_info['inputs']:
            print("\n[TEXT INPUTS]")
            for inp in search_info['inputs'][:10]:
                print(f"\n  Input #{inp['index']}:")
                print(f"    Visible: {inp['visible']}")
                if inp['placeholder']:
                    print(f"    Placeholder: {inp['placeholder']}")
                if inp['id']:
                    print(f"    ID: {inp['id']}")
                if inp['class']:
                    print(f"    Class: {inp['class']}")

        if search_info['contentEditables']:
            print("\n[CONTENTEDITABLE ELEMENTS]")
            for ce in search_info['contentEditables']:
                print(f"\n  Element #{ce['index']}:")
                print(f"    Tag: {ce['tag']}")
                print(f"    Visible: {ce['visible']}")
                if ce['ariaLabel']:
                    print(f"    Aria-Label: {ce['ariaLabel']}")
                if ce['class']:
                    print(f"    Class: {ce['class']}")

        # Take screenshot
        screenshot_path = session_dir / "screenshots" / "search_box_debug.png"
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"\n[SAVED] Screenshot: {screenshot_path}")

        # Save to JSON
        json_path = session_dir / "screenshots" / "search_elements.json"
        with open(json_path, 'w') as f:
            json.dump(search_info, f, indent=2)
        print(f"[SAVED] Elements data: {json_path}")

        print("\n[BROWSER] Keeping open for 30 seconds for inspection...")
        await asyncio.sleep(30)

        await browser.close()
        print("\n[DONE]")

if __name__ == "__main__":
    asyncio.run(find_search_box())
