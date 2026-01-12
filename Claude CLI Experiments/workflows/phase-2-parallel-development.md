# Phase 2: Parallel Development

**Lead Agents:** Frontend Agent, Backend Agent, Database Agent (working simultaneously)

**Objective:** Implement the system components in parallel according to the architecture defined in Phase 1.

## Overview

In Phase 2, three specialized agents work simultaneously on their respective domains:
- **Frontend Agent** builds the user interface
- **Backend Agent** implements APIs and business logic
- **Database Agent** creates schema, migrations, and data layer

**Key Success Factor:** Coordination through well-defined contracts from Phase 1.

## Prerequisites from Phase 1

Before starting Phase 2, ensure you have:
- [ ] Architecture Decision Records (ADRs) for all major decisions
- [ ] API contracts defined (OpenAPI/GraphQL schema)
- [ ] Database schema designed (ERD)
- [ ] Technology stack selected
- [ ] Security requirements identified

## Parallel Workstreams

### Workstream A: Frontend Development

**Responsible:** Frontend Agent (`/frontend`)

#### Setup Tasks
- [ ] Initialize project with chosen framework (React, Vue.js, Angular)
- [ ] Configure build tool (Vite, Webpack)
- [ ] Setup linting and formatting (ESLint, Prettier)
- [ ] Configure TypeScript (if applicable)
- [ ] Setup testing framework (Jest, Vitest)

#### Component Development
- [ ] Create component library structure
- [ ] Implement design system / UI kit
- [ ] Build reusable components
- [ ] Setup Storybook for component documentation
- [ ] Ensure accessibility compliance (WCAG 2.1)
- [ ] Implement responsive design

#### State Management
- [ ] Setup state management solution (Redux, Zustand, Context API)
- [ ] Define state structure
- [ ] Implement state normalization
- [ ] Create actions/reducers or equivalent
- [ ] Implement persistence if needed

#### API Integration
- [ ] Create API client layer
- [ ] Implement HTTP interceptors for auth
- [ ] Setup error handling
- [ ] Implement request/response transformation
- [ ] Add loading and error states
- [ ] Implement retry logic

#### Forms and Validation
- [ ] Implement form components
- [ ] Add client-side validation
- [ ] Implement error display
- [ ] Add form submission handling
- [ ] Implement field-level and form-level validation

#### Routing and Navigation
- [ ] Setup routing (React Router, Vue Router, Angular Router)
- [ ] Implement protected routes
- [ ] Add navigation components
- [ ] Implement deep linking
- [ ] Add breadcrumbs if needed

#### Performance Optimization
- [ ] Implement code splitting
- [ ] Add lazy loading for routes and components
- [ ] Optimize images and assets
- [ ] Implement virtual scrolling for large lists
- [ ] Add performance monitoring

**Deliverables:**
- Component library with Storybook documentation
- State management implementation
- API integration layer
- Form validation and error handling
- Responsive, accessible UI
- Unit tests for components

**Coordination Points:**
- Verify API contracts with Backend Agent
- Report any API contract issues to Orchestrator
- Coordinate authentication flow with Backend Agent

---

### Workstream B: Backend Development

**Responsible:** Backend Agent (`/backend`)

#### Setup Tasks
- [ ] Initialize project with chosen framework
- [ ] Configure development environment
- [ ] Setup linting and formatting
- [ ] Configure ORM/database library
- [ ] Setup logging framework
- [ ] Configure environment variables

#### API Implementation
- [ ] Implement API endpoints per contract (REST or GraphQL)
- [ ] Create request/response serialization
- [ ] Implement proper HTTP status codes
- [ ] Add API versioning
- [ ] Implement pagination
- [ ] Add filtering and sorting capabilities
- [ ] Create API documentation (Swagger/GraphQL Playground)

#### Business Logic Layer
- [ ] Create service layer for business logic
- [ ] Implement domain models
- [ ] Add business rule validation
- [ ] Implement error handling
- [ ] Add transaction management
- [ ] Create repository pattern for data access

#### Authentication and Authorization
- [ ] Implement authentication middleware (JWT, OAuth 2.0)
- [ ] Create user registration endpoint
- [ ] Implement login/logout endpoints
- [ ] Add password hashing
- [ ] Implement token refresh mechanism
- [ ] Create authorization middleware (RBAC)
- [ ] Protect endpoints with auth guards

#### Input Validation and Security
- [ ] Implement request validation (JSON schema, class validators)
- [ ] Add input sanitization
- [ ] Implement rate limiting
- [ ] Add security headers (HSTS, CSP, X-Frame-Options)
- [ ] Implement CORS properly
- [ ] Add SQL injection prevention (parameterized queries)
- [ ] Implement XSS prevention

#### Error Handling and Logging
- [ ] Implement global error handler
- [ ] Create custom error classes
- [ ] Add structured logging
- [ ] Implement request logging
- [ ] Add error tracking integration
- [ ] Create meaningful error messages

#### Background Jobs (if needed)
- [ ] Setup message queue (RabbitMQ, Kafka, Redis)
- [ ] Implement job processors
- [ ] Add job scheduling
- [ ] Implement retry logic
- [ ] Add job monitoring

**Deliverables:**
- API endpoints (REST or GraphQL)
- Business logic services
- Authentication/authorization middleware
- Input validation and sanitization
- Comprehensive error handling and logging
- Rate limiting and security headers
- API documentation
- Unit and integration tests

**Coordination Points:**
- Verify API implementation matches contract with Frontend Agent
- Coordinate database queries with Database Agent
- Report schema issues to Database Agent
- Coordinate authentication tokens with Frontend Agent

---

### Workstream C: Database Development

**Responsible:** Database Agent (`/database`)

#### Schema Implementation
- [ ] Create database migrations
- [ ] Implement tables/collections per ERD
- [ ] Define primary keys and auto-increment
- [ ] Create foreign key constraints
- [ ] Add unique constraints
- [ ] Implement check constraints
- [ ] Add default values

#### Indexing Strategy
- [ ] Create indexes on frequently queried columns
- [ ] Implement composite indexes for multi-column queries
- [ ] Add full-text search indexes if needed
- [ ] Monitor index usage
- [ ] Remove unused indexes

#### Data Seeding
- [ ] Create seed data for development
- [ ] Generate test data
- [ ] Create data fixtures for testing
- [ ] Implement data anonymization for staging/dev

#### Stored Procedures and Functions (if applicable)
- [ ] Create stored procedures for complex operations
- [ ] Implement database functions
- [ ] Add triggers if needed
- [ ] Document all procedures and functions

#### Migration Management
- [ ] Version control all migrations
- [ ] Test migrations forward and backward
- [ ] Document migration dependencies
- [ ] Create rollback scripts
- [ ] Test on fresh database instance

#### Performance Optimization
- [ ] Analyze query performance
- [ ] Optimize slow queries
- [ ] Implement query result caching
- [ ] Add database connection pooling
- [ ] Monitor database metrics

#### Backup and Recovery
- [ ] Configure automated backups
- [ ] Test backup restoration
- [ ] Document recovery procedures
- [ ] Implement point-in-time recovery
- [ ] Setup backup retention policy

**Deliverables:**
- Database migration scripts
- Seed data
- Indexes and constraints
- Stored procedures (if applicable)
- Backup and recovery procedures
- Database documentation
- Performance tuning recommendations

**Coordination Points:**
- Verify schema matches Backend Agent's ORM models
- Provide query optimization guidance to Backend Agent
- Report schema constraint issues to Architecture Agent

---

## Integration and Coordination

### Daily Coordination Checklist

- [ ] Frontend and Backend: Verify API contract alignment
- [ ] Backend and Database: Verify schema and query alignment
- [ ] All agents: Report blockers to Orchestrator
- [ ] All agents: Share progress updates

### Common Integration Points

**Frontend ↔ Backend:**
- API endpoint URLs
- Request/response formats
- Authentication token handling
- Error response formats
- WebSocket connections (if applicable)

**Backend ↔ Database:**
- ORM model definitions
- Query performance
- Transaction boundaries
- Data type compatibility
- Constraint validation

### Resolving Integration Issues

When integration issues arise:

1. **Identify the issue:** Which contract is unclear or incorrect?
2. **Determine impact:** Does this affect Phase 1 decisions?
3. **Coordinate resolution:**
   - Minor issues: Agents resolve directly
   - Major issues: Escalate to Orchestrator
   - Architecture changes: Update relevant ADRs
4. **Document solution:** Update contracts and documentation

## Quality Standards

All code produced in Phase 2 must meet:

### Code Quality
- [ ] Follows established coding conventions
- [ ] DRY principle (no duplication)
- [ ] SOLID principles (for OOP)
- [ ] Clear, descriptive naming
- [ ] Appropriate comments for complex logic
- [ ] No hardcoded secrets or credentials

### Testing (Preliminary)
- [ ] Unit tests for critical functions/components
- [ ] Integration tests for API endpoints
- [ ] Test coverage >50% (will increase in Phase 3)
- [ ] All tests passing

### Security
- [ ] Input validation implemented
- [ ] Authentication/authorization working
- [ ] Security headers added
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Secrets in environment variables

### Performance (Initial)
- [ ] No obvious performance bottlenecks
- [ ] Database queries optimized
- [ ] API response times reasonable (<500ms for most endpoints)
- [ ] Frontend renders without lag

## Phase Gate: Ready for Phase 3?

Before proceeding to Phase 3 (Testing and QA), validate:

### Implementation Complete
- [ ] All API endpoints implemented
- [ ] Frontend components completed
- [ ] Database migrations written and tested
- [ ] Authentication/authorization working

### Integration Working
- [ ] Frontend can communicate with Backend
- [ ] Backend can query Database
- [ ] End-to-end flows working for critical paths
- [ ] API contracts being followed

### Code Quality
- [ ] Code follows established conventions
- [ ] Basic unit tests in place
- [ ] No hardcoded secrets
- [ ] Security basics implemented

### Documentation
- [ ] API documentation complete (Swagger/GraphQL Playground)
- [ ] Component documentation (Storybook)
- [ ] Database schema documented
- [ ] Setup instructions for all components

## Estimated Timeline

**Small Project:** 1-2 weeks
**Medium Project:** 3-4 weeks
**Large Project:** 6-12 weeks

## Common Pitfalls to Avoid

1. **Breaking API contracts:** Always implement exactly what was specified
2. **Skipping coordination:** Regular sync between agents is critical
3. **Ignoring security early:** Build security in from the start
4. **No integration testing:** Test frontend-backend integration continuously
5. **Poor error handling:** Don't leave error scenarios unhandled
6. **Skipping documentation:** Document as you build, not after
7. **Premature optimization:** Focus on working code first, optimize in Phase 3

## Next Phase

Once Phase 2 is complete and validated, proceed to:

**[Phase 3: Testing and Quality Assurance](phase-3-testing-qa.md)**

The Testing Agent will create comprehensive test suites and validate quality.

---

**Related Documents:**
- [Frontend Agent Command](.claude/commands/frontend.md)
- [Backend Agent Command](.claude/commands/backend.md)
- [Database Agent Command](.claude/commands/database.md)
- [Phase 1: Requirements and Architecture](phase-1-requirements-architecture.md)
- [Phase 3: Testing and QA](phase-3-testing-qa.md)
