# Alembic Database Migration Guide

This guide covers all common Alembic use cases for managing database schema changes in your FastAPI SQLModel application.

## Prerequisites

- Alembic is configured and initialized
- Database connection is properly set up in `alembic.ini` and `alembic/env.py`
- All SQLModel models are imported in `alembic/env.py`

## Basic Commands

### 1. Check Current Migration Status

```bash
# Show current revision
alembic current

# Show migration history
alembic history

# Show migration history with details
alembic history --verbose
```

### 2. Create New Migrations

#### Auto-generate Migration from Model Changes
```bash
# Generate migration automatically by comparing models to database
alembic revision --autogenerate -m "Description of changes"

# Example: Adding a new field
alembic revision --autogenerate -m "Add email field to users table"
```

#### Create Empty Migration (Manual)
```bash
# Create empty migration file for manual changes
alembic revision -m "Custom migration description"
```

### 3. Apply Migrations

```bash
# Upgrade to latest migration
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Upgrade by relative steps
alembic upgrade +2  # Upgrade 2 steps forward
```

### 4. Rollback Migrations

```bash
# Downgrade to previous revision
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>

# Downgrade to base (remove all migrations)
alembic downgrade base
```

## Common Use Cases

### 1. Adding a New Model/Table

1. Create your SQLModel class:
```python
# app/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
```

2. Import the model in `app/models/__init__.py`:
```python
from .user import User
__all__ = ["AuthorizationCode", "User"]
```

3. Import in `alembic/env.py`:
```python
from app.models.user import User
```

4. Generate and apply migration:
```bash
alembic revision --autogenerate -m "Add user table"
alembic upgrade head
```

### 2. Adding Fields to Existing Table

1. Update your model:
```python
class AuthorizationCode(SQLModel, table=True):
    # ... existing fields ...
    ip_address: Optional[str] = None  # New field
```

2. Generate migration:
```bash
alembic revision --autogenerate -m "Add ip_address to authorization_codes"
```

3. Review the generated migration file and apply:
```bash
alembic upgrade head
```

### 3. Adding Indexes

1. Update model with index:
```python
class AuthorizationCode(SQLModel, table=True):
    # ... existing fields ...
    client_id: str = Field(index=True)  # Add index
```

2. Generate migration:
```bash
alembic revision --autogenerate -m "Add index on client_id"
alembic upgrade head
```

### 4. Renaming Columns

Alembic cannot auto-detect column renames. Create manual migration:

1. Create empty migration:
```bash
alembic revision -m "Rename user_id to account_id"
```

2. Edit the migration file:
```python
def upgrade() -> None:
    op.alter_column('authorization_codes', 'user_id', new_column_name='account_id')

def downgrade() -> None:
    op.alter_column('authorization_codes', 'account_id', new_column_name='user_id')
```

### 5. Adding Foreign Keys

1. Update models:
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str

class AuthorizationCode(SQLModel, table=True):
    # ... existing fields ...
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
```

2. Generate migration:
```bash
alembic revision --autogenerate -m "Add foreign key to user table"
alembic upgrade head
```

### 6. Data Migrations

For migrations that need to modify data:

1. Create empty migration:
```bash
alembic revision -m "Migrate old data format"
```

2. Edit migration with data operations:
```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

def upgrade() -> None:
    # Schema changes first
    op.add_column('authorization_codes', sa.Column('new_field', sa.String()))
    
    # Data migration
    auth_codes = table('authorization_codes',
        column('id', sa.Integer),
        column('old_field', sa.String()),
        column('new_field', sa.String())
    )
    
    connection = op.get_bind()
    connection.execute(
        auth_codes.update().values(new_field=auth_codes.c.old_field + '_migrated')
    )
    
    # Remove old column
    op.drop_column('authorization_codes', 'old_field')

def downgrade() -> None:
    # Reverse the operations
    op.add_column('authorization_codes', sa.Column('old_field', sa.String()))
    # ... reverse data migration ...
    op.drop_column('authorization_codes', 'new_field')
```

## Advanced Operations

### 1. Branching and Merging

When multiple developers create migrations:

```bash
# Create branch
alembic revision -m "Feature A changes" --branch-label=feature_a

# Merge branches
alembic merge -m "Merge feature branches" <rev1> <rev2>
```

### 2. Squashing Migrations

To combine multiple migrations into one:

1. Create new migration with all changes
2. Delete old migration files
3. Update revision history

### 3. Environment-Specific Migrations

Use revision labels for different environments:

```bash
# Create migration for specific environment
alembic revision -m "Production-only changes" --branch-label=production
```

## Troubleshooting

### 1. Migration Conflicts

If you get conflicts during merge:
```bash
# Show heads
alembic heads

# Merge conflicting heads
alembic merge -m "Resolve migration conflict" <head1> <head2>
```

### 2. Schema Drift

If database schema doesn't match migrations:
```bash
# Check differences
alembic check

# Generate migration to fix drift
alembic revision --autogenerate -m "Fix schema drift"
```

### 3. Rollback Failed Migration

If a migration fails during upgrade:
```bash
# Check current state
alembic current

# Force set revision (dangerous - use carefully)
alembic stamp <working_revision>

# Fix the migration and try again
alembic upgrade head
```

## Best Practices

1. **Always review auto-generated migrations** before applying
2. **Test migrations on a copy of production data**
3. **Keep migrations small and focused**
4. **Add meaningful descriptions to migrations**
5. **Never edit applied migrations** - create new ones instead
6. **Backup database before major migrations**
7. **Use transactions for data migrations**
8. **Test both upgrade and downgrade paths**

## Integration with Application

### Startup Migration Check

Add to your FastAPI startup:

```python
from alembic.config import Config
from alembic import command

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check if migrations are up to date
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield
```

### Environment Variables

Set database URL via environment:

```python
# In alembic/env.py
import os
from app.config.settings import Settings

settings = Settings()
database_url = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
config.set_main_option("sqlalchemy.url", database_url)
```

This guide covers the most common Alembic use cases. For more advanced scenarios, refer to the [official Alembic documentation](https://alembic.sqlalchemy.org/).