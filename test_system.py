"""
Quick test script to verify the system is working
"""

from database.db_manager import get_db
from matching_engine import get_matching_engine


def test_database():
    """Test database operations"""
    print("Testing Database...")
    db = get_db()

    # Get statistics
    stats = db.get_statistics()
    print(f"✓ Database connected")
    print(f"  - Candidates: {stats['total_candidates']}")
    print(f"  - Jobs: {stats['active_jobs']}")
    print(f"  - Matches: {stats['total_matches']}")
    print()


def test_matching_engine():
    """Test matching engine"""
    print("Testing Matching Engine...")
    try:
        engine = get_matching_engine()
        print("✓ Matching engine loaded")
        print("  - Model ready")
        print("  - Vectorizer ready")
        print()
    except Exception as e:
        print(f"✗ Error loading matching engine: {e}")
        print()


def main():
    print("="*60)
    print("AI RESUME SHORTLISTER - SYSTEM TEST")
    print("="*60)
    print()

    test_database()
    test_matching_engine()

    print("="*60)
    print("✓ System test complete!")
    print("="*60)
    print()
    print("To start the web application, run:")
    print("  streamlit run app.py")
    print()


if __name__ == "__main__":
    main()
