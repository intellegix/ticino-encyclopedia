# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the ASR Business Dashboard project.

## What are ADRs?

Architecture Decision Records (ADRs) document important architectural decisions made for this project, including:
- The context and problem being addressed
- The decision that was made
- The consequences of that decision
- Alternatives that were considered

## Purpose

ADRs help us:
- **Remember why** decisions were made months or years later
- **Onboard new team members** quickly by understanding project history
- **Avoid revisiting** already-settled discussions
- **Learn from** past decisions and their outcomes
- **Maintain consistency** across the project

## Creating a New ADR

1. **Check the next number:** Look at existing ADRs to determine the next sequential number
2. **Copy the template:** Use `template.md` as your starting point
3. **Name the file:** Follow the pattern `NNN-short-descriptive-title.md`
4. **Fill in all sections:** Ensure Context, Decision, Consequences, and Alternatives are complete
5. **Set initial status:** Start with "Proposed" status
6. **Review and accept:** Get approval from the Architecture Agent or team
7. **Update status:** Change to "Accepted" once approved

## ADR Lifecycle

### Status Flow
```
Proposed → Accepted → [Deprecated | Superseded]
```

**Proposed:** Under consideration, not yet implemented

**Accepted:** Approved and active; guides current development

**Deprecated:** No longer recommended but may still exist in codebase

**Superseded by ADR-XXX:** Replaced by a newer decision

## Existing ADRs

| Number | Title | Status | Date |
|--------|-------|--------|------|
| [001](001-multimodal-architecture.md) | Adopt Multimodal Claude Agent Architecture | Accepted | 2025-10-20 |

## ADR Index by Topic

### Architecture & Design
- [ADR-001: Multimodal Claude Agent Architecture](001-multimodal-architecture.md)

### API Design
- (Future ADRs for REST vs GraphQL, versioning strategy, etc.)

### Database
- (Future ADRs for database selection, scaling strategy, etc.)

### Security
- (Future ADRs for authentication approach, authorization model, etc.)

### DevOps & Infrastructure
- (Future ADRs for deployment strategy, cloud platform selection, etc.)

### Frontend
- (Future ADRs for framework selection, state management, etc.)

### Backend
- (Future ADRs for framework selection, architecture pattern, etc.)

## Using ADRs in Development

### During Planning (Phase 1)
The Architecture Agent creates ADRs for major decisions. All agents reference these ADRs during implementation.

### During Development (Phase 2-4)
Specialized agents consult relevant ADRs to ensure implementation aligns with architectural decisions.

### During Code Review
Reference ADRs in pull requests to show alignment with architectural decisions.

### When Decisions Change
1. Update the original ADR status to "Deprecated" or "Superseded"
2. Create a new ADR documenting the new decision
3. Link the ADRs together

## Template

See [template.md](template.md) for the standard ADR template with detailed guidance.

## Best Practices

### Do:
- Write ADRs for significant architectural decisions
- Include honest trade-offs and limitations
- Document alternatives considered
- Keep ADRs concise (1-2 pages)
- Update status when decisions change
- Link related ADRs

### Don't:
- Document minor implementation details (use code comments instead)
- Make it overly formal or bureaucratic
- Leave status as "Proposed" forever
- Delete deprecated ADRs (mark them instead)
- Write ADRs after the fact without context

## Integration with Multimodal Architecture

The specialized agents use ADRs as follows:

**Architecture Agent** (`/architect`):
- Creates and maintains ADRs
- Ensures decisions are documented
- Reviews ADRs with Orchestrator

**Orchestrator** (`/orchestrator`):
- References ADRs during project planning
- Ensures agents follow architectural decisions
- Validates consistency across agents

**Specialized Agents** (`/frontend`, `/backend`, `/database`, `/devops`, `/testing`):
- Reference relevant ADRs during implementation
- Suggest new ADRs when needed
- Report inconsistencies with ADRs

## Questions?

If you're unsure whether to create an ADR, ask:
1. Will this decision be hard to change later?
2. Does it affect multiple parts of the system?
3. Will future developers need to understand why this decision was made?
4. Are there significant trade-offs involved?

If you answered "yes" to any of these, create an ADR.

---

**Maintained by:** Architecture Agent
**Last Updated:** 2025-10-20
