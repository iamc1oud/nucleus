#!/usr/bin/env python3
"""
Simple migration script for SQLModel tables
"""
from app.database import init_db
from app.models import AuthorizationCode

def main():
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!")

if __name__ == "__main__":
    main()