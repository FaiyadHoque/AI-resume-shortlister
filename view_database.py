"""
View Database Contents - Simple CLI tool
"""

from database.db_manager import get_db
import pandas as pd


def view_candidates():
    """View all candidates"""
    db = get_db()
    candidates = db.get_all_candidates()
    
    if candidates:
        df = pd.DataFrame(candidates)
        # Select key columns
        display_cols = ['id', 'name', 'email', 'phone', 'experience_years', 'created_at']
        available_cols = [col for col in display_cols if col in df.columns]
        print("\n" + "="*80)
        print("CANDIDATES")
        print("="*80)
        print(df[available_cols].to_string(index=False))
        print(f"\nTotal: {len(candidates)} candidates")
    else:
        print("\nNo candidates in database.")


def view_jobs():
    """View all job posts"""
    db = get_db()
    jobs = db.get_all_job_posts(status='all')
    
    if jobs:
        df = pd.DataFrame(jobs)
        # Select key columns
        display_cols = ['id', 'title', 'company', 'location', 'status', 'required_experience_years', 'created_at']
        available_cols = [col for col in display_cols if col in df.columns]
        print("\n" + "="*80)
        print("JOB POSTS")
        print("="*80)
        print(df[available_cols].to_string(index=False))
        print(f"\nTotal: {len(jobs)} jobs")
    else:
        print("\nNo job posts in database.")


def view_matches():
    """View all match results"""
    db = get_db()
    matches = db.get_top_matches(limit=100)
    
    if matches:
        df = pd.DataFrame(matches)
        # Convert score to percentage
        df['match_score'] = (df['match_score'] * 100).round(2)
        
        print("\n" + "="*80)
        print("MATCH RESULTS")
        print("="*80)
        print(df.to_string(index=False))
        print(f"\nTotal: {len(matches)} matches")
    else:
        print("\nNo matches in database.")


def view_statistics():
    """View database statistics"""
    db = get_db()
    stats = db.get_statistics()
    
    print("\n" + "="*80)
    print("DATABASE STATISTICS")
    print("="*80)
    print(f"Total Candidates:     {stats['total_candidates']}")
    print(f"Active Job Posts:     {stats['active_jobs']}")
    print(f"Total Matches:        {stats['total_matches']}")
    print(f"Average Match Score:  {stats['average_match_score']*100:.2f}%")
    print("="*80)


def main():
    """Main menu"""
    print("\n" + "="*80)
    print("DATABASE VIEWER - AI Resume Shortlister")
    print("="*80)
    
    while True:
        print("\nOptions:")
        print("  1. View Statistics")
        print("  2. View Candidates")
        print("  3. View Job Posts")
        print("  4. View Matches")
        print("  5. View All")
        print("  0. Exit")
        
        choice = input("\nEnter choice (0-5): ").strip()
        
        if choice == '1':
            view_statistics()
        elif choice == '2':
            view_candidates()
        elif choice == '3':
            view_jobs()
        elif choice == '4':
            view_matches()
        elif choice == '5':
            view_statistics()
            view_candidates()
            view_jobs()
            view_matches()
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
