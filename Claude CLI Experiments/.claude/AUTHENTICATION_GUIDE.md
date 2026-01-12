# Perplexity Pro Authentication Guide

**Status:** Ready for manual authentication
**Estimated Time:** 3-5 minutes (one-time setup)
**Session Duration:** 23 hours (auto-renews)

---

## Why Authentication is Needed

The Perplexity Research integration requires authentication to access:
- **Pro Search Mode** - Deep research with comprehensive sources
- **Research-backed answers** - Authoritative citations
- **Advanced query modes** - Copilot, Focus, Research modes
- **Higher quality results** - Better than standard search

Without authentication, the system falls back to Claude's built-in knowledge (still useful, but without external sources).

---

## Authentication Process

### Step 1: Start Authentication

```bash
cd "C:\Users\AustinKidwell\ASR Dropbox\Austin Kidwell\02_DevelopmentProjects\Claude CLI Experiments"

# Run authentication in visible mode
.venv/Scripts/python.exe .claude/perplexity_bridge.py --check-auth --visible
```

### Step 2: What Happens

1. **Browser Opens** - Chromium browser launches automatically
2. **Navigate to Perplexity** - Goes to https://www.perplexity.ai
3. **Login Prompt** - You'll see the Perplexity login page
4. **Wait Time** - Script waits up to 5 minutes for you to log in

### Step 3: Log In to Perplexity

**In the opened browser:**
1. Click "Sign In" or "Log In"
2. Use your Perplexity Pro credentials:
   - Email/password
   - Or Google/GitHub SSO
3. Complete 2FA if enabled
4. Wait for dashboard to load

### Step 4: Automatic Detection

Once logged in:
- Script detects authentication automatically
- Saves session cookies to `.claude/sessions/perplexity_cookies.json`
- Closes browser
- Confirms: "Authentication successful"

---

## Session Management

### Session Details

| Property | Value | Notes |
|----------|-------|-------|
| Duration | 23 hours | Auto-expires |
| Storage | `.claude/sessions/perplexity_cookies.json` | Gitignored |
| Auto-Refresh | Yes | On next query after expiry |
| Manual Reset | `--clear-session` | Forces re-authentication |

### Check Authentication Status

```bash
# Quick check (no browser)
.venv/Scripts/python.exe .claude/perplexity_bridge.py --check-auth

# Output if authenticated:
{
  "authenticated": true,
  "session_valid": true
}

# Output if not authenticated:
{
  "authenticated": false,
  "session_valid": false
}
```

---

## Troubleshooting

### Issue: Browser doesn't open

**Cause:** Chromium not installed or PATH issue

**Solution:**
```bash
# Reinstall Playwright Chromium
.venv/Scripts/playwright.exe install chromium

# Verify installation
.venv/Scripts/playwright.exe --version
```

### Issue: Authentication timeout

**Cause:** Took longer than 5 minutes to log in

**Solution:**
```bash
# Increase timeout to 10 minutes
.venv/Scripts/python.exe .claude/perplexity_bridge.py --check-auth --visible --timeout 600
```

### Issue: "Could not detect authentication"

**Possible causes:**
1. Not logged in to Pro account (free tier won't work)
2. Browser closed too quickly
3. Network issues

**Solution:**
```bash
# Clear session and retry
.venv/Scripts/python.exe .claude/perplexity_bridge.py --clear-session
.venv/Scripts/python.exe .claude/perplexity_bridge.py --check-auth --visible
```

### Issue: Session expired

**Cause:** More than 23 hours since last authentication

**Solution:**
Just run any research query - auto-refreshes authentication

```bash
.venv/Scripts/python.exe .claude/perplexity_bridge.py --query "test"
# Will automatically re-authenticate if needed
```

---

## Manual Authentication Alternative

If automated authentication doesn't work, you can manually copy cookies:

### Option 1: Use Existing Browser Session

**Not recommended** - Complex cookie extraction

### Option 2: Re-run with Visible Mode

```bash
# Run with visible browser for debugging
.venv/Scripts/python.exe .claude/perplexity_bridge.py --check-auth --visible

# Watch browser actions in real-time
# Manually assist if automation fails
```

---

## After Authentication

Once authenticated, you can:

### 1. Test Research Query

```bash
.venv/Scripts/python.exe .claude/perplexity_bridge.py \
  --query "React Server Components performance best practices 2024" \
  --mode research
```

**Expected output:**
```json
{
  "success": true,
  "query": "React Server Components performance...",
  "mode": "research",
  "answer": "Comprehensive answer with details...",
  "sources": [
    {
      "url": "https://react.dev/...",
      "title": "React Server Components Documentation"
    },
    ...
  ],
  "related_questions": [
    "How do Server Components compare to Client Components?",
    "What are the caching strategies for Server Components?"
  ],
  "timestamp": "2024-10-29T..."
}
```

### 2. Use via Claude Code Max CLI

```bash
/research React Server Components performance best practices 2024
```

### 3. Integrate with Smart Commands

```bash
/smart-plan
# Automatically uses research for best practices

/smart-debug
# Uses research for error troubleshooting

/smart-optimize
# Uses research for optimization strategies
```

---

## Working Without Authentication

**You can still use most features without Perplexity authentication:**

### Available Features
✅ Agent orchestration
✅ Project planning (`agent_orchestrator.py`)
✅ Task coordination
✅ Workflow generation
✅ ADR creation
✅ Architecture design

### Limited Features
⚠️ Research queries - Falls back to Claude's knowledge
⚠️ Source citations - Not available
⚠️ External references - Not available

### To Use Without Authentication

Simply skip the authentication step and use commands normally. Research queries will use Claude's built-in knowledge instead of external sources.

---

## Security Considerations

### Cookie Storage

**Location:** `.claude/sessions/perplexity_cookies.json`

**Security measures:**
- ✅ Automatically gitignored
- ✅ Stored locally only
- ✅ No network transmission
- ✅ Auto-expires after 23 hours
- ✅ Encrypted by filesystem permissions

**Never commit:**
- `.claude/sessions/*.json`
- `.claude/perplexity_bridge.log`

### Best Practices

1. **Don't share session files** - Contains authentication
2. **Don't commit cookies** - Setup script handles .gitignore
3. **Clear sessions periodically** - Use `--clear-session`
4. **Use environment isolation** - Virtual environment per project
5. **Monitor logs** - Check for unusual activity

---

## Quick Reference

```bash
# Check authentication
.venv/Scripts/python.exe .claude/perplexity_bridge.py --check-auth

# Authenticate (visible)
.venv/Scripts/python.exe .claude/perplexity_bridge.py --check-auth --visible

# Clear session
.venv/Scripts/python.exe .claude/perplexity_bridge.py --clear-session

# Test query
.venv/Scripts/python.exe .claude/perplexity_bridge.py --query "test"

# View logs
type .claude\perplexity_bridge.log
```

---

## Next Steps After Authentication

1. ✅ **Test first research query** - Verify it's working
2. ✅ **Try different modes** - research, copilot, focus
3. ✅ **Use with smart commands** - /smart-plan, /smart-debug, /smart-optimize
4. ✅ **Build a real project** - Full integration workflow

---

## Support

**If authentication fails after multiple attempts:**

1. Check Perplexity Pro subscription is active
2. Try logging in manually at https://www.perplexity.ai
3. Clear browser cache: `--clear-session`
4. Check logs: `.claude/perplexity_bridge.log`
5. Verify Chromium installed: `playwright install chromium`

**Authentication is optional** - You can use all orchestration features without it. Research queries will use Claude's knowledge instead.

---

*For detailed system documentation, see `.claude/README.md`*
