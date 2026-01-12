#!/usr/bin/env python3
"""
Comprehensive debug script for Perplexity authentication
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def comprehensive_debug():
    print("Opening browser to Perplexity...")
    screenshots_dir = Path(__file__).parent / "sessions" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()

        await page.goto("https://www.perplexity.ai", wait_until="networkidle")

        print("\n[OK] Browser opened at Perplexity.")
        print("[ACTION REQUIRED] Please ensure you are logged in to your Perplexity Pro account.")
        print("[WAIT] Waiting 45 seconds...")
        await asyncio.sleep(45)

        print("\n[SCREENSHOT] Taking screenshot...")
        screenshot_path = screenshots_dir / "perplexity_logged_in.png"
        await page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"[SAVED] Screenshot: {screenshot_path}")

        print("\n[ANALYZING] Extracting ALL page elements...")

        # Get comprehensive page info
        page_info = await page.evaluate("""
            () => {
                const info = {
                    url: window.location.href,
                    title: document.title,
                    allButtons: [],
                    allLinks: [],
                    allInputs: [],
                    allImages: [],
                    elementsWithTestId: [],
                    elementsWithAriaLabel: [],
                    bodyClasses: document.body?.className || '',
                    hasLoginButton: false,
                    hasSignInButton: false,
                    hasLogoutButton: false,
                    hasSignOutButton: false
                };

                // Get ALL buttons
                document.querySelectorAll('button').forEach((btn, idx) => {
                    const text = btn.textContent?.trim();
                    const ariaLabel = btn.getAttribute('aria-label');
                    const classes = btn.className;
                    const id = btn.id;

                    if (idx < 50) {  // Limit to first 50 buttons
                        info.allButtons.push({
                            index: idx,
                            text: text?.substring(0, 100),
                            ariaLabel: ariaLabel,
                            class: classes?.substring(0, 150),
                            id: id,
                            visible: btn.offsetParent !== null
                        });
                    }

                    // Check for authentication-related text
                    const lowerText = text?.toLowerCase() || '';
                    const lowerAria = ariaLabel?.toLowerCase() || '';

                    if (lowerText.includes('log in') || lowerText.includes('login') ||
                        lowerAria.includes('log in') || lowerAria.includes('login')) {
                        info.hasLoginButton = true;
                    }
                    if (lowerText.includes('sign in') || lowerText.includes('signin') ||
                        lowerAria.includes('sign in') || lowerAria.includes('signin')) {
                        info.hasSignInButton = true;
                    }
                    if (lowerText.includes('log out') || lowerText.includes('logout') ||
                        lowerAria.includes('log out') || lowerAria.includes('logout')) {
                        info.hasLogoutButton = true;
                    }
                    if (lowerText.includes('sign out') || lowerText.includes('signout') ||
                        lowerAria.includes('sign out') || lowerAria.includes('signout')) {
                        info.hasSignOutButton = true;
                    }
                });

                // Get all elements with data-testid
                document.querySelectorAll('[data-testid]').forEach((el, idx) => {
                    if (idx < 30) {
                        info.elementsWithTestId.push({
                            testId: el.getAttribute('data-testid'),
                            tag: el.tagName,
                            class: el.className?.substring(0, 100)
                        });
                    }
                });

                // Get all elements with aria-label
                document.querySelectorAll('[aria-label]').forEach((el, idx) => {
                    if (idx < 30) {
                        info.elementsWithAriaLabel.push({
                            ariaLabel: el.getAttribute('aria-label')?.substring(0, 100),
                            tag: el.tagName,
                            class: el.className?.substring(0, 100)
                        });
                    }
                });

                // Get all images
                document.querySelectorAll('img').forEach((img, idx) => {
                    if (idx < 20) {
                        info.allImages.push({
                            src: img.src?.substring(0, 100),
                            alt: img.alt,
                            ariaLabel: img.getAttribute('aria-label'),
                            class: img.className?.substring(0, 100)
                        });
                    }
                });

                return info;
            }
        """)

        print("\n" + "="*80)
        print("[RESULTS] Page Analysis")
        print("="*80)

        print(f"\n[PAGE INFO]")
        print(f"  URL: {page_info['url']}")
        print(f"  Title: {page_info['title']}")

        print(f"\n[AUTHENTICATION STATUS]")
        print(f"  Has 'Log In' button: {page_info['hasLoginButton']}")
        print(f"  Has 'Sign In' button: {page_info['hasSignInButton']}")
        print(f"  Has 'Log Out' button: {page_info['hasLogoutButton']}")
        print(f"  Has 'Sign Out' button: {page_info['hasSignOutButton']}")

        if page_info['hasLogoutButton'] or page_info['hasSignOutButton']:
            print("\n  ==> LIKELY LOGGED IN (found logout button)")
        elif page_info['hasLoginButton'] or page_info['hasSignInButton']:
            print("\n  ==> LIKELY NOT LOGGED IN (found login button)")
        else:
            print("\n  ==> STATUS UNCLEAR (no obvious login/logout buttons)")

        print(f"\n[ALL BUTTONS] (first 20 visible buttons)")
        visible_buttons = [b for b in page_info['allButtons'] if b['visible']]
        for btn in visible_buttons[:20]:
            print(f"\n  Button #{btn['index']}:")
            if btn['text']:
                print(f"    Text: {btn['text']}")
            if btn['ariaLabel']:
                print(f"    Aria-Label: {btn['ariaLabel']}")
            if btn['class']:
                print(f"    Class: {btn['class']}")
            if btn['id']:
                print(f"    ID: {btn['id']}")

        if page_info['elementsWithTestId']:
            print(f"\n[DATA-TESTID ELEMENTS]")
            for el in page_info['elementsWithTestId'][:15]:
                print(f"  - {el['tag']}: {el['testId']}")
                if el['class']:
                    print(f"    Class: {el['class']}")

        if page_info['elementsWithAriaLabel']:
            print(f"\n[ARIA-LABEL ELEMENTS]")
            for el in page_info['elementsWithAriaLabel'][:15]:
                print(f"  - {el['tag']}: {el['ariaLabel']}")
                if el['class']:
                    print(f"    Class: {el['class']}")

        # Save full results to JSON
        json_path = screenshots_dir / "page_analysis.json"
        with open(json_path, 'w') as f:
            json.dump(page_info, f, indent=2)
        print(f"\n[SAVED] Full analysis: {json_path}")

        print("\n" + "="*80)
        print("[BROWSER] Keeping open for 20 more seconds for manual inspection...")
        print("="*80)
        await asyncio.sleep(20)

        await browser.close()
        print("\n[DONE] Check the screenshot and JSON file for details.")

if __name__ == "__main__":
    asyncio.run(comprehensive_debug())
