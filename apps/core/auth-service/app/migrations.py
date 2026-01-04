"""
Migration utilities for automatic database schema management
"""
import os
from pathlib import Path
from alembic.config import Config
from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine
from .database import get_database_url

def get_alembic_config() -> Config:
    """Get Alembic configuration"""
    # Get the path to alembic.ini (should be in the project root)
    alembic_ini_path = Path(__file__).parent.parent / "alembic.ini"
    
    if not alembic_ini_path.exists():
        raise FileNotFoundError(f"alembic.ini not found at {alembic_ini_path}")
    
    return Config(str(alembic_ini_path))

def check_migration_status() -> dict:
    """Check current migration status"""
    config = get_alembic_config()
    script = ScriptDirectory.from_config(config)
    
    # Get database connection
    engine = create_engine(get_database_url())
    
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        current_rev = context.get_current_revision()
        head_rev = script.get_current_head()
        
        return {
            "current_revision": current_rev,
            "head_revision": head_rev,
            "is_up_to_date": current_rev == head_rev,
            "needs_upgrade": current_rev != head_rev
        }

def run_migrations():
    """Run migrations to head"""
    try:
        config = get_alembic_config()
        command.upgrade(config, "head")
        return {"success": True, "message": "Migrations completed successfully"}
    except Exception as e:
        return {"success": False, "message": f"Migration failed: {str(e)}"}

def auto_migrate_on_startup():
    """
    Automatically run migrations on startup.
    Use this carefully - only in development or with proper safeguards.
    """
    status = check_migration_status()
    
    if status["needs_upgrade"]:
        print(f"Database needs migration from {status['current_revision']} to {status['head_revision']}")
        result = run_migrations()
        
        if result["success"]:
            print("✅ Database migrations completed successfully")
        else:
            print(f"❌ Migration failed: {result['message']}")
            raise Exception(f"Migration failed: {result['message']}")
    else:
        print("✅ Database is up to date")

# Optional: Add this to your FastAPI lifespan if you want automatic migrations
# WARNING: Only use in development or with proper safeguards in production