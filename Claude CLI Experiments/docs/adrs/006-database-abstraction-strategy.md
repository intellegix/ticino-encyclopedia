# ADR-006: Database Abstraction Strategy

Date: 2025-10-24

## Status
Accepted

## Context

The ASR Ops Dashboard requires a flexible database strategy that supports:
- **Development:** Fast local setup without external dependencies
- **Production:** Scalable, reliable database for real workloads
- **Testing:** Isolated test environments
- **Data Migration:** Schema evolution over time

The application has significant data requirements:
- **41 database models** (tables)
- **Complex relationships:** Foreign keys, one-to-many, many-to-many
- **Large datasets:** Timecards, daily reports, workers comp data
- **Financial data:** Requires ACID compliance
- **File references:** Receipt uploads, document storage

Current challenges:
- Need seamless transition between development and production databases
- Schema changes require migration management
- Different developers may use different database types
- Testing requires fast, isolated database setup

## Decision

We will implement **database abstraction with dual-database support** using SQLAlchemy ORM:

### Database Strategy

**Development Environment:**
- **Database:** SQLite
- **Connection:** `sqlite:///./asr_ops.db` (local file)
- **Benefits:** Zero setup, fast, portable, version control friendly

**Production Environment:**
- **Database:** PostgreSQL
- **Connection:** From `DATABASE_URL` environment variable
- **Benefits:** Production-grade, ACID, concurrent access, JSON support

**Testing Environment:**
- **Database:** SQLite in-memory
- **Connection:** `sqlite:///:memory:`
- **Benefits:** Fast test execution, isolated tests, no cleanup needed

### Implementation

**database.py:**
```python
import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment or default to SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./asr_ops.db"
    print("WARNING: DATABASE_URL not set - using SQLite for development")
else:
    print(f"INFO: Using database: {SQLALCHEMY_DATABASE_URL.split('@')[-1]}")

# Configure engine with appropriate settings
engine_kwargs = {"pool_pre_ping": True}

if "sqlite" in SQLALCHEMY_DATABASE_URL.lower():
    # SQLite-specific configuration
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # PostgreSQL configuration
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20
    engine_kwargs["pool_recycle"] = 3600

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)

# SQLite optimizations
if "sqlite" in SQLALCHEMY_DATABASE_URL.lower():
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
        cursor.execute("PRAGMA foreign_keys=ON")   # Enforce FK constraints
        cursor.execute("PRAGMA synchronous=NORMAL") # Performance
        cursor.execute("PRAGMA cache_size=10000")   # Memory cache
        cursor.execute("PRAGMA temp_store=MEMORY")  # Temp tables in memory
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### SQLAlchemy ORM Usage

**Model Definition (Cross-Database Compatible):**
```python
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    job_number = Column(String, unique=True, index=True)
    start_date = Column(Date)
    budget = Column(Float)
    status = Column(String)

    # Relationship
    time_entries = relationship("TimeEntry", back_populates="project")
```

**Avoiding Database-Specific Features:**
```python
# ❌ PostgreSQL-specific (breaks SQLite)
from sqlalchemy.dialects.postgresql import JSONB
data = Column(JSONB)

# ✅ Cross-compatible
from sqlalchemy import JSON
data = Column(JSON)  # Works on both SQLite and PostgreSQL

# ❌ PostgreSQL array (breaks SQLite)
from sqlalchemy.dialects.postgresql import ARRAY
tags = Column(ARRAY(String))

# ✅ Cross-compatible
tags = Column(String)  # Store as comma-separated or JSON
```

### Migration Strategy with Alembic

**Setup:**
```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Configure alembic.ini to use DATABASE_URL
sqlalchemy.url = ${DATABASE_URL}
```

**alembic/env.py:**
```python
import os
from alembic import context
from database import Base
import models  # Import all models

# Get database URL from environment
config.set_main_option(
    'sqlalchemy.url',
    os.getenv('DATABASE_URL', 'sqlite:///./asr_ops.db')
)

target_metadata = Base.metadata
```

**Creating Migrations:**
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add workers comp tables"

# Review generated migration file
# Edit alembic/versions/xxx_add_workers_comp_tables.py

# Apply migration
alembic upgrade head
```

**Migration Example:**
```python
# alembic/versions/001_add_raken_uuid.py
def upgrade():
    op.add_column('team_members',
        sa.Column('raken_uuid', sa.String(), nullable=True))
    op.create_index('ix_team_members_raken_uuid',
        'team_members', ['raken_uuid'])

def downgrade():
    op.drop_index('ix_team_members_raken_uuid', 'team_members')
    op.drop_column('team_members', 'raken_uuid')
```

**Migration Best Practices:**
1. Always include both `upgrade()` and `downgrade()`
2. Test migrations on SQLite before production
3. Backup database before running migrations
4. Use transactions for data migrations
5. Never edit applied migrations (create new ones)

### Environment Configuration

**.env (Development):**
```bash
# Development - SQLite (default if not set)
# DATABASE_URL=sqlite:///./asr_ops.db

# Or use PostgreSQL locally
# DATABASE_URL=postgresql://user:password@localhost/asr_ops_dev
```

**.env (Production):**
```bash
# Production - PostgreSQL
DATABASE_URL=postgresql://user:password@prod-server.example.com/asr_ops_prod
```

**Docker Compose (Development):**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: asr_ops_dev
      POSTGRES_USER: asr_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./Backend
    environment:
      DATABASE_URL: postgresql://asr_user:dev_password@postgres/asr_ops_dev
    depends_on:
      - postgres
```

### Testing Strategy

**Test Database Setup:**
```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base

@pytest.fixture(scope="function")
def test_db():
    # Create in-memory SQLite database for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)

# Usage in tests
def test_create_project(test_db):
    project = Project(name="Test Project", job_number="WO-123")
    test_db.add(project)
    test_db.commit()

    assert project.id is not None
```

### Database Health Monitoring

```python
def check_database_health() -> dict:
    """Health check for database connection"""
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "type": "PostgreSQL" if "postgresql" in str(engine.url) else "SQLite"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
```

## Consequences

### Positive Consequences

**Development Velocity:**
- Zero database setup for new developers
- Fast local development with SQLite
- No Docker required for simple development
- Easy to reset database (delete .db file)

**Production Readiness:**
- PostgreSQL provides production-grade reliability
- ACID compliance for financial data
- Concurrent access for multiple users
- JSON support for flexible schemas

**Testing:**
- In-memory SQLite for fast test execution
- Isolated test databases
- No cleanup required between tests
- Parallel test execution possible

**Portability:**
- Same codebase works on both databases
- Easy environment transitions
- Flexible deployment options
- Can switch databases without code changes

**Migration Management:**
- Alembic tracks schema versions
- Reversible migrations
- Auto-generation from model changes
- Version control for schema evolution

### Negative Consequences

**Feature Limitations:**
- Must avoid database-specific features
- Cannot use PostgreSQL-specific optimizations in development
- Some features work differently (SQLite vs PostgreSQL)
- JSON support varies between databases

**Testing Gaps:**
- SQLite tests may not catch PostgreSQL-specific issues
- Need production-like staging environment
- Performance characteristics differ
- Transaction behavior may vary

**Complexity:**
- Need to understand both database systems
- Debugging issues may be database-specific
- Configuration management across environments
- Migration testing required for both databases

### Risks and Mitigation

**Risk: SQLite → PostgreSQL differences cause production bugs**
- **Mitigation:** Staging environment with PostgreSQL
- **Mitigation:** Integration tests on PostgreSQL before deployment
- **Mitigation:** Avoid database-specific SQL
- **Mitigation:** Use SQLAlchemy ORM exclusively

**Risk: Migrations break production database**
- **Mitigation:** Always backup before migration
- **Mitigation:** Test migrations on staging first
- **Mitigation:** Implement rollback procedures
- **Mitigation:** Monitor post-migration health

**Risk: SQLite performance inadequate for development**
- **Mitigation:** Optional PostgreSQL for development (Docker Compose)
- **Mitigation:** SQLite optimizations (WAL mode, pragmas)
- **Mitigation:** Seed data scripts for realistic testing

**Risk: Connection pool exhaustion**
- **Mitigation:** Proper connection pooling configuration
- **Mitigation:** Monitor database connections
- **Mitigation:** Implement connection limits
- **Mitigation:** Use `pool_pre_ping` to detect stale connections

## Alternatives Considered

### Alternative 1: PostgreSQL Only

**Pros:**
- Production parity in development
- No database compatibility concerns
- Full PostgreSQL feature set available
- Consistent behavior across environments

**Cons:**
- Requires PostgreSQL installation for all developers
- Slower setup for new developers
- Docker dependency for development
- Heavier resource usage locally
- More complex local debugging

**Why not chosen:** Higher barrier to entry for development, unnecessary complexity for simple local work.

### Alternative 2: MongoDB (NoSQL)

**Pros:**
- Flexible schema
- Good for document-oriented data
- Easy horizontal scaling
- JSON-native storage

**Cons:**
- No ACID transactions (older versions)
- Financial data needs ACID compliance
- Different querying paradigm
- Team unfamiliar with NoSQL
- Complex relationships harder to model

**Why not chosen:** Relational model better fits our domain (projects, timecards, users with relationships). Financial data requires ACID guarantees.

### Alternative 3: MySQL/MariaDB

**Pros:**
- Popular, well-documented
- Good performance
- Wide hosting support
- Similar to PostgreSQL

**Cons:**
- PostgreSQL has better JSON support
- Less strict with data types (can hide bugs)
- PostgreSQL preferred in Python ecosystem
- No significant advantages over PostgreSQL

**Why not chosen:** PostgreSQL is more feature-rich and better integrated with Python/SQLAlchemy ecosystem.

### Alternative 4: No Abstraction (Direct SQL)

**Pros:**
- Full database feature access
- Maximum performance
- No ORM overhead
- Direct control

**Cons:**
- SQL injection risk
- Database-specific code
- No automatic migrations
- More boilerplate
- Harder to test
- Manual schema management

**Why not chosen:** SQLAlchemy provides safety, productivity, and maintainability benefits that outweigh raw performance gains.

## Implementation Checklist

**Completed:**
- [x] SQLAlchemy ORM setup
- [x] Dual database support (SQLite/PostgreSQL)
- [x] Environment-based configuration
- [x] Connection pooling
- [x] SQLite optimizations (WAL mode)
- [x] Health check endpoint
- [x] Database session management

**TODO:**
- [ ] Alembic migration setup
- [ ] Initial migration for existing schema
- [ ] Migration documentation
- [ ] Staging environment with PostgreSQL
- [ ] Backup/restore procedures
- [ ] Database monitoring
- [ ] Query performance optimization
- [ ] Index analysis and optimization

## Migration Setup Guide

**Step 1: Install Alembic**
```bash
pip install alembic
echo "alembic==1.13.0" >> requirements.txt
```

**Step 2: Initialize Alembic**
```bash
cd Backend
alembic init alembic
```

**Step 3: Configure Alembic**
Edit `alembic.ini`:
```ini
[alembic]
# Remove hardcoded sqlalchemy.url
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

Edit `alembic/env.py`:
```python
import os
import sys
from pathlib import Path

# Add Backend directory to path
sys.path.append(str(Path(__file__).parents[1]))

from database import Base
import models  # Import ALL models

# Use environment variable
config.set_main_option(
    'sqlalchemy.url',
    os.getenv('DATABASE_URL', 'sqlite:///./asr_ops.db')
)

target_metadata = Base.metadata
```

**Step 4: Create Initial Migration**
```bash
# Generate migration from current models
alembic revision --autogenerate -m "Initial schema"

# Review generated file in alembic/versions/
# Edit if needed

# Apply migration
alembic upgrade head
```

**Step 5: Future Schema Changes**
```bash
# 1. Modify models.py
# 2. Generate migration
alembic revision --autogenerate -m "Add new column"

# 3. Review and test migration
# 4. Apply to development
alembic upgrade head

# 5. Apply to production (after testing)
DATABASE_URL=postgresql://... alembic upgrade head
```

## Related Decisions

- ADR-002: Monolithic Architecture (establishes single database)
- ADR-003: Dual Data Model Strategy (affects schema design)
- Future ADR: Database Sharding Strategy (if scale requires)

## References

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This)
- [SQLite Optimization](https://www.sqlite.org/pragma.html)

---

**Next Review Date:** 2026-04-24 (6 months)
**Owner:** Backend Team + DevOps Team
**Stakeholders:** Development Team, Operations Team
