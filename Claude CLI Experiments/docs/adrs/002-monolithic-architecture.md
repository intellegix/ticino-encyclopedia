# ADR-002: Monolithic Architecture for ASR Ops Dashboard

Date: 2025-10-24

## Status
Accepted

## Context

ASR Ops Dashboard is a construction management and payroll operations platform serving a small to medium-sized team. The application needs to:
- Integrate with Raken API for construction data (projects, timecards, daily reports)
- Manage payroll processing and workers compensation
- Provide real-time dashboards for operations and financial data
- Support role-based access control for different user types
- Handle file uploads and document management
- Process supplier intelligence and pricing data

The team consists of:
- Small development team (1-2 developers)
- Operations staff with varying technical expertise
- Need for rapid feature development and iteration
- Limited DevOps resources
- Single deployment environment initially

## Decision

We will implement a **monolithic layered architecture** with clear separation of concerns:

### Architecture Components

**Frontend Layer (React SPA):**
- Single-page application built with React
- Client-side routing with React Router
- Context API for state management
- Responsive design for desktop and mobile

**Backend Layer (FastAPI):**
- Single Python application using FastAPI framework
- RESTful API endpoints
- Layered structure: Routers → CRUD → Services → Models → Database
- Background job scheduling with APScheduler

**Data Layer (PostgreSQL):**
- Single relational database
- SQLAlchemy ORM for database abstraction
- Support for SQLite in development, PostgreSQL in production

**Integration Layer:**
- Raken API client service
- Supplier intelligence services
- Workers compensation processing service

### Technology Stack Rationale

**Frontend - React:**
- Large ecosystem and community support
- Component reusability
- Familiar to development team
- Excellent tooling and documentation

**Backend - FastAPI:**
- Modern Python framework with automatic API documentation
- Built-in async support for background jobs
- Type hints for better code quality
- Easy integration with SQLAlchemy
- Fast development cycle

**Database - PostgreSQL:**
- Proven reliability for production workloads
- ACID compliance for financial data
- Rich querying capabilities
- Good performance for expected data volumes

## Consequences

### Positive Consequences

**Development Velocity:**
- Single codebase simplifies development and debugging
- Shared business logic across features
- Faster initial development and MVP delivery
- Single deployment reduces complexity
- Easier onboarding for new developers

**Operational Simplicity:**
- Single application to deploy and monitor
- Simpler infrastructure requirements
- Lower hosting costs initially
- Easier to backup and restore
- Straightforward database transactions across features

**Technical Benefits:**
- Simplified dependency management
- Consistent error handling
- Unified authentication and authorization
- Single logging and monitoring setup
- Easier to maintain data consistency

**Team Alignment:**
- Appropriate for small team size
- No need for complex service orchestration
- Reduced coordination overhead between services
- Clear ownership of features

### Negative Consequences

**Scalability Limitations:**
- All components scale together (cannot scale independently)
- Single point of failure
- Larger codebase over time
- Potential performance bottlenecks as data grows
- Database connection pool shared across all features

**Deployment Constraints:**
- Single deployment means all features deploy together
- Higher risk deployments (entire app must restart)
- Cannot deploy features independently
- Downtime affects all users

**Technology Lock-in:**
- Entire backend committed to Python/FastAPI
- Difficult to introduce different technologies
- All features must use same database
- Migration to microservices requires significant refactoring

**Organizational Challenges:**
- As team grows, merge conflicts increase
- Feature teams cannot work completely independently
- Coordination required for shared components
- Testing entire application for each change

### Risks and Mitigation

**Risk: Application becomes too large to manage**
- **Mitigation:** Use modular design with clear boundaries between features
- **Mitigation:** Regular refactoring to maintain code quality
- **Mitigation:** Consider microservices migration if team grows beyond 5-10 developers

**Risk: Performance degradation as data grows**
- **Mitigation:** Implement caching strategies (Redis)
- **Mitigation:** Database query optimization and indexing
- **Mitigation:** Background job processing for heavy operations
- **Mitigation:** Monitor performance metrics continuously

**Risk: Single point of failure**
- **Mitigation:** Implement proper error handling and graceful degradation
- **Mitigation:** Database replication for high availability
- **Mitigation:** Automated backups and disaster recovery procedures
- **Mitigation:** Health check endpoints and monitoring

## Alternatives Considered

### Alternative 1: Microservices Architecture

**Description:** Split application into independent services (Project Service, Payroll Service, Raken Integration Service, etc.)

**Pros:**
- Independent scaling of services
- Technology flexibility per service
- Fault isolation
- Independent deployments
- Better suited for large teams

**Cons:**
- Significantly higher complexity
- Requires service orchestration (Kubernetes, Docker Swarm)
- Distributed transaction challenges
- Network latency between services
- Requires DevOps expertise
- Higher infrastructure costs
- Overkill for current team size

**Why not chosen:** Too complex for current team size and requirements. The operational overhead outweighs the benefits at this scale.

### Alternative 2: Serverless Architecture

**Description:** Use cloud functions (AWS Lambda, Azure Functions) for backend logic

**Pros:**
- Automatic scaling
- Pay per execution
- No server management
- Built-in high availability

**Cons:**
- Cold start latency
- Limited execution time per function
- Vendor lock-in to cloud provider
- Complex state management
- Difficult to debug
- Background job scheduling more complex
- Database connection pooling challenges

**Why not chosen:** Background job requirements (scheduled syncs, backups) and need for long-running processes (WC report processing) make serverless unsuitable.

### Alternative 3: Modular Monolith

**Description:** Monolithic deployment with strict module boundaries internally

**Pros:**
- Better organization than simple monolith
- Easier future migration to microservices
- Module isolation within codebase
- Maintains deployment simplicity

**Cons:**
- Requires strong architectural discipline
- Still shares deployment and scaling characteristics
- Module boundaries can be violated
- Additional complexity without clear immediate benefit

**Why not chosen:** While this is a good pattern, the added complexity of enforcing module boundaries is not justified for current team size. We can evolve toward this pattern as the codebase grows.

## Related Decisions

- ADR-003: Dual Data Model Strategy (Internal + Raken Integration)
- ADR-004: RESTful API Design Pattern
- ADR-006: Database Abstraction Strategy (SQLite/PostgreSQL)
- Future: If application reaches critical scale, will create ADR for microservices migration

## Migration Path (Future)

If the application outgrows the monolithic architecture, migration to microservices should follow this approach:

**Phase 1: Identify Service Boundaries**
- Raken Integration Service (external API integration)
- Workers Compensation Processing Service (batch processing)
- Supplier Intelligence Service (analytics)
- Core Operations Service (projects, time tracking, safety)

**Phase 2: Extract Services One-by-One**
- Start with least-coupled services (Raken Integration, WC Processing)
- Implement service contracts (API specifications)
- Gradually extract and deploy independently
- Maintain monolith for core operations initially

**Phase 3: Event-Driven Communication**
- Implement message broker (RabbitMQ, Kafka)
- Convert synchronous calls to asynchronous events
- Implement saga pattern for distributed transactions

**Triggers for Migration:**
- Team grows beyond 10 developers
- Performance issues cannot be resolved with optimization
- Need for independent scaling of specific features
- Different features require different technology stacks

## Notes

### Current Codebase Size
- **Backend:** ~65 Python files including services, routers, models
- **Frontend:** 96+ React components
- **Database:** 41 database models
- **Lines of Code:** Estimated 30,000+ lines

### Performance Characteristics
- Expected concurrent users: <100
- Expected data volume: <1M records per year
- Response time requirements: <2s for most operations
- Background job processing: Daily syncs, hourly token refresh

### Deployment Environment
- **Development:** SQLite database, local hosting
- **Production:** PostgreSQL database, cloud hosting (AWS/Azure/GCP)
- **Deployment:** Single container or VM
- **Monitoring:** Application-level logging and health checks

## References

- [Monolithic Architecture Pattern](https://martinfowler.com/articles/dont-start-monolith.html)
- [When to use microservices](https://martinfowler.com/articles/microservices.html)
- Team size and architecture decisions research

---

**Next Review Date:** 2026-04-24 (6 months)
**Owner:** Development Team
**Stakeholders:** Operations Team, Management
