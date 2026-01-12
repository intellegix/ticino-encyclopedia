# Development Workflow Phases

This directory contains detailed workflow templates for the 5-phase enterprise development process used by the multimodal Claude agent team.

## Overview

The multimodal architecture follows a structured, phase-based approach to software development:

```
Phase 1: Requirements & Architecture
    ↓
Phase 2: Parallel Development (Frontend, Backend, Database)
    ↓
Phase 3: Testing & Quality Assurance
    ↓
Phase 4: DevOps & Deployment
    ↓
Phase 5: Monitoring & Maintenance (Ongoing)
```

## Phase Documents

### [Phase 1: Requirements and Architecture](phase-1-requirements-architecture.md)
**Lead:** Architecture Agent + Orchestrator
**Objective:** Establish project foundation

**Key Activities:**
- Requirements gathering
- Architectural decision making (documented in ADRs)
- Technology stack selection
- Database schema design
- API contract definition
- Security planning

**Deliverables:**
- Requirements specification
- Architecture Decision Records
- System architecture diagrams
- Database schema (ERD)
- API specifications (OpenAPI/GraphQL)

**Timeline:** 2 days - 3 weeks (depending on project size)

---

### [Phase 2: Parallel Development](phase-2-parallel-development.md)
**Lead:** Frontend, Backend, Database Agents (simultaneously)
**Objective:** Implement system components in parallel

**Key Activities:**
- Frontend: Component development, state management, API integration
- Backend: API implementation, business logic, authentication
- Database: Schema implementation, migrations, indexing

**Deliverables:**
- Frontend components with Storybook docs
- Backend API with documentation
- Database migrations and seed data
- Unit tests for all components

**Timeline:** 1-12 weeks (depending on project size)

**Critical Success Factor:** Coordination through well-defined API contracts

---

### [Phase 3: Testing and Quality Assurance](phase-3-testing-qa.md)
**Lead:** Testing Agent
**Objective:** Comprehensive testing and quality validation

**Key Activities:**
- Unit testing (>80% coverage)
- Integration testing (API, database)
- End-to-end testing (critical flows)
- Performance testing
- Security testing (OWASP Top 10)
- Accessibility testing (WCAG 2.1)

**Deliverables:**
- Comprehensive test suites
- Code coverage reports
- Performance testing results
- Security audit report
- Accessibility compliance report

**Timeline:** 1-4 weeks (depending on project size)

---

### [Phase 4: DevOps and Deployment](phase-4-devops-deployment.md)
**Lead:** DevOps Agent
**Objective:** Automate deployment and establish production infrastructure

**Key Activities:**
- CI/CD pipeline configuration
- Containerization (Docker)
- Orchestration (Kubernetes)
- Infrastructure as Code (Terraform)
- Monitoring and logging setup
- Security configuration

**Deliverables:**
- CI/CD pipeline
- Container orchestration
- Infrastructure code
- Monitoring dashboards
- Deployment runbooks

**Timeline:** 1-4 weeks (depending on infrastructure complexity)

---

### [Phase 5: Monitoring and Maintenance](phase-5-monitoring-maintenance.md)
**Lead:** All Agents (ongoing collaboration)
**Objective:** Continuous monitoring, optimization, and maintenance

**Key Activities:**
- Application performance monitoring
- Incident response and management
- Performance optimization
- Security monitoring
- Feature development
- Dependency management
- Cost optimization

**Deliverables:**
- Performance reports
- Incident reports and post-mortems
- Optimization improvements
- Security scan results
- New features and enhancements

**Timeline:** Ongoing (continuous)

## Phase Gates

Each phase has a **Phase Gate** checklist to validate readiness before proceeding:

**Phase 1 → Phase 2:**
- [ ] All ADRs created and accepted
- [ ] Technology stack selected
- [ ] API contracts defined
- [ ] Database schema designed

**Phase 2 → Phase 3:**
- [ ] All components implemented
- [ ] Frontend-backend integration working
- [ ] Basic tests passing
- [ ] Documentation complete

**Phase 3 → Phase 4:**
- [ ] Test coverage >80%
- [ ] All tests passing
- [ ] Security vulnerabilities addressed
- [ ] Performance benchmarks met

**Phase 4 → Phase 5:**
- [ ] CI/CD pipeline operational
- [ ] Infrastructure deployed
- [ ] Monitoring active
- [ ] Production deployment successful

## Using These Workflows

### For New Projects

1. **Start with Phase 1:**
   - Use `/orchestrator` to initiate the project
   - Orchestrator will engage `/architect` for architectural decisions
   - Follow Phase 1 checklist completely

2. **Progress Sequentially:**
   - Complete each phase gate before moving forward
   - Document all decisions in ADRs
   - Coordinate between agents as needed

3. **Validate Quality:**
   - Use phase gate checklists
   - Don't skip phases or rush through
   - Quality in early phases prevents issues later

### For Existing Projects

**Adding New Features:**
- Start at Phase 1 (if architectural changes) or Phase 2 (if using existing architecture)
- Follow relevant phase guidelines
- Ensure Phase 3 (testing) before deployment

**Fixing Bugs:**
- Identify the phase most relevant to the bug
- Use appropriate specialist agent
- Follow Phase 3 for testing fixes
- Deploy via Phase 4 process

**Performance Optimization:**
- Use Phase 5 guidance for continuous optimization
- Test changes in Phase 3
- Deploy via Phase 4 process

**Infrastructure Changes:**
- Review Phase 1 for architectural decisions
- Implement in Phase 4
- Monitor in Phase 5

## Phase Timelines

**Small Project (MVP, prototype):**
- Phase 1: 2-3 days
- Phase 2: 1-2 weeks
- Phase 3: 1-2 weeks
- Phase 4: 1-2 weeks
- Phase 5: Ongoing
- **Total to Production: 4-6 weeks**

**Medium Project (full-featured application):**
- Phase 1: 1 week
- Phase 2: 3-4 weeks
- Phase 3: 2-3 weeks
- Phase 4: 2-3 weeks
- Phase 5: Ongoing
- **Total to Production: 8-11 weeks**

**Large Project (enterprise system):**
- Phase 1: 2-3 weeks
- Phase 2: 6-12 weeks
- Phase 3: 3-4 weeks
- Phase 4: 3-4 weeks
- Phase 5: Ongoing
- **Total to Production: 14-23 weeks**

## Integration with Specialized Agents

Each phase leverages specific specialized agents:

| Phase | Primary Agents | Supporting Agents |
|-------|---------------|------------------|
| Phase 1 | Architect, Orchestrator | All (for input) |
| Phase 2 | Frontend, Backend, Database | Architect (for questions) |
| Phase 3 | Testing | Frontend, Backend (for fixes) |
| Phase 4 | DevOps | Database (for migrations) |
| Phase 5 | All | Orchestrator (for coordination) |

## Success Metrics

Track these metrics throughout the phases:

**Phase 1:**
- ADRs created: All major decisions documented
- Architecture diagrams: Complete and reviewed
- API contracts: Fully specified

**Phase 2:**
- Code completion: 100% of planned features
- Integration: Frontend-backend communication working
- Basic tests: Unit tests passing

**Phase 3:**
- Test coverage: >80%
- Security: 0 critical/high vulnerabilities
- Performance: Benchmarks met

**Phase 4:**
- CI/CD: Automated pipeline functional
- Deployment: Successful production deployment
- Monitoring: Dashboards and alerts active

**Phase 5:**
- Uptime: >99.9%
- MTTR: <1 hour for P0/P1 incidents
- User satisfaction: >4.0/5.0

## Best Practices Across All Phases

1. **Document Everything:** ADRs, runbooks, API docs, code comments
2. **Test Continuously:** Don't wait for Phase 3 to start testing
3. **Coordinate Frequently:** Agents should sync regularly
4. **Automate Repetitively:** If you do it twice, automate it
5. **Monitor Proactively:** Catch issues before users report them
6. **Iterate Based on Feedback:** Use real-world data to improve

## Common Patterns

**Feature Development (Existing Project):**
```
Phase 1 (light) → Phase 2 → Phase 3 → Phase 4 (deploy) → Phase 5 (monitor)
```

**Bug Fix:**
```
Phase 2 (fix) → Phase 3 (test) → Phase 4 (deploy) → Phase 5 (verify)
```

**Performance Optimization:**
```
Phase 5 (identify) → Phase 2 (optimize) → Phase 3 (benchmark) → Phase 4 (deploy)
```

**Infrastructure Change:**
```
Phase 1 (ADR) → Phase 4 (implement) → Phase 5 (monitor)
```

## Questions?

If you're unsure which phase to be in or what to do:

1. **Use `/orchestrator`** to get strategic guidance
2. **Review the relevant phase document** for detailed checklists
3. **Check ADRs** in `.claude/docs/adrs/` for past decisions
4. **Consult the Multimodal Blueprint** in `.claude/MULTIMODAL_BLUEPRINT.md`

## Related Documentation

- [Multimodal Blueprint](../ MULTIMODAL_BLUEPRINT.md) - Complete architecture overview
- [Specialized Agent Commands](../commands/) - Agent-specific guidance
- [Architecture Decision Records](../docs/adrs/) - Documented decisions

---

**Remember:** These phases provide structure, but remain flexible. Small projects may move through phases quickly; large projects may iterate within phases. Use the orchestrator to adapt the workflow to your specific needs.

**Last Updated:** 2025-10-20
