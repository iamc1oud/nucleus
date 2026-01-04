#!/usr/bin/env python3
"""
Database management script for common operations
"""
import sys
import argparse
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from app.migrations import check_migration_status, run_migrations
from app.db_utils import cleanup_expired_codes, get_active_codes_count
from alembic.config import Config
from alembic import command

def create_migration(message: str, autogenerate: bool = True):
    """Create a new migration"""
    config = Config("alembic.ini")
    if autogenerate:
        command.revision(config, message=message, autogenerate=True)
    else:
        command.revision(config, message=message)
    print(f"✅ Created migration: {message}")

def upgrade_database():
    """Upgrade database to latest migration"""
    result = run_migrations()
    if result["success"]:
        print("✅ Database upgraded successfully")
    else:
        print(f"❌ Upgrade failed: {result['message']}")
        sys.exit(1)

def downgrade_database(revision: str = "-1"):
    """Downgrade database"""
    config = Config("alembic.ini")
    command.downgrade(config, revision)
    print(f"✅ Database downgraded to {revision}")

def migration_status():
    """Show migration status"""
    status = check_migration_status()
    print(f"Current revision: {status['current_revision']}")
    print(f"Head revision: {status['head_revision']}")
    print(f"Up to date: {'✅' if status['is_up_to_date'] else '❌'}")

def migration_history():
    """Show migration history"""
    config = Config("alembic.ini")
    command.history(config, verbose=True)

def cleanup_database():
    """Clean up expired authorization codes"""
    count = cleanup_expired_codes()
    print(f"✅ Cleaned up {count} expired authorization codes")

def database_stats():
    """Show database statistics"""
    active_codes = get_active_codes_count()
    print(f"Active authorization codes: {active_codes}")

def main():
    parser = argparse.ArgumentParser(description="Database management script")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Migration commands
    migrate_parser = subparsers.add_parser("migrate", help="Create new migration")
    migrate_parser.add_argument("message", help="Migration message")
    migrate_parser.add_argument("--manual", action="store_true", help="Create empty migration")

    subparsers.add_parser("upgrade", help="Upgrade database to latest migration")
    
    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade database")
    downgrade_parser.add_argument("--revision", default="-1", help="Revision to downgrade to")

    subparsers.add_parser("status", help="Show migration status")
    subparsers.add_parser("history", help="Show migration history")

    # Database maintenance commands
    subparsers.add_parser("cleanup", help="Clean up expired authorization codes")
    subparsers.add_parser("stats", help="Show database statistics")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "migrate":
            create_migration(args.message, autogenerate=not args.manual)
        elif args.command == "upgrade":
            upgrade_database()
        elif args.command == "downgrade":
            downgrade_database(args.revision)
        elif args.command == "status":
            migration_status()
        elif args.command == "history":
            migration_history()
        elif args.command == "cleanup":
            cleanup_database()
        elif args.command == "stats":
            database_stats()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()