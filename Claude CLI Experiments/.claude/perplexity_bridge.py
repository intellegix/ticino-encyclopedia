#!/usr/bin/env python3
"""
Perplexity Research Mode Bridge for Claude Code Max CLI
Integrates with multiagent architecture for well-sourced answers
"""

import os
import sys
import json
import asyncio
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging

# External dependencies: pip install playwright aiohttp
try:
    from playwright.async_api import async_playwright, Browser, Page, BrowserContext
except ImportError:
    print(json.dumps({
        "success": False,
        "error": "playwright not installed. Run: pip install playwright && playwright install chromium"
    }))
    sys.exit(1)

# Setup logging
LOG_DIR = Path(__file__).parent
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler(LOG_DIR / 'perplexity_bridge.log')
    ]
)
logger = logging.getLogger(__name__)


class SessionManager:
    """Manages browser session persistence with cookie storage"""

    def __init__(self, session_dir: str = None):
        if session_dir is None:
            session_dir = Path(__file__).parent / "sessions"
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.cookies_file = self.session_dir / "perplexity_cookies.json"
        self.session_file = self.session_dir / "session_meta.json"
        self.cache_file = self.session_dir / "query_cache.json"

    def save_cookies(self, cookies: list) -> None:
        """Save cookies to persistent storage"""
        try:
            with open(self.cookies_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            logger.info(f"Saved {len(cookies)} cookies")
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")

    def load_cookies(self) -> list:
        """Load cookies from persistent storage"""
        try:
            if self.cookies_file.exists():
                with open(self.cookies_file, 'r') as f:
                    cookies = json.load(f)
                logger.info(f"Loaded {len(cookies)} cookies")
                return cookies
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
        return []

    def save_session_meta(self, meta: Dict[str, Any]) -> None:
        """Save session metadata"""
        meta['last_updated'] = datetime.now().isoformat()
        try:
            with open(self.session_file, 'w') as f:
                json.dump(meta, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save session metadata: {e}")

    def get_session_meta(self) -> Dict[str, Any]:
        """Get session metadata"""
        try:
            if self.session_file.exists():
                with open(self.session_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load session metadata: {e}")
        return {}

    def is_session_valid(self) -> bool:
        """Check if cached session is still valid (23 hours)"""
        if not self.cookies_file.exists():
            return False

        meta = self.get_session_meta()
        if not meta:
            return False

        try:
            last_updated = datetime.fromisoformat(meta.get('last_updated', ''))
            if datetime.now() - last_updated < timedelta(hours=23):
                return True
        except Exception:
            pass

        return False

    def get_cached_query(self, query: str) -> Optional[Dict[str, Any]]:
        """Get cached query result if available and fresh (1 hour)"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)

                query_hash = hash(query.lower().strip())
                cache_key = str(query_hash)

                if cache_key in cache:
                    cached = cache[cache_key]
                    cached_time = datetime.fromisoformat(cached['timestamp'])
                    if datetime.now() - cached_time < timedelta(hours=1):
                        logger.info(f"Using cached result for query: {query[:50]}...")
                        return cached['result']
        except Exception as e:
            logger.error(f"Failed to load cache: {e}")
        return None

    def save_query_cache(self, query: str, result: Dict[str, Any]) -> None:
        """Save query result to cache"""
        try:
            cache = {}
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    cache = json.load(f)

            query_hash = hash(query.lower().strip())
            cache_key = str(query_hash)

            cache[cache_key] = {
                'query': query,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }

            # Clean old entries (older than 24 hours)
            cutoff = datetime.now() - timedelta(hours=24)
            cache = {
                k: v for k, v in cache.items()
                if datetime.fromisoformat(v['timestamp']) > cutoff
            }

            with open(self.cache_file, 'w') as f:
                json.dump(cache, f, indent=2)

            logger.info(f"Cached query result: {query[:50]}...")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")


class PerplexityBridge:
    """Main bridge for Perplexity research queries"""

    def __init__(self, headless: bool = True):
        self.session_manager = SessionManager()
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
        self.authenticated = False
        self.headless = headless

    async def initialize_browser(self) -> None:
        """Initialize Playwright browser instance"""
        try:
            self.playwright = await async_playwright().start()

            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            logger.info(f"Browser initialized (headless={self.headless})")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

    async def create_context_with_cookies(self) -> None:
        """Create browser context with saved cookies"""
        try:
            self.context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )

            # Load saved cookies
            cookies = self.session_manager.load_cookies()
            if cookies:
                await self.context.add_cookies(cookies)
                logger.info("Loaded saved cookies into context")

            self.page = await self.context.new_page()
            await self.page.set_viewport_size({"width": 1920, "height": 1080})

        except Exception as e:
            logger.error(f"Failed to create context: {e}")
            raise

    async def authenticate_if_needed(self, timeout: int = 300) -> bool:
        """Authenticate with Perplexity if session not valid"""
        if self.session_manager.is_session_valid():
            logger.info("Using cached authentication")
            self.authenticated = True
            return True

        logger.info("Authentication required")

        try:
            await self.page.goto("https://www.perplexity.ai",
                               wait_until="networkidle",
                               timeout=30000)

            # Check if already logged in
            await asyncio.sleep(2)
            try:
                logged_in = await self.page.query_selector(
                    "[data-testid='user-menu'], .user-profile, button[aria-label*='profile' i]"
                )

                if logged_in:
                    logger.info("Already authenticated")
                    self.authenticated = True
                    cookies = await self.context.cookies()
                    self.session_manager.save_cookies(cookies)
                    self.session_manager.save_session_meta({
                        'authenticated': True,
                        'method': 'existing_session'
                    })
                    return True
            except Exception:
                pass

            # Wait for manual authentication
            logger.info("Waiting for manual authentication...")
            print(json.dumps({
                "action": "auth_required",
                "message": "Please log into Perplexity in your browser (complete OAuth if needed)",
                "timeout_seconds": timeout
            }), file=sys.stderr)

            start_time = asyncio.get_event_loop().time()

            while asyncio.get_event_loop().time() - start_time < timeout:
                try:
                    # Check if we're back on Perplexity domain (after OAuth)
                    current_url = self.page.url

                    # If we're on perplexity.ai domain, check for authentication indicators
                    if "perplexity.ai" in current_url:
                        # Multiple selectors to check for authentication
                        auth_selectors = [
                            "[data-testid='user-menu']",
                            ".user-profile",
                            "button[aria-label*='profile' i]",
                            "button[aria-label*='account' i]",
                            "button[aria-label*='user' i]",
                            "img[alt*='profile' i]",
                            "img[alt*='avatar' i]",
                            # Look for absence of sign-in button
                            "button:has-text('Sign Up')"  # If Sign Up button is absent, likely logged in
                        ]

                        # Check for logout/signout text (indicates logged in)
                        page_text = await self.page.evaluate("document.body.textContent")
                        if "log out" in page_text.lower() or "sign out" in page_text.lower():
                            logger.info("Authentication successful (found logout text)")
                            self.authenticated = True

                            cookies = await self.context.cookies()
                            self.session_manager.save_cookies(cookies)
                            self.session_manager.save_session_meta({
                                'authenticated': True,
                                'method': 'manual_login'
                            })
                            return True

                        # Check multiple selectors
                        for selector in auth_selectors[:-1]:  # Skip the negative check
                            try:
                                logged_in = await self.page.query_selector(selector)
                                if logged_in:
                                    logger.info(f"Authentication successful (selector: {selector})")
                                    self.authenticated = True

                                    cookies = await self.context.cookies()
                                    self.session_manager.save_cookies(cookies)
                                    self.session_manager.save_session_meta({
                                        'authenticated': True,
                                        'method': 'manual_login'
                                    })
                                    return True
                            except Exception:
                                pass

                    await asyncio.sleep(2)

                except Exception as e:
                    logger.debug(f"Checking authentication: {e}")
                    await asyncio.sleep(2)

            logger.warning("Authentication timeout")
            return False

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    async def execute_research_query(
        self,
        query: str,
        mode: str = "auto",
        timeout: int = 60
    ) -> Dict[str, Any]:
        """
        Execute a research query on Perplexity

        Args:
            query: The research question
            mode: Search mode - 'auto', 'research', 'copilot', 'normal', 'focus'
            timeout: Query timeout in seconds
        """
        if not self.authenticated:
            return {
                "success": False,
                "error": "Not authenticated with Perplexity",
                "query": query
            }

        # Check cache first
        cached = self.session_manager.get_cached_query(query)
        if cached:
            cached['from_cache'] = True
            return cached

        try:
            logger.info(f"Executing research query: {query[:100]}...")

            # Navigate to Perplexity
            await self.page.goto("https://www.perplexity.ai",
                               wait_until="networkidle",
                               timeout=30000)

            # Wait for search interface
            await asyncio.sleep(2)

            # Find and click search box (Perplexity uses contenteditable div)
            search_selectors = [
                "div[contenteditable='true']",
                "[contenteditable='true']",
                "textarea[placeholder*='Ask' i]",
                "textarea[placeholder*='search' i]",
                "input[placeholder*='Ask' i]",
                "textarea"
            ]

            search_box = None
            for selector in search_selectors:
                try:
                    search_box = await self.page.wait_for_selector(
                        selector,
                        timeout=5000
                    )
                    if search_box:
                        logger.info(f"Found search box with selector: {selector}")
                        break
                except Exception:
                    continue

            if not search_box:
                return {
                    "success": False,
                    "error": "Could not locate search box",
                    "query": query
                }

            # Click and clear search box
            await search_box.click()
            await asyncio.sleep(0.5)

            # For contenteditable divs, we need to use different approach
            await search_box.evaluate("element => element.textContent = ''")
            await asyncio.sleep(0.3)

            # Type query
            await search_box.type(query, delay=50)
            await asyncio.sleep(1)

            # Select mode if specified
            if mode != "auto":
                mode_selectors = {
                    "research": "button:has-text('Pro Search')",
                    "copilot": "button:has-text('Copilot')",
                    "focus": "button:has-text('Focus')"
                }

                if mode in mode_selectors:
                    try:
                        mode_btn = await self.page.wait_for_selector(
                            mode_selectors[mode],
                            timeout=3000
                        )
                        if mode_btn:
                            await mode_btn.click()
                            logger.info(f"Selected {mode} mode")
                            await asyncio.sleep(0.5)
                    except Exception as e:
                        logger.warning(f"Could not select {mode} mode: {e}")

            # Submit query
            await self.page.keyboard.press("Enter")
            logger.info("Query submitted, waiting for results...")

            # Wait for results with longer timeout
            result_selectors = [
                "[class*='answer' i]",
                "[class*='result' i]",
                "article",
                "[data-testid*='answer' i]"
            ]

            results_loaded = False
            for selector in result_selectors:
                try:
                    await self.page.wait_for_selector(
                        selector,
                        timeout=timeout * 1000
                    )
                    results_loaded = True
                    break
                except Exception:
                    continue

            if not results_loaded:
                return {
                    "success": False,
                    "error": "Results did not load within timeout",
                    "query": query
                }

            # Wait for results to stabilize
            await asyncio.sleep(3)

            logger.info("Extracting results...")

            # Extract comprehensive results
            results = await self.page.evaluate("""
                () => {
                    const data = {
                        answer: '',
                        sources: [],
                        related_questions: []
                    };

                    // Extract main answer
                    const answerSelectors = [
                        '[class*="answer"]',
                        '[data-testid*="answer"]',
                        'article',
                        '[class*="result"]'
                    ];

                    for (const selector of answerSelectors) {
                        const answerEl = document.querySelector(selector);
                        if (answerEl && answerEl.textContent.trim()) {
                            data.answer = answerEl.textContent.trim();
                            break;
                        }
                    }

                    // Extract sources/citations
                    const sourceLinks = document.querySelectorAll('a[href^="http"]');
                    const uniqueSources = new Set();

                    sourceLinks.forEach(link => {
                        const href = link.href;
                        const title = link.textContent.trim() || link.getAttribute('aria-label') || '';

                        if (href && !href.includes('perplexity.ai') && title) {
                            if (!uniqueSources.has(href)) {
                                uniqueSources.add(href);
                                data.sources.push({
                                    url: href,
                                    title: title.substring(0, 200)
                                });
                            }
                        }
                    });

                    // Limit sources
                    data.sources = data.sources.slice(0, 10);

                    // Extract related questions
                    const relatedSelectors = [
                        '[class*="related"]',
                        '[class*="follow-up"]',
                        'button'
                    ];

                    for (const selector of relatedSelectors) {
                        const relatedEls = document.querySelectorAll(selector);
                        relatedEls.forEach(el => {
                            const text = el.textContent.trim();
                            if (text && text.includes('?') && text.length > 10 && data.related_questions.length < 5) {
                                data.related_questions.push(text);
                            }
                        });

                        if (data.related_questions.length > 0) break;
                    }

                    return data;
                }
            """)

            result = {
                "success": True,
                "query": query,
                "mode": mode,
                "answer": results.get('answer', ''),
                "sources": results.get('sources', []),
                "related_questions": results.get('related_questions', []),
                "timestamp": datetime.now().isoformat()
            }

            # Cache the result
            self.session_manager.save_query_cache(query, result)

            logger.info(f"Research query completed: {len(results.get('answer', ''))} chars")
            return result

        except Exception as e:
            logger.error(f"Research query failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    async def close(self) -> None:
        """Cleanup resources"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")


async def main():
    parser = argparse.ArgumentParser(
        description="Perplexity Research Mode Bridge for Claude"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Research query to execute"
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="auto",
        choices=["auto", "research", "copilot", "normal", "focus"],
        help="Search mode to use"
    )
    parser.add_argument(
        "--check-auth",
        action="store_true",
        help="Check authentication status"
    )
    parser.add_argument(
        "--clear-session",
        action="store_true",
        help="Clear saved session and cookies"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear query cache"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)"
    )
    parser.add_argument(
        "--visible",
        action="store_true",
        help="Run browser in visible mode (for debugging)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Query timeout in seconds (default: 60)"
    )

    args = parser.parse_args()

    # Handle session/cache clearing
    if args.clear_session or args.clear_cache:
        session_mgr = SessionManager()
        if args.clear_session:
            session_mgr.cookies_file.unlink(missing_ok=True)
            session_mgr.session_file.unlink(missing_ok=True)
        if args.clear_cache:
            session_mgr.cache_file.unlink(missing_ok=True)

        print(json.dumps({
            "success": True,
            "message": "Session/cache cleared"
        }))
        return

    headless = not args.visible if args.visible else args.headless
    bridge = PerplexityBridge(headless=headless)

    try:
        # Initialize browser
        await bridge.initialize_browser()
        await bridge.create_context_with_cookies()

        # Authenticate if needed
        if not await bridge.authenticate_if_needed(timeout=300):
            print(json.dumps({
                "success": False,
                "error": "Authentication failed or timed out"
            }))
            return

        # Check auth status
        if args.check_auth:
            print(json.dumps({
                "authenticated": bridge.authenticated,
                "session_valid": bridge.session_manager.is_session_valid()
            }))
            return

        # Execute query
        if args.query:
            result = await bridge.execute_research_query(
                args.query,
                mode=args.mode,
                timeout=args.timeout
            )
            print(json.dumps(result, indent=2))
            return

        print(json.dumps({
            "success": False,
            "error": "No action specified (--query or --check-auth)"
        }))

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))
    finally:
        await bridge.close()


if __name__ == "__main__":
    asyncio.run(main())
