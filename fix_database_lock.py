"""
Fix database lock issue by enabling WAL mode and checking connections
"""

import sqlite3
import os

db_path = "database/resume_shortlister.db"

print("🔧 Fixing database lock issue...")
print(f"Database: {db_path}")
print()

# Check if database exists
if not os.path.exists(db_path):
    print(f"❌ Database not found at {db_path}")
    exit(1)

try:
    # Connect with proper settings
    print("1. Connecting to database...")
    conn = sqlite3.connect(db_path, timeout=30.0)

    # Enable WAL mode for better concurrency
    print("2. Enabling WAL (Write-Ahead Logging) mode...")
    conn.execute('PRAGMA journal_mode=WAL')
    result = conn.execute('PRAGMA journal_mode').fetchone()
    print(f"   Journal mode: {result[0]}")

    # Set busy timeout
    print("3. Setting busy timeout to 30 seconds...")
    conn.execute('PRAGMA busy_timeout=30000')

    # Check database integrity
    print("4. Checking database integrity...")
    integrity = conn.execute('PRAGMA integrity_check').fetchone()
    print(f"   Integrity: {integrity[0]}")

    # Get table counts
    print("5. Checking table data...")
    tables = ['candidates', 'job_posts', 'match_results']
    for table in tables:
        try:
            count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
            print(f"   {table}: {count} records")
        except Exception as e:
            print(f"   {table}: Error - {e}")

    conn.close()
    print()
    print("✅ Database is ready!")
    print()
    print("📝 Tips to avoid database locks:")
    print("   1. Close any sqlite3 terminal sessions")
    print("   2. Stop any running Streamlit apps before starting new one")
    print("   3. Use 'Ctrl+C' to stop Streamlit properly")
    print("   4. The updated db_manager.py now handles locks better with:")
    print("      - 30 second timeout")
    print("      - WAL mode for concurrent access")
    print("      - Proper connection handling")

except sqlite3.OperationalError as e:
    print(f"❌ Database error: {e}")
    print()
    print("💡 To fix:")
    print("   1. Stop all Streamlit apps (Ctrl+C)")
    print("   2. Close any sqlite3 terminal sessions")
    print("   3. Run this script again")
    exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    exit(1)
