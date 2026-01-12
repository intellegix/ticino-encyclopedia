---
description: "Query Perplexity Research Mode for in-depth, well-sourced answers"
---

Execute a comprehensive research query using Perplexity Pro subscription via headless browser.

**Capabilities:**
- Deep research with multiple authoritative sources
- Automatic citation and source extraction
- Related questions for follow-up exploration
- Results cached for 1 hour for efficiency
- Integrates with multiagent workflow for context-aware development

**Usage:**
```bash
/research [your complex research question]
```

**Examples:**
```bash
# Research best practices
/research modern React state management patterns and performance optimization

# Technical deep-dive
/research PostgreSQL indexing strategies for high-traffic applications

# Architecture decisions
/research microservices vs monolithic architecture trade-offs for e-commerce platforms

# Security research
/research OWASP Top 10 mitigation strategies for Node.js applications

# DevOps investigation
/research Kubernetes autoscaling best practices and cost optimization
```

**How it works:**
1. Connects to your authenticated Perplexity session (one-time login)
2. Executes query in Research Mode (Pro Search) for comprehensive analysis
3. Extracts answer, sources, and related questions
4. Caches results for 1 hour to minimize API usage
5. Returns structured JSON with answer and citations

**Authentication:**
- First use requires browser login (one-time, 23-hour session)
- Subsequent queries use cached authentication automatically
- To re-authenticate: `python .claude/perplexity_bridge.py --clear-session`

**Integration with Agents:**
This research capability is automatically used by specialized agents when they need:
- Latest best practices and patterns
- Technology comparisons and recommendations
- Security vulnerability information
- Performance optimization strategies
- Framework and library documentation

**Troubleshooting:**
- If authentication fails: `python .claude/perplexity_bridge.py --check-auth`
- View logs: `tail -f .claude/perplexity_bridge.log`
- Clear cache: `python .claude/perplexity_bridge.py --clear-cache`
