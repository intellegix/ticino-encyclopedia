# ADR Template

Use this template for creating new Architecture Decision Records.

## File Naming Convention
`NNN-short-title.md`

Examples:
- `001-choose-database.md`
- `002-api-design-strategy.md`
- `003-authentication-approach.md`

## ADR Structure

```markdown
# [ADR Number]: [Short Title]

Date: YYYY-MM-DD

## Status
<!-- Choose one: Proposed | Accepted | Deprecated | Superseded by ADR-XXX -->
Proposed

## Context
<!-- What is the issue that we're seeing that is motivating this decision or change? -->
<!-- Include relevant background information, constraints, and requirements. -->
<!-- This section should be objective and factual. -->

## Decision
<!-- What is the change that we're proposing and/or doing? -->
<!-- This should be in active voice: "We will..." -->
<!-- Be specific and concrete. Include technical details if relevant. -->

## Consequences
<!-- What becomes easier or more difficult to do because of this change? -->
<!-- Include both positive and negative consequences. -->
<!-- Be honest about trade-offs. -->

### Positive Consequences
-
-

### Negative Consequences
-
-

### Risks
-

## Alternatives Considered
<!-- What other options did we consider? -->
<!-- Why were they not chosen? -->

### Alternative 1: [Name]
**Description:**

**Pros:**
-

**Cons:**
-

**Why not chosen:**

## Related Decisions
<!-- Links to related ADRs -->
- ADR-XXX: [Title]

## Notes
<!-- Any additional information, links to resources, or discussion points -->
```

## ADR Best Practices

### When to Create an ADR

Create an ADR for:
- Significant architectural decisions affecting the system structure
- Technology stack choices (frameworks, databases, languages)
- API design strategies (REST vs GraphQL)
- Authentication/authorization approaches
- Deployment and infrastructure decisions
- Major design pattern selections
- Data storage strategies
- Third-party service integrations

### When NOT to Create an ADR

Don't create ADRs for:
- Minor implementation details
- Code style preferences (use linters instead)
- Temporary solutions
- Individual bug fixes
- Routine maintenance tasks

### Writing Effective ADRs

**Be Specific:** Include concrete technical details, not vague generalizations.

**Be Honest:** Document the real reasons for decisions, including political or resource constraints.

**Include Context:** Future readers need to understand the situation at decision time.

**Document Alternatives:** Show what options were considered and why they were rejected.

**Acknowledge Trade-offs:** Every decision has pros and cons. Be transparent.

**Keep it Short:** Aim for 1-2 pages. Link to external documents for details.

**Update Status:** Mark as Deprecated or Superseded when decisions change.

### Status Definitions

**Proposed:** Decision is being considered but not yet accepted.

**Accepted:** Decision has been approved and is being implemented or is active.

**Deprecated:** Decision is no longer recommended but may still be in use.

**Superseded by ADR-XXX:** Decision has been replaced by a newer decision.

## Example Usage

### Creating a New ADR

1. Copy this template
2. Determine the next ADR number (check `.claude/docs/adrs/` directory)
3. Create file: `NNN-descriptive-title.md`
4. Fill in all sections
5. Set status to "Proposed"
6. Review with team (Architecture Agent)
7. Update status to "Accepted" when approved

### Updating an Existing ADR

**If decision changes:**
1. Update status to "Deprecated" or "Superseded by ADR-XXX"
2. Create new ADR documenting the new decision
3. Link the two ADRs together

**If adding information:**
1. Add to Notes section
2. Update Date to show last modification

## ADR Review Checklist

Before finalizing an ADR, ensure:

- [ ] Title is clear and descriptive
- [ ] Date is included
- [ ] Status is set appropriately
- [ ] Context explains the problem clearly
- [ ] Decision is specific and actionable
- [ ] Both positive and negative consequences are documented
- [ ] Alternatives were considered and documented
- [ ] Trade-offs are acknowledged
- [ ] Related ADRs are linked
- [ ] Technical details are sufficient for implementation
- [ ] Language is clear and jargon is explained

## Integration with Development Workflow

### Phase 1: Requirements and Architecture
- Architecture Agent creates ADRs for major decisions
- Orchestrator reviews and approves
- ADRs guide Phase 2 implementation

### During Development
- Specialized agents reference ADRs for guidance
- New decisions trigger new ADRs
- ADRs are updated as needed

### Code Reviews
- Reference relevant ADRs in pull requests
- Verify implementation matches ADR decisions
- Update ADRs if implementation reveals new information

---

**Note:** This template is maintained in `.claude/docs/adrs/template.md`. Update this file to improve the ADR process for all team members.
