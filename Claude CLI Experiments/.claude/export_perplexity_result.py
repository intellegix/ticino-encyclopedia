#!/usr/bin/env python3
"""
Export Perplexity research results using built-in export functionality
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def export_latest_result():
    """Navigate to latest query and export using Perplexity's export button"""

    session_dir = Path(__file__).parent / "sessions"
    cookies_file = session_dir / "perplexity_cookies.json"

    # Load cookies
    with open(cookies_file, 'r') as f:
        cookies = json.load(f)

    print(f"[INFO] Loaded {len(cookies)} cookies\n")

    async with async_playwright() as p:
        # Launch visible browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )

        # Add cookies
        await context.add_cookies(cookies)
        page = await context.new_page()

        print("[1/5] Navigating to Perplexity...")
        await page.goto("https://www.perplexity.ai", wait_until="networkidle")
        await asyncio.sleep(3)

        print("[2/5] Looking for recent AI gaming model query in sidebar...")

        # Try to click the most recent relevant query
        try:
            # Look for the query text in the sidebar
            query_link = page.get_by_text("Blueprint for AI model", exact=False).first
            await query_link.click()
            print("    ✓ Clicked on query")
            await asyncio.sleep(5)  # Wait for results to load
        except Exception as e:
            print(f"    ! Could not auto-click query: {e}")
            print("    → Assuming we're already on a results page")

        print("\n[3/5] Looking for Export button...")

        # Try multiple selectors for the Export button
        export_button = None
        export_selectors = [
            "button:has-text('Export')",
            "[aria-label*='Export' i]",
            "button[title*='Export' i]"
        ]

        for selector in export_selectors:
            try:
                export_button = await page.wait_for_selector(selector, timeout=3000)
                if export_button:
                    print(f"    ✓ Found Export button: {selector}")
                    break
            except:
                continue

        if not export_button:
            print("    ✗ Could not find Export button")
            print("    → Taking manual screenshot instead")

            # Fallback: just screenshot and extract text
            output_dir = session_dir / "screenshots"
            output_dir.mkdir(parents=True, exist_ok=True)

            screenshot_path = output_dir / "manual_export.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)

            full_text = await page.evaluate("document.body.innerText")
            text_path = output_dir / "manual_export.txt"
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(full_text)

            print(f"\n[SAVED] Screenshot: {screenshot_path}")
            print(f"[SAVED] Text: {text_path}")

            print("\n[INFO] Keeping browser open for 20 seconds...")
            await asyncio.sleep(20)
            await browser.close()
            return

        print("\n[4/5] Clicking Export button...")
        await export_button.click()
        await asyncio.sleep(2)

        # Look for export options (might be a menu with different formats)
        print("[5/5] Checking for export options...")

        # Common export formats: Markdown, Text, PDF, etc.
        # Try to find and click a text/markdown export option
        export_options = [
            "button:has-text('Markdown')",
            "button:has-text('Text')",
            "button:has-text('Copy')",
            "[aria-label*='markdown' i]",
            "[aria-label*='text' i]"
        ]

        export_clicked = False
        for option_selector in export_options:
            try:
                option = await page.wait_for_selector(option_selector, timeout=2000)
                if option:
                    print(f"    ✓ Found export option: {option_selector}")
                    await option.click()
                    export_clicked = True
                    await asyncio.sleep(1)
                    break
            except:
                continue

        # Try to get clipboard content if copy was used
        try:
            # Check if something was copied to clipboard
            clipboard_text = await page.evaluate("""
                async () => {
                    try {
                        return await navigator.clipboard.readText();
                    } catch (e) {
                        return null;
                    }
                }
            """)

            if clipboard_text and len(clipboard_text) > 100:
                print(f"\n[SUCCESS] Exported content from clipboard ({len(clipboard_text)} chars)")

                output_dir = session_dir / "screenshots"
                output_dir.mkdir(parents=True, exist_ok=True)

                export_path = output_dir / "perplexity_export.md"
                with open(export_path, 'w', encoding='utf-8') as f:
                    f.write(clipboard_text)

                print(f"[SAVED] Exported content: {export_path}")

                # Also save screenshot
                screenshot_path = output_dir / "export_screenshot.png"
                await page.screenshot(path=str(screenshot_path))
                print(f"[SAVED] Screenshot: {screenshot_path}")

        except Exception as e:
            print(f"    ! Could not access clipboard: {e}")

        # Also extract page text as backup
        full_text = await page.evaluate("document.body.innerText")
        output_dir = session_dir / "screenshots"
        text_path = output_dir / "page_export.txt"
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f"[SAVED] Backup text export: {text_path}")

        print("\n[INFO] Keeping browser open for 30 seconds for review...")
        await asyncio.sleep(30)

        await browser.close()
        print("\n[DONE]")

if __name__ == "__main__":
    asyncio.run(export_latest_result())
