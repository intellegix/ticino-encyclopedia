#!/usr/bin/env python3
"""
Debug script to identify correct authentication selectors for Perplexity
"""
import asyncio
from playwright.async_api import async_playwright

async def debug_auth():
    print("Opening browser to Perplexity...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.perplexity.ai", wait_until="networkidle")

        print("\n[OK] Browser opened. Please log in if not already logged in.")
        print("[WAIT] Waiting 60 seconds for you to log in...")
        await asyncio.sleep(60)

        print("\n[ANALYZING] Checking page for authentication indicators...\n")

        # Check for various common authentication indicators
        indicators = await page.evaluate("""
            () => {
                const results = {
                    buttons: [],
                    links: [],
                    testIds: [],
                    profileElements: [],
                    userElements: [],
                    menuElements: []
                };

                // Find all buttons
                document.querySelectorAll('button').forEach(btn => {
                    const text = btn.textContent?.trim().toLowerCase();
                    const ariaLabel = btn.getAttribute('aria-label')?.toLowerCase();
                    const classes = btn.className;

                    if (text?.includes('profile') || text?.includes('user') ||
                        text?.includes('account') || text?.includes('settings') ||
                        ariaLabel?.includes('profile') || ariaLabel?.includes('user') ||
                        ariaLabel?.includes('account') || ariaLabel?.includes('menu')) {
                        results.buttons.push({
                            text: btn.textContent?.trim().substring(0, 50),
                            ariaLabel: ariaLabel,
                            class: classes,
                            id: btn.id
                        });
                    }
                });

                // Find all test-id attributes
                document.querySelectorAll('[data-testid]').forEach(el => {
                    const testId = el.getAttribute('data-testid');
                    if (testId?.includes('user') || testId?.includes('profile') ||
                        testId?.includes('menu') || testId?.includes('account')) {
                        results.testIds.push({
                            testId: testId,
                            tag: el.tagName,
                            class: el.className
                        });
                    }
                });

                // Find profile-related elements
                document.querySelectorAll('[class*="profile"], [class*="user"], [class*="account"]').forEach(el => {
                    results.profileElements.push({
                        tag: el.tagName,
                        class: el.className,
                        id: el.id
                    });
                });

                // Check for avatar/image elements
                document.querySelectorAll('img, svg').forEach(el => {
                    const alt = el.getAttribute('alt')?.toLowerCase();
                    const ariaLabel = el.getAttribute('aria-label')?.toLowerCase();

                    if (alt?.includes('profile') || alt?.includes('user') || alt?.includes('avatar') ||
                        ariaLabel?.includes('profile') || ariaLabel?.includes('user') || ariaLabel?.includes('avatar')) {
                        results.userElements.push({
                            tag: el.tagName,
                            alt: alt,
                            ariaLabel: ariaLabel,
                            class: el.className
                        });
                    }
                });

                return results;
            }
        """)

        print("[RESULTS] Found Authentication Indicators:\n")

        if indicators['buttons']:
            print("[+] BUTTONS (likely authentication indicators):")
            for btn in indicators['buttons'][:10]:
                print(f"  - Text: {btn['text']}")
                if btn['ariaLabel']:
                    print(f"    Aria-Label: {btn['ariaLabel']}")
                if btn['class']:
                    print(f"    Class: {btn['class'][:100]}")
                if btn['id']:
                    print(f"    ID: {btn['id']}")
                print()

        if indicators['testIds']:
            print("[+] DATA-TESTID ATTRIBUTES:")
            for tid in indicators['testIds'][:5]:
                print(f"  - Test ID: {tid['testId']}")
                print(f"    Tag: {tid['tag']}")
                print(f"    Class: {tid['class'][:100] if tid['class'] else 'None'}")
                print()

        if indicators['profileElements']:
            print("[+] PROFILE/USER/ACCOUNT ELEMENTS:")
            for el in indicators['profileElements'][:5]:
                print(f"  - Tag: {el['tag']}")
                print(f"    Class: {el['class'][:100] if el['class'] else 'None'}")
                print(f"    ID: {el['id'] if el['id'] else 'None'}")
                print()

        if indicators['userElements']:
            print("[+] USER IMAGES/ICONS:")
            for el in indicators['userElements'][:5]:
                print(f"  - Tag: {el['tag']}")
                if el['alt']:
                    print(f"    Alt: {el['alt']}")
                if el['ariaLabel']:
                    print(f"    Aria-Label: {el['ariaLabel']}")
                print()

        if not any([indicators['buttons'], indicators['testIds'],
                   indicators['profileElements'], indicators['userElements']]):
            print("[-] No authentication indicators found!")
            print("This might mean:")
            print("  1. You're not logged in")
            print("  2. Perplexity uses different selectors")
            print("  3. The page hasn't fully loaded")

        print("\n" + "="*60)
        print("Keeping browser open for 30 more seconds for inspection...")
        print("="*60)
        await asyncio.sleep(30)

        await browser.close()
        print("\n[DONE] Use the information above to update the authentication selectors.")

if __name__ == "__main__":
    asyncio.run(debug_auth())
