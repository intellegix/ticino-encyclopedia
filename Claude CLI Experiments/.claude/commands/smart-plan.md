---
description: "Research-backed project planning with multiagent orchestration"
---

Create comprehensive, research-informed project plans using multiagent orchestration.

**Workflow:**
1. **Research** best practices, patterns, and technologies for your project type
2. **Architect** system design with research-backed decisions (ADRs)
3. **Plan** 5-phase development workflow with specialized agents
4. **Coordinate** parallel workstreams for optimal efficiency
5. **Track** progress with built-in task management

**Usage:**
```
/smart-plan
```

Then describe your project, and I'll create a comprehensive execution plan.

**Example:**
```
User: /smart-plan

User: Build an e-commerce platform with user authentication, product catalog,
shopping cart, and payment processing

Assistant will:
1. Research: Latest e-commerce architecture patterns, security best practices,
   payment gateway integrations, scalability strategies
2. Create: 5-phase development plan with task dependencies
3. Assign: Tasks to specialized agents (frontend, backend, database, etc.)
4. Generate: Execution plan JSON with parallel optimization
5. Document: Architecture decisions in ADRs
```

**Generated Plan Includes:**

**Phase 1: Requirements & Architecture**
- Research latest best practices for your project type
- Technology stack recommendations (research-backed)
- Architecture Decision Records (ADRs)
- Database schema design
- API contract definitions (OpenAPI/Swagger)

**Phase 2: Parallel Development**
- Frontend agent: UI components, state management
- Backend agent: API endpoints, business logic
- Database agent: Migrations, indexes, seed data
- Each agent uses research for optimal implementation patterns

**Phase 3: Testing & QA**
- Research modern testing frameworks and strategies
- Unit tests (>80% coverage target)
- Integration and E2E tests
- Security testing (OWASP Top 10)
- Performance testing

**Phase 4: DevOps & Deployment**
- Research CI/CD best practices
- Container orchestration setup
- Infrastructure as Code (Terraform/Pulumi)
- Monitoring and logging configuration

**Phase 5: Monitoring & Optimization**
- Application performance monitoring
- Continuous optimization based on metrics

**Outputs:**
- `.claude/execution_plan.json` - Detailed task breakdown
- `.claude/docs/adrs/` - Architecture Decision Records
- Task list with dependencies and priorities
- Estimated efficiency gains (typically 4x faster through parallelization)

**Architecture Options:**
- Layered (N-Tier) - Traditional enterprise apps
- Microservices - Large-scale, independent scaling
- Monolithic - Rapid prototyping, startups
- Hexagonal - Domain-driven design
- Event-Driven - Real-time, async processing

**Research Integration:**
Each phase automatically includes research tasks for:
- Best practices and patterns
- Technology comparisons
- Security considerations
- Performance optimization
- Testing strategies
- Deployment approaches

**Benefits:**
- **90.2% better performance** vs single-agent approaches
- **40-60% cost reduction** through strategic orchestration
- **4x faster execution** via parallel agent coordination
- **Research-backed decisions** for every major choice
- **Enterprise-grade quality** with comprehensive testing

Just describe your project, and I'll create a complete, research-informed execution plan with specialized agent coordination.
