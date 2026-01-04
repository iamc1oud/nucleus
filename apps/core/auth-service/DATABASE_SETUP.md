# Database Setup Guide

This guide explains how to set up and manage the database for the auth service.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or
   uv sync
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Run migrations**:
   ```bash
   # Using Alembic directly
   alembic upgrade head
   
   # Or using the management script
   python manage.py upgrade
   ```

4. **Start the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## Database Management

### Using the Management Script

The `manage.py` script provides convenient commands for database operations:

```bash
# Check migration status
python manage.py status

# Create new migration
python manage.py migrate "Add new field to users"

# Create manual migration
python manage.py migrate "Custom data migration" --manual

# Upgrade database
python manage.py upgrade

# Downgrade database
python manage.py downgrade

# Show migration history
python manage.py history

# Database maintenance
python manage.py cleanup  # Remove expired auth codes
python manage.py stats    # Show database statistics
```

### Using Alembic Directly

```bash
# Check current status
alembic current
alembic history

# Create migrations
alembic revision --autogenerate -m "Description"
alembic revision -m "Manual migration"

# Apply migrations
alembic upgrade head
alembic upgrade +1
alembic upgrade <revision_id>

# Rollback migrations
alembic downgrade -1
alembic downgrade <revision_id>
alembic downgrade base
```

## Environment Configuration

### Database Settings

Configure these environment variables in your `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=nucleus
DB_PASSWORD=nucleus
DB_NAME=nucleus
```

### Alembic Configuration

The `alembic.ini` file is configured to:
- Use PostgreSQL with psycopg2
- Read database URL from environment via `alembic/env.py`
- Auto-generate migrations from SQLModel changes
- Include proper logging

## Development Workflow

### Adding New Models

1. Create the SQLModel class:
   ```python
   # app/models/new_model.py
   from sqlmodel import SQLModel, Field
   
   class NewModel(SQLModel, table=True):
       id: int = Field(primary_key=True)
       name: str
   ```

2. Import in `app/models/__init__.py`:
   ```python
   from .new_model import NewModel
   __all__ = ["AuthorizationCode", "NewModel"]
   ```

3. Import in `alembic/env.py`:
   ```python
   from app.models.new_model import NewModel
   ```

4. Generate and apply migration:
   ```bash
   python manage.py migrate "Add NewModel table"
   python manage.py upgrade
   ```

### Modifying Existing Models

1. Update the SQLModel class
2. Generate migration:
   ```bash
   python manage.py migrate "Update AuthorizationCode model"
   ```
3. Review the generated migration file
4. Apply migration:
   ```bash
   python manage.py upgrade
   ```

## Production Considerations

### Migration Safety

- **Always backup** your database before running migrations in production
- **Test migrations** on a copy of production data first
- **Review auto-generated migrations** before applying
- **Use transactions** for data migrations

### Deployment Strategy

1. **Blue-Green Deployment**:
   - Deploy new version alongside old
   - Run migrations on new environment
   - Switch traffic after verification

2. **Rolling Deployment**:
   - Ensure migrations are backward compatible
   - Deploy application first, then run migrations
   - Or run migrations first if they're additive only

### Monitoring

Monitor migration status in production:

```bash
# Check if database is up to date
python manage.py status

# Get database statistics
python manage.py stats
```

## Troubleshooting

### Common Issues

1. **Migration conflicts**:
   ```bash
   alembic heads  # Show multiple heads
   alembic merge -m "Merge branches" <head1> <head2>
   ```

2. **Schema drift**:
   ```bash
   alembic check  # Check for differences
   python manage.py migrate "Fix schema drift"
   ```

3. **Failed migration**:
   ```bash
   alembic current  # Check current state
   # Fix the migration file and retry
   python manage.py upgrade
   ```

### Recovery

If you need to reset migrations (development only):

```bash
# Drop all tables
alembic downgrade base

# Recreate from scratch
python manage.py upgrade
```

## Files Overview

- `alembic.ini` - Alembic configuration
- `alembic/env.py` - Migration environment setup
- `alembic/versions/` - Migration files
- `app/database.py` - Database connection setup
- `app/migrations.py` - Migration utilities
- `app/db_utils.py` - Database utility functions
- `manage.py` - Management script for common operations
- `ALEMBIC_GUIDE.md` - Comprehensive Alembic usage guide