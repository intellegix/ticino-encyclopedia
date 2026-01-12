# Claude Code Project Context

**Project:** Perplexity-Assisted Claude Code CLI Integration
**Purpose:** Multimodal research-backed AI development workflows
**Created:** 2025-10-29

---

## Project Architecture

### Core Components

1. **`.claude/` Directory**
   - `simple_research.py` - Main Perplexity research integration script
   - `perplexity_bridge.py` - Original bridge implementation (deprecated in favor of simple_research.py)
   - `config/agent_orchestrator.py` - Multi-agent task orchestration
   - `commands/` - Custom slash commands
   - `sessions/` - Authentication cookies and research results cache

2. **Research Integration**
   - Perplexity Pro authentication via browser cookies
   - Research mode activation (`button[aria-label='Research']`)
   - Automatic text extraction and screenshot capture
   - Results cached in `.claude/sessions/screenshots/`

3. **Agent System**
   - 8 specialized agents: Orchestrator, Architect, Frontend, Backend, Database, DevOps, Testing, Research
   - Task dependency management
   - Parallel and sequential execution support
   - Research task integration via `execute_research_task()`

---

## Coding Standards

### Python

- **Style:** PEP 8 compliant
- **Type Hints:** Use for function signatures
- **Async:** Use `asyncio` for Playwright browser automation
- **Error Handling:** Explicit try/except blocks with descriptive error messages
- **Logging:** Use `logging` module with INFO level for user-facing messages

### File Organization

```
.claude/
├── config/
│   └── agent_orchestrator.py      # Multi-agent orchestration
├── commands/
│   └── perplexity.md               # /perplexity slash command
├── sessions/
│   ├── perplexity_cookies.json    # Authentication (gitignored)
│   └── screenshots/                # Research results
├── simple_research.py              # Main research script
└── perplexity_bridge.py            # Legacy (deprecated)
```

---

## Key Patterns & Workflows

### Research Query Pattern

```bash
# Standard research query (150 second wait)
.venv/Scripts/python.exe .claude/simple_research.py "Your question" 150
```

**Flow:**
1. Load saved Perplexity cookies
2. Navigate to perplexity.ai
3. Type query in search box
4. Click Research mode button
5. Submit and wait for results
6. Extract text + optional screenshot
7. Save to `.claude/sessions/screenshots/research_result.txt`

### Slash Command Usage

```
/perplexity [your research question]
```

Claude automatically:
- Runs `simple_research.py`
- Waits for completion
- Reads and summarizes results
- Presents with sources and follow-ups

### Agent Orchestration Pattern

```python
orchestrator = AgentOrchestrator()
task = AgentTask(
    task_id="research_task_1",
    agent_type=AgentType.RESEARCH,
    description="Research best practices for...",
    priority=TaskPriority.HIGH,
    requires_research=True,
    research_query="Your question here"
)

result = await orchestrator.execute_research_task(task, wait_time=150)
```

---

## Domain-Specific Terminology

### Perplexity Integration

- **Research Mode:** Pro Search with comprehensive sourcing, charts, and advanced reasoning
- **Research Button:** `button[aria-label='Research']` - segmented control to activate Pro mode
- **Session Cookies:** Stored in `.claude/sessions/perplexity_cookies.json`, valid for 23 hours
- **Content Extraction:** `document.body.innerText` for full page text
- **Wait Time:** Typical 120-180 seconds for deep research reports

### Agent Types

- **Orchestrator:** Coordinates all agents, manages dependencies
- **Architect:** System design and architecture decisions
- **Frontend/Backend:** Specialized domain implementations
- **Research:** Perplexity-powered research tasks
- **Testing:** Test generation and validation

### Task Management

- **TaskStatus:** `PENDING`, `IN_PROGRESS`, `COMPLETED`, `FAILED`, `BLOCKED`
- **TaskPriority:** `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`
- **Dependencies:** List of task_ids that must complete first
- **Workflow Phase:** Grouping of tasks with parallel/sequential execution

---

## Testing Protocols

### Manual Testing

**Research Integration:**
```bash
# Test with quick query (30 seconds)
.venv/Scripts/python.exe .claude/simple_research.py "test query" 30

# Verify:
- Browser opens in visible mode
- Research button is clicked
- Results saved to research_result.txt
```

**Slash Command:**
```
/perplexity What are the latest best practices for React 19?
```

**Expected:** Claude runs research, presents formatted summary with sources

### Validation Checklist

- [ ] Perplexity cookies loaded (25 cookies expected)
- [ ] Research mode button clicked successfully
- [ ] Results file created with > 1000 characters
- [ ] Screenshot captured (optional, may timeout on long pages)
- [ ] No authentication errors
- [ ] No Unicode encoding errors in console output

---

## Known Issues & Solutions

### Issue: "Could not activate Research mode"

**Cause:** Research button selector changed or page not fully loaded

**Solution:** Update selector in `simple_research.py` line 55:
```python
research_btn = await page.wait_for_selector("button[aria-label='Research']", timeout=3000)
```

### Issue: Screenshot timeout

**Cause:** Page is too long for full-page screenshot

**Solution:** Already handled - text extraction happens first, screenshot failure is non-blocking

### Issue: Session expired

**Cause:** Cookies older than 23 hours

**Solution:** Re-import cookies from browser:
```bash
.venv/Scripts/python.exe .claude/import_cookies.py
```

---

## Configuration Files

### `.gitignore` Requirements

```
.claude/sessions/*.json
.claude/sessions/screenshots/*.png
.claude/perplexity_bridge.log
```

### Virtual Environment

- **Location:** `.venv/`
- **Python:** 3.14
- **Key Dependencies:**
  - `playwright` - Browser automation
  - `asyncio` - Async execution

---

## Best Practices

### When to Use Research

- **Architecture decisions:** Get latest best practices
- **Technology selection:** Compare current options
- **Problem solving:** Research error messages and solutions
- **Learning:** Deep dives into new technologies

### Caching Strategy

- Research results auto-saved to `.claude/sessions/screenshots/`
- Reuse recent results when appropriate
- Cookie sessions valid for 23 hours
- No need to re-authenticate daily

### Workflow Recommendations

1. **Plan First:** Use agent orchestrator for complex multi-step tasks
2. **Research Early:** Use `/perplexity` before major decisions
3. **Iterate:** Run shorter queries (60-90s) for quick answers
4. **Deep Dive:** Use 150-180s for comprehensive research reports

---

## Quick Reference

### Common Commands

```bash
# Research query
.venv/Scripts/python.exe .claude/simple_research.py "question" 150

# Generate project plan
.venv/Scripts/python.exe .claude/config/agent_orchestrator.py --project "description" --architecture microservices

# Import fresh cookies
.venv/Scripts/python.exe .claude/import_cookies.py
```

### File Locations

- **Research Results:** `.claude/sessions/screenshots/research_result.txt`
- **Screenshots:** `.claude/sessions/screenshots/research_result.png`
- **Cookies:** `.claude/sessions/perplexity_cookies.json`
- **Execution Plans:** `.claude/execution_plan.json`

---

## Success Metrics

- **Authentication:** 25 cookies loaded successfully
- **Research Quality:** 4,000+ characters for comprehensive queries
- **Success Rate:** >90% query success (excluding network issues)
- **Speed:** 2-3 minutes average for deep research

---

*This file is auto-read by Claude Code to understand project context and patterns. Update when architecture or workflows change.*
