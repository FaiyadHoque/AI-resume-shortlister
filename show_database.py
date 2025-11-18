"""
Quick Database View - Display all database contents
"""

from database.db_manager import get_db
import pandas as pd


def main():
    """Display all database contents"""
    db = get_db()
    
    print("\n" + "="*100)
    print("DATABASE CONTENTS - AI Resume Shortlister")
    print("="*100)
    
    # Statistics
    stats = db.get_statistics()
    print("\n📊 STATISTICS")
    print("-" * 100)
    print(f"Total Candidates:     {stats['total_candidates']}")
    print(f"Active Job Posts:     {stats['active_jobs']}")
    print(f"Total Matches:        {stats['total_matches']}")
    if stats['average_match_score'] > 0:
        print(f"Average Match Score:  {stats['average_match_score']*100:.2f}%")
    
    # Candidates
    print("\n👥 CANDIDATES")
    print("-" * 100)
    candidates = db.get_all_candidates()
    if candidates:
        df = pd.DataFrame(candidates)
        display_cols = ['id', 'name', 'email', 'phone', 'experience_years', 'resume_filename']
        available_cols = [col for col in display_cols if col in df.columns]
        print(df[available_cols].to_string(index=False))
        print(f"\nTotal: {len(candidates)} candidates")
    else:
        print("No candidates in database.")
    
    # Jobs
    print("\n💼 JOB POSTS")
    print("-" * 100)
    jobs = db.get_all_job_posts(status='all')
    if jobs:
        df = pd.DataFrame(jobs)
        display_cols = ['id', 'title', 'company', 'location', 'status', 'required_experience_years']
        available_cols = [col for col in display_cols if col in df.columns]
        print(df[available_cols].to_string(index=False))
        print(f"\nTotal: {len(jobs)} jobs")
    else:
        print("No job posts in database.")
    
    # Matches
    print("\n🎯 MATCHES")
    print("-" * 100)
    matches = db.get_top_matches(limit=50)
    if matches:
        df = pd.DataFrame(matches)
        df['match_score'] = (df['match_score'] * 100).round(1)
        df = df.rename(columns={'match_score': 'score_%'})
        print(df.to_string(index=False))
        print(f"\nTotal: {len(matches)} matches shown (max 50)")
    else:
        print("No matches in database.")
    
    print("\n" + "="*100)
    print("\nDatabase location: database/resume_shortlister.db")
    print("="*100 + "\n")


if __name__ == "__main__":
    main()
