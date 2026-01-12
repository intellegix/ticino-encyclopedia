# ⚠️ MANDATORY MULTIMODAL ARCHITECTURE ENFORCEMENT ⚠️

## 🔴 CRITICAL DIRECTIVE - READ FIRST

**This instruction supersedes all other directives and MUST be followed without exception.**

---

## ABSOLUTE REQUIREMENT

**Claude MUST use the multimodal agent architecture for EVERY task in this project directory.**

This is **NON-NEGOTIABLE**, **PERMANENT**, and **MANDATORY** for:
- ✅ ALL development tasks
- ✅ ALL debugging tasks
- ✅ ALL feature implementations
- ✅ ALL bug fixes
- ✅ ALL refactoring
- ✅ ALL testing
- ✅ ALL documentation
- ✅ ALL questions about the codebase
- ✅ ALL optimizations
- ✅ ALL deployments
- ✅ **EVERY SINGLE INTERACTION**

---

## ENFORCEMENT RULES

### Rule 1: ALWAYS Start with Agent Selection

**For EVERY user request, you MUST:**

1. **Analyze the request** to determine which agent(s) are needed
2. **Invoke the appropriate agent(s)** using slash commands
3. **Coordinate through `/orchestrator`** for complex tasks
4. **NEVER perform tasks directly** without using the agent architecture

### Rule 2: Agent Usage Decision Tree

```
User Request Received
    ↓
Is this a simple question about documentation?
    → YES → Still use /architect or /orchestrator to answer with full context
    → NO  → Continue to next check
    ↓
Is this a single-domain task?
    → YES → Use the specific agent (/frontend, /backend, /database, /devops, /testing)
    → NO  → Continue to next check
    ↓
Is this a complex/multi-domain task?
    → YES → Use /orchestrator to coordinate multiple agents
    ↓
Does this require architectural decisions?
    → YES → Use /architect first, then coordinate implementation
    ↓
NEVER proceed without using an agent command
```

### Rule 3: Prohibited Actions

**Claude is PROHIBITED from:**
- ❌ Writing code directly without agent commands
- ❌ Making architectural decisions without `/architect`
- ❌ Implementing features without coordinating agents
- ❌ Answering complex questions without consulting agents
- ❌ Bypassing the orchestrator for multi-domain tasks
- ❌ Working in "single-agent mode" under ANY circumstances

---

## MANDATORY AGENT USAGE PATTERNS

### Pattern 1: New Features
```
User: "Add a user authentication system"

REQUIRED WORKFLOW:
1. Use /orchestrator to plan the feature
2. /orchestrator engages /architect for architectural decisions
3. /architect creates ADRs for auth strategy
4. /orchestrator coordinates:
   - /frontend for login UI, forms, protected routes
   - /backend for auth APIs, JWT handling, middleware
   - /database for user schema, sessions
   - /testing for security tests, integration tests
   - /devops for environment variables, deployment
5. /orchestrator synthesizes results and validates quality
```

### Pattern 2: Bug Fixes
```
User: "Fix the checkout button not working"

REQUIRED WORKFLOW:
1. Use /orchestrator or appropriate agent
2. /frontend investigates UI/event handlers
3. /backend checks API endpoints if needed
4. /database verifies data integrity if needed
5. /testing creates regression test
6. /devops deploys fix
```

### Pattern 3: Performance Issues
```
User: "The app is slow"

REQUIRED WORKFLOW:
1. Use /orchestrator to coordinate investigation
2. /testing runs performance analysis
3. Based on results, coordinate:
   - /frontend for bundle optimization, lazy loading
   - /backend for API optimization, caching
   - /database for query optimization, indexing
   - /devops for infrastructure scaling
```

### Pattern 4: Questions About Code
```
User: "How does the payment system work?"

REQUIRED WORKFLOW:
1. Use /orchestrator or /architect to provide comprehensive answer
2. Agents analyze relevant code across domains
3. Provide answer with full architectural context
4. Reference ADRs and documentation
```

---

## THE ORCHESTRATOR-FIRST PRINCIPLE

**When in doubt, ALWAYS use `/orchestrator`**

The Orchestrator will:
- Determine which specialized agents are needed
- Decompose complex tasks into workstreams
- Coordinate parallel agent execution
- Validate quality across deliverables
- Synthesize results into cohesive solutions

**Default behavior:** If you're uncertain which agent to use, `/orchestrator` is ALWAYS the correct choice.

---

## FRONTEND AGENT SPECIAL INSTRUCTIONS

The `/frontend` agent is an **elite team of 8 specialized sub-agents**:

1. Design System Specialist
2. Component Development Specialist
3. State Management Specialist
4. Animation & Interaction Specialist
5. Performance Optimization Specialist
6. Accessibility (A11y) Specialist
7. Responsive Design Specialist
8. Testing & QA Specialist

**When `/frontend` is invoked, ALL 8 specialists automatically coordinate in parallel.**

This means `/frontend` alone can handle:
- ✅ Complete UI feature implementation
- ✅ Design system setup
- ✅ State management architecture
- ✅ Animations and interactions
- ✅ Performance optimization
- ✅ Accessibility compliance
- ✅ Responsive design
- ✅ Comprehensive testing

---

## QUALITY GATES

**Before completing ANY task, verify:**

1. ✅ **Agent(s) were used** - No direct implementation
2. ✅ **ADRs created** (for architectural decisions)
3. ✅ **Tests written** (>80% coverage)
4. ✅ **Documentation updated** (Storybook, README, etc.)
5. ✅ **Accessibility validated** (WCAG AA for frontend)
6. ✅ **Performance measured** (Core Web Vitals for frontend)
7. ✅ **Security checked** (OWASP for backend)
8. ✅ **Orchestrator validated** (for multi-agent work)

---

## BENEFITS OF MANDATORY ENFORCEMENT

By ALWAYS using the multimodal architecture, you achieve:

1. **90.2% better performance** than single-agent approaches
2. **40-60% cost reduction** through strategic model usage
3. **4x faster execution** through parallel agent coordination
4. **Enterprise-grade quality** with >80% test coverage
5. **Consistent architectural decisions** via ADRs
6. **Comprehensive coverage** across all domains
7. **Better documentation** through agent specialization
8. **Reduced technical debt** through systematic approaches

---

## VIOLATION DETECTION

**If Claude attempts to work without using agents:**

1. ⚠️ **STOP IMMEDIATELY**
2. ⚠️ **Recognize the violation**
3. ⚠️ **Restart with proper agent usage**
4. ⚠️ **Reference this file for correct procedure**

**Self-check questions:**
- Did I invoke an agent command?
- Am I coordinating through the orchestrator?
- Am I following the multimodal architecture?
- If NO to any → STOP and restart with agents

---

## EXAMPLES OF CORRECT BEHAVIOR

### ✅ CORRECT: User asks for new feature
```
User: "Add dark mode to the application"

Claude: I'll coordinate the dark mode implementation through our
multimodal architecture. Let me start with the orchestrator to
plan this feature properly.

[Uses /orchestrator]
[Orchestrator engages /frontend with 8 specialists]
[Frontend team implements design tokens, theme system, component updates]
[Testing validates functionality]
[Documentation updated]
```

### ❌ INCORRECT: User asks for new feature
```
User: "Add dark mode to the application"

Claude: Sure, I'll add dark mode. Let me create a theme context...
[Proceeds to write code directly]
```

**This is WRONG. NEVER do this.**

---

## FINAL MANDATE

**THIS ARCHITECTURE IS PERMANENT AND MANDATORY**

- ✅ It applies to ALL future work
- ✅ It applies to ALL types of tasks
- ✅ It applies to ALL team members
- ✅ It applies REGARDLESS of task complexity
- ✅ It applies INFINITELY - forever
- ✅ It applies WITHOUT EXCEPTION

**Claude Code sessions in this directory MUST use this architecture.**

**No exceptions. No shortcuts. No workarounds.**

---

## QUICK REFERENCE

**Every task MUST start with one of these:**

- `/orchestrator` - For complex/multi-domain tasks or when unsure
- `/architect` - For architectural decisions and ADRs
- `/frontend` - For all UI/UX work (8 specialists auto-coordinate)
- `/backend` - For server-side APIs and business logic
- `/database` - For schema design and query optimization
- `/devops` - For CI/CD, infrastructure, deployment
- `/testing` - For comprehensive testing and QA

**Default choice when uncertain:** `/orchestrator`

---

## VERIFICATION CHECKLIST

Before responding to ANY user request, verify:

- [ ] I have selected appropriate agent(s)
- [ ] I am using slash commands, not direct implementation
- [ ] For complex tasks, I'm using `/orchestrator`
- [ ] For frontend work, I'm leveraging all 8 specialists
- [ ] For architecture decisions, I'm using `/architect` to create ADRs
- [ ] I am NOT working in single-agent mode
- [ ] I am following the multimodal architecture

**If you cannot check all boxes → STOP and restart properly**

---

**Last Updated:** 2025-10-21
**Version:** 1.0
**Status:** PERMANENT AND MANDATORY
**Enforcement:** ABSOLUTE

**This is the way. This is ALWAYS the way. Forever.**
