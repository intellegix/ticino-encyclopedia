# Phase 4: DevOps and Deployment

**Lead Agent:** DevOps Agent

**Objective:** Automate deployment, configure infrastructure, and establish monitoring for production readiness.

## Overview

Phase 4 transforms tested code into a production-ready system. The DevOps Agent configures CI/CD pipelines, provisions infrastructure, sets up monitoring, and establishes deployment procedures.

## Prerequisites from Phase 3

Before starting Phase 4, ensure you have:
- [ ] All tests passing (unit, integration, E2E)
- [ ] Test coverage >80%
- [ ] Security vulnerabilities addressed
- [ ] Performance benchmarks met
- [ ] Code quality validated

## Workstream: Infrastructure and Deployment

**Responsible:** DevOps Agent (`/devops`)

### 1. CI/CD Pipeline Configuration

**Pipeline Stages:**

```
Trigger → Lint → Test → Security Scan → Build → Deploy to Staging → Smoke Test → Deploy to Production
```

**Stage 1: Trigger**
- [ ] Configure triggers (on push to main, on PR, manual trigger)
- [ ] Define branch protection rules
- [ ] Setup pipeline for multiple branches (dev, staging, main)

**Stage 2: Linting and Code Quality**
- [ ] Run code linters (ESLint, Pylint, Checkstyle)
- [ ] Run code formatters (Prettier, Black)
- [ ] Run static analysis (SonarQube, CodeClimate)
- [ ] Fail pipeline on critical issues

**Stage 3: Testing**
- [ ] Run unit tests
- [ ] Run integration tests
- [ ] Run E2E tests (on staging)
- [ ] Generate code coverage reports
- [ ] Fail pipeline if coverage drops below threshold

**Stage 4: Security Scanning**
- [ ] Run dependency vulnerability scans (Snyk, npm audit, pip-audit)
- [ ] Scan for secrets in code
- [ ] Run container image scanning (Trivy, Clair)
- [ ] Run infrastructure security scanning (Checkov, tfsec)
- [ ] Fail pipeline on critical/high vulnerabilities

**Stage 5: Build**
- [ ] Build frontend (production build)
- [ ] Build backend (compile if needed)
- [ ] Create Docker images
- [ ] Tag images with version and commit SHA
- [ ] Push images to container registry
- [ ] Generate build artifacts

**Stage 6: Deploy to Staging**
- [ ] Deploy to staging environment
- [ ] Run database migrations (if any)
- [ ] Update environment variables
- [ ] Deploy containers/services

**Stage 7: Smoke Tests**
- [ ] Run smoke tests on staging
- [ ] Verify critical endpoints
- [ ] Check health endpoints
- [ ] Validate database connectivity

**Stage 8: Deploy to Production**
- [ ] Require manual approval (for production)
- [ ] Use blue-green or canary deployment
- [ ] Run database migrations (with rollback plan)
- [ ] Update services
- [ ] Monitor deployment

**CI/CD Platform Options:**
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Azure DevOps

**Deliverables:**
- CI/CD pipeline configuration
- Pipeline documentation
- Deployment runbook

### 2. Containerization

**Docker Configuration:**

**Frontend Dockerfile:**
- [ ] Use multi-stage build
- [ ] Install dependencies
- [ ] Build production assets
- [ ] Use nginx or similar for serving
- [ ] Run as non-root user
- [ ] Implement health check

**Backend Dockerfile:**
- [ ] Use multi-stage build
- [ ] Install dependencies
- [ ] Copy application code
- [ ] Run as non-root user
- [ ] Implement health check
- [ ] Use specific base image version (not latest)

**Docker Compose (for local development):**
- [ ] Define all services (frontend, backend, database, redis)
- [ ] Setup networking
- [ ] Configure volumes for persistence
- [ ] Setup environment variables
- [ ] Add health checks

**Best Practices:**
- [ ] Use .dockerignore to reduce image size
- [ ] Minimize layers in Dockerfile
- [ ] Cache dependencies for faster builds
- [ ] Scan images for vulnerabilities
- [ ] Tag images with semantic versions

**Deliverables:**
- Dockerfiles for all services
- Docker Compose configuration
- Container registry setup
- Image scanning results

### 3. Orchestration (Kubernetes)

**If using Kubernetes:**

**Kubernetes Manifests:**
- [ ] Create Deployment manifests
- [ ] Create Service manifests
- [ ] Create Ingress for routing
- [ ] Create ConfigMaps for configuration
- [ ] Create Secrets for sensitive data
- [ ] Define resource requests and limits
- [ ] Implement horizontal pod autoscaling
- [ ] Add liveness and readiness probes

**Helm Charts (recommended):**
- [ ] Create Helm chart for application
- [ ] Define values for different environments
- [ ] Template configuration files
- [ ] Package and version Helm charts

**Best Practices:**
- [ ] Use namespaces for environment separation
- [ ] Implement network policies
- [ ] Use RBAC for access control
- [ ] Configure persistent volumes for stateful services
- [ ] Set up ingress controller
- [ ] Implement pod disruption budgets

**Deliverables:**
- Kubernetes manifests or Helm charts
- Namespace configuration
- Autoscaling configuration
- Documentation

### 4. Infrastructure as Code (IaC)

**Cloud Resources to Provision:**

**AWS Example:**
- [ ] VPC and networking (subnets, security groups)
- [ ] ECS/EKS for container orchestration
- [ ] RDS for database
- [ ] ElastiCache for Redis
- [ ] S3 for static assets
- [ ] CloudFront for CDN
- [ ] Route 53 for DNS
- [ ] ALB/NLB for load balancing
- [ ] IAM roles and policies

**Terraform Configuration:**
- [ ] Define provider and backend (S3 + DynamoDB for state)
- [ ] Create modules for reusable components
- [ ] Define variables for different environments
- [ ] Use workspaces for environment separation
- [ ] Implement remote state management
- [ ] Version control all IaC code

**Best Practices:**
- [ ] Use consistent naming conventions
- [ ] Tag all resources appropriately
- [ ] Implement least privilege access
- [ ] Enable logging for all services
- [ ] Use parameter store for secrets
- [ ] Plan before applying
- [ ] Review state changes

**Deliverables:**
- Terraform/CloudFormation templates
- Infrastructure documentation
- State management setup
- Environment configuration files

### 5. Database Deployment

**Migration Strategy:**
- [ ] Version control all migrations
- [ ] Test migrations on staging first
- [ ] Create rollback scripts
- [ ] Backup database before migrations
- [ ] Use migration tools (Flyway, Liquibase, Alembic)

**Database Configuration:**
- [ ] Setup automated backups
- [ ] Configure point-in-time recovery
- [ ] Implement read replicas (if needed)
- [ ] Setup monitoring and alerts
- [ ] Configure connection pooling
- [ ] Enable encryption at rest and in transit

**Deliverables:**
- Migration deployment process
- Backup and recovery procedures
- Database monitoring setup

### 6. Monitoring and Logging

**Application Performance Monitoring (APM):**
- [ ] Setup APM tool (Datadog, New Relic, AppDynamics)
- [ ] Track API response times
- [ ] Monitor error rates
- [ ] Track custom metrics (user signups, purchases, etc.)
- [ ] Setup dashboards for key metrics
- [ ] Configure alerts for anomalies

**Infrastructure Monitoring:**
- [ ] Monitor CPU, memory, disk usage
- [ ] Track network traffic
- [ ] Monitor database performance
- [ ] Track container metrics
- [ ] Monitor Kubernetes cluster (if applicable)
- [ ] Setup autoscaling based on metrics

**Logging:**
- [ ] Centralize logs (ELK Stack, CloudWatch, Datadog)
- [ ] Implement structured logging (JSON format)
- [ ] Define log levels appropriately
- [ ] Setup log retention policies
- [ ] Implement log-based alerting
- [ ] Create log dashboards

**Metrics to Track:**
- API response time (p50, p95, p99)
- Error rate
- Request throughput
- Database query time
- Cache hit rate
- CPU and memory usage
- Disk usage
- Network latency

**Alerts to Configure:**
- [ ] High error rate (>1% of requests)
- [ ] Slow API response times (p95 >1s)
- [ ] High CPU usage (>80% for 5 minutes)
- [ ] High memory usage (>90%)
- [ ] Disk space low (<20%)
- [ ] Database connection pool exhausted
- [ ] SSL certificate expiring soon

**Tools:**
- Prometheus + Grafana
- Datadog
- New Relic
- ELK Stack (Elasticsearch, Logstash, Kibana)
- AWS CloudWatch
- Azure Monitor
- GCP Cloud Logging

**Deliverables:**
- Monitoring dashboards
- Alert configuration
- Logging aggregation setup
- On-call rotation and escalation procedures

### 7. Security Configuration

**Secrets Management:**
- [ ] Use secrets manager (AWS Secrets Manager, HashiCorp Vault)
- [ ] Rotate secrets regularly
- [ ] Never commit secrets to version control
- [ ] Use different secrets per environment
- [ ] Implement least privilege access to secrets

**Network Security:**
- [ ] Configure VPC with private subnets
- [ ] Use security groups to restrict access
- [ ] Implement network ACLs
- [ ] Enable VPC flow logs
- [ ] Use WAF for web application protection

**SSL/TLS:**
- [ ] Obtain SSL certificates (Let's Encrypt, ACM)
- [ ] Configure HTTPS only
- [ ] Implement HSTS header
- [ ] Setup certificate renewal automation

**Access Control:**
- [ ] Implement RBAC for Kubernetes
- [ ] Use IAM roles for AWS resources
- [ ] Enable MFA for administrative access
- [ ] Audit access logs regularly

**Deliverables:**
- Secrets management setup
- Network security configuration
- SSL/TLS certificate setup
- Access control policies

### 8. Backup and Disaster Recovery

**Backup Strategy:**
- [ ] Automated daily database backups
- [ ] Backup retention policy (30 days recommended)
- [ ] Test backup restoration regularly
- [ ] Store backups in different region
- [ ] Backup configuration files and IaC

**Disaster Recovery Plan:**
- [ ] Define Recovery Time Objective (RTO)
- [ ] Define Recovery Point Objective (RPO)
- [ ] Document recovery procedures
- [ ] Test disaster recovery plan
- [ ] Setup multi-region failover (if needed)

**Deliverables:**
- Backup configuration
- Disaster recovery plan
- Recovery procedure documentation

## Deployment Strategies

### Blue-Green Deployment
- Maintain two identical environments (blue and green)
- Deploy new version to inactive environment
- Switch traffic to new environment
- Keep old environment for quick rollback

### Canary Deployment
- Deploy new version to small subset of users (5-10%)
- Monitor metrics closely
- Gradually increase traffic to new version
- Roll back if issues detected

### Rolling Deployment
- Update instances gradually
- Monitor health during rollout
- Automatic rollback on failures

**Recommended:** Blue-Green for critical applications, Canary for gradual rollouts

## Phase Gate: Ready for Phase 5?

Before proceeding to Phase 5 (Monitoring and Maintenance), validate:

### CI/CD Operational
- [ ] CI/CD pipeline fully configured
- [ ] All pipeline stages working
- [ ] Automated deployment to staging working
- [ ] Production deployment process tested

### Infrastructure Deployed
- [ ] All infrastructure provisioned via IaC
- [ ] Kubernetes/container orchestration configured
- [ ] Database deployed and configured
- [ ] SSL/TLS certificates installed

### Monitoring Active
- [ ] APM configured and collecting metrics
- [ ] Dashboards created for key metrics
- [ ] Alerts configured and tested
- [ ] Logging aggregation working

### Security Configured
- [ ] Secrets management in place
- [ ] Network security implemented
- [ ] Access controls configured
- [ ] Security scanning in pipeline

### Documentation Complete
- [ ] Deployment runbook documented
- [ ] Infrastructure documentation complete
- [ ] Disaster recovery plan documented
- [ ] On-call procedures established

## Estimated Timeline

**Small Project:** 1-2 weeks
**Medium Project:** 2-3 weeks
**Large Project:** 3-4 weeks

## Common Pitfalls to Avoid

1. **No rollback plan:** Always have a way to revert deployments
2. **Deploying on Friday:** Avoid weekend incident response
3. **Not testing on staging first:** Staging should mirror production
4. **Ignoring monitoring:** Can't fix what you can't see
5. **Manual deployment steps:** Automate everything
6. **Weak secrets management:** Never hardcode secrets
7. **No backup testing:** Untested backups are useless

## Next Phase

Once Phase 4 is complete and validated, proceed to:

**[Phase 5: Monitoring and Maintenance](phase-5-monitoring-maintenance.md)**

Continuous monitoring, optimization, and maintenance of the production system.

---

**Related Documents:**
- [DevOps Agent Command](.claude/commands/devops.md)
- [Phase 3: Testing and QA](phase-3-testing-qa.md)
- [Phase 5: Monitoring and Maintenance](phase-5-monitoring-maintenance.md)
- [Multimodal Blueprint](.claude/MULTIMODAL_BLUEPRINT.md)
