# ADR-003: Dual Data Model Strategy (Internal + Raken Integration)

Date: 2025-10-24

## Status
**NEEDS REVIEW** - High Complexity, Requires Decision

## Context

ASR Ops Dashboard integrates with Raken API to access construction project data. Raken is a third-party construction management platform that ASR uses for:
- Daily reports and timecards
- Project management
- Team member and worker management
- Equipment tracking
- Material tracking
- Safety observations

The application currently maintains **dual data models**:

### Parallel Data Structures

```
Internal Tables          Raken API Tables/Endpoints
---------------          ---------------------------
projects                 raken_projects
team_members            raken_users
workers                 raken_users
time_entries            raken_time_cards, raken_work_logs
materials               /api/raken/live/materials
safety_observations     /api/raken/live/observations
equipment               raken_equipment
```

### Current Synchronization Approach

**Scheduled Jobs (APScheduler):**
- Daily sync at midnight: Fetch all Raken data
- Hourly token refresh: Maintain API authentication
- Background processing: Store fetched data in local tables

**Real-time API Calls:**
- Some endpoints fetch directly from Raken API
- Others query local cached tables
- Inconsistent approach across features

### Problems Identified

1. **Data Duplication:** Same data stored in 2+ places
2. **Sync Complexity:** 24-hour sync means stale data
3. **Eventual Consistency:** Users see different data depending on endpoint
4. **Route Migrations:** Ongoing consolidation efforts (noted in App.js)
5. **Storage Overhead:** Database bloat from duplicate records
6. **Maintenance Burden:** Changes require updating multiple tables
7. **Data Conflicts:** What happens when local and Raken data diverge?

## Decision

We need to choose one of three strategies:

## Option A: Raken as Source of Truth, Internal as Cache (RECOMMENDED)

### Strategy

**Raken API = Primary Data Source**
**Internal Tables = Cache Layer + Extensions**

### Implementation

```python
# Data Flow:
User Request → Check Cache → If Expired → Fetch from Raken → Update Cache → Return

# Tables Kept:
- raken_projects (cached, refreshed on access if >1 hour old)
- raken_users (cached, refreshed on access if >1 hour old)
- raken_time_cards (cached, refreshed daily)
- raken_equipment (cached, refreshed on access if >4 hours old)

# Tables Removed:
- projects (merged into raken_projects)
- team_members (merged into raken_users with raken_uuid link)
- workers (merged into raken_users)

# Internal-Only Tables (No Raken equivalent):
- users (authentication, local accounts)
- wage_reports (ASR-specific payroll data)
- wc_processing_jobs (workers comp processing)
- receipts (local file uploads)
- supplier_intelligence (ASR analytics)
- project_dailies (ASR-specific daily reports)
```

### Caching Strategy

**Time-To-Live (TTL) by Entity:**
- Projects: 1 hour (rarely change)
- Users/Workers: 1 hour (rarely change)
- Time Cards: 5 minutes (frequently updated)
- Equipment: 4 hours (infrequent changes)
- Materials: 1 hour (moderate changes)
- Daily Reports: 30 minutes (active during day)

**Cache Invalidation:**
- Automatic: TTL expiration
- Manual: Admin "Refresh Data" button per entity
- Webhooks: If Raken provides webhook support (future)

### Data Extensions

Local tables can extend Raken data with ASR-specific fields:

```sql
-- Example: Extend Raken projects with internal data
CREATE TABLE project_extensions (
    raken_project_uuid VARCHAR PRIMARY KEY REFERENCES raken_projects(uuid),
    internal_notes TEXT,
    asr_budget_override FLOAT,
    custom_fields JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Pros
- Single source of truth (Raken)
- Always have access to latest Raken data
- Reduced storage requirements
- Clear data ownership
- Simpler sync logic (cache refresh vs full sync)
- Can work offline with cached data
- Clear upgrade path if Raken adds features

### Cons
- Dependent on Raken API availability
- API rate limits may restrict usage
- Slower initial response (cache miss)
- Cannot modify Raken-owned data locally
- Requires internet connectivity

---

## Option B: Internal as Source of Truth, Raken as External System

### Strategy

**Internal DB = Primary Data Source**
**Raken = Read-Only Import + Reference**

### Implementation

```python
# Data Flow:
User Request → Internal DB → Return
Scheduled Job → Fetch from Raken → Import/Merge into Internal DB

# Primary Tables:
- projects (internal IDs, synced FROM Raken)
- team_members (internal IDs, linked to raken_uuid)
- time_entries (internal format, imported from Raken)

# Reference Tables:
- raken_import_log (track what's been imported)
- raken_mapping (internal_id ↔ raken_uuid)
```

### Pros
- Full control over data
- Can modify and extend freely
- Works offline completely
- No API rate limit concerns
- Faster query performance
- Can outlive Raken integration

### Cons
- Complex bidirectional sync if writing back to Raken
- Data divergence over time
- Large storage requirements
- Must handle Raken schema changes
- Duplicate data maintenance
- Risk of data inconsistency

---

## Option C: Bounded Contexts with Clear Ownership

### Strategy

**Partition data by domain ownership**

### Implementation

```
Raken-Owned Domains (read-only from API):
- Time tracking (timecards, work logs)
- Daily reports
- Equipment tracking

Internal-Owned Domains (local only):
- User authentication
- Payroll processing
- Workers compensation
- Supplier intelligence
- Receipt management

Hybrid Domains (composite from both):
- Projects (Raken core + internal extensions)
- Team Members (Raken profile + internal permissions)
```

### Pros
- Clear boundaries
- Avoids duplication in pure domains
- Flexibility for hybrid cases
- Each domain can evolve independently

### Cons
- Most complex to implement
- Requires careful API design
- UI complexity (showing merged data)
- Unclear for future features (which domain?)

---

## Recommended Decision: Option A (Raken as Source of Truth)

### Rationale

1. **Raken is the operational system** - Teams use Raken daily for timecards, daily reports
2. **ASR Ops is an analytics/operations dashboard** - Consuming Raken data, not replacing it
3. **Simplicity** - Cache pattern is well-understood and maintainable
4. **Scalability** - Reduces database size and maintenance
5. **Data freshness** - Users get real-time data with smart caching

### Migration Plan

**Phase 1: Implement Caching Layer (Week 1-2)**
```python
# Backend/services/cache_service.py
class CacheService:
    def get_projects(self, force_refresh=False):
        if force_refresh or cache_expired('projects'):
            data = raken_api.fetch_projects()
            cache_store('projects', data, ttl=3600)
        return cache_retrieve('projects')
```

**Phase 2: Route Consolidation (Week 2-3)**
- Complete pending migrations in App.js
- Redirect all project routes to unified endpoints
- Remove duplicate API endpoints
- Update frontend to use consolidated routes

**Phase 3: Table Merging (Week 3-4)**
```sql
-- Merge team_members → raken_users
-- Migration script:
-- 1. Add internal_user_id to raken_users
-- 2. Copy local-only data (permissions, roles) to new tables
-- 3. Update foreign keys
-- 4. Drop team_members table

-- Merge projects → raken_projects
-- Similar migration process
```

**Phase 4: Sync Job Refactoring (Week 4)**
- Convert from "full sync" to "cache refresh"
- Implement smart invalidation
- Add manual refresh endpoints
- Remove obsolete sync logic

**Phase 5: Testing & Validation (Week 5)**
- Verify data consistency
- Test cache expiration
- Load testing for API rate limits
- User acceptance testing

### Implementation Details

**Cache Storage Options:**
1. **Redis** (recommended for production)
   - Fast in-memory cache
   - Built-in TTL support
   - Distributed caching

2. **Database table** (acceptable for MVP)
   ```sql
   CREATE TABLE api_cache (
       cache_key VARCHAR PRIMARY KEY,
       cache_value JSONB,
       expires_at TIMESTAMP,
       created_at TIMESTAMP
   );
   ```

**API Endpoint Strategy:**
```python
# Unified endpoint pattern
GET /api/projects/          # Cached Raken projects + local extensions
GET /api/projects/{id}      # Single project (cache or real-time)
GET /api/projects/refresh   # Force cache refresh (admin only)

# Remove deprecated endpoints
# DELETE /api/raken/projects  (redirect to /api/projects)
```

**Frontend Route Consolidation:**
```javascript
// App.js - Complete migrations
<Route path="projects" element={<Projects />} />
<Route path="raken/projects" element={<Navigate to="/projects" />} />

<Route path="team-members" element={<TeamMembers />} />
<Route path="workers" element={<Navigate to="/team-members" />} />
<Route path="raken/members" element={<Navigate to="/team-members" />} />
```

## Consequences

### Positive Consequences

**Data Consistency:**
- Single source of truth eliminates conflicts
- Users always see consistent data
- No divergence between local and Raken

**Reduced Complexity:**
- Simplified sync logic (cache vs full replication)
- Fewer tables to maintain
- Clearer data ownership
- Easier debugging (single source)

**Performance:**
- Faster queries with caching
- Reduced database size
- Lower storage costs
- Smarter data fetching

**Maintainability:**
- Clearer architecture
- Fewer moving parts
- Easier onboarding for new developers
- Simpler testing

### Negative Consequences

**Raken Dependency:**
- Application depends on Raken API availability
- API rate limits may constrain usage
- Schema changes in Raken affect us
- Cannot operate if Raken is down (unless cache valid)

**Initial Performance:**
- Cache misses cause API roundtrip delay
- First load after expiration is slower
- Need to warm cache for critical paths

**Migration Effort:**
- Significant refactoring required
- Risk of data loss if migration done incorrectly
- Downtime during table merges
- Need comprehensive testing

### Risks and Mitigation

**Risk: Raken API downtime**
- **Mitigation:** Longer cache TTLs (configurable)
- **Mitigation:** Graceful degradation (show cached data with warning)
- **Mitigation:** Health check monitoring

**Risk: API rate limits**
- **Mitigation:** Implement request throttling
- **Mitigation:** Smart cache invalidation (don't fetch if not needed)
- **Mitigation:** Batch requests where possible
- **Mitigation:** Monitor API usage

**Risk: Data loss during migration**
- **Mitigation:** Full database backup before migration
- **Mitigation:** Test migration on staging environment
- **Mitigation:** Rollback plan with restore scripts
- **Mitigation:** Data validation checks post-migration

**Risk: Cache staleness**
- **Mitigation:** Configurable TTLs per entity type
- **Mitigation:** Manual refresh for critical operations
- **Mitigation:** Real-time refresh for time-sensitive data (timecards)
- **Mitigation:** UI indicators showing data freshness

## Alternatives Analysis Summary

| Criteria | Option A (Raken SOT) | Option B (Internal SOT) | Option C (Bounded) |
|----------|---------------------|------------------------|-------------------|
| Complexity | Medium | High | Very High |
| Data Consistency | High | Medium | Medium |
| Storage Requirements | Low | High | Medium |
| Raken Dependency | High | Low | Medium |
| Maintenance Burden | Low | High | High |
| Performance | Medium-High | High | Medium |
| Migration Effort | Medium | High | Very High |
| **RECOMMENDED** | **✅ YES** | ❌ No | ❌ No |

## Related Decisions

- ADR-002: Monolithic Architecture (establishes context)
- ADR-006: Database Abstraction Strategy (migration tooling)
- Future ADR: Webhook Integration (if Raken adds webhook support)

## Success Metrics

After implementation, measure:
- Cache hit rate (target: >90%)
- API request count (should decrease 70-80%)
- Response time improvement (target: <500ms for cached responses)
- Database size reduction (expect 30-40% reduction)
- User-reported data consistency issues (target: zero)

## Review Date

**Next Review:** 2025-11-24 (1 month post-implementation)
**Re-evaluate if:**
- Raken API availability drops below 99%
- Rate limits become constraining
- Cache strategy causes performance issues
- Team requirements change significantly

---

**Status:** AWAITING APPROVAL
**Owner:** Architecture Team + Database Team
**Stakeholders:** Development Team, Operations Team, Management
**Implementation Timeline:** 5 weeks
**Risk Level:** HIGH (significant refactoring)
