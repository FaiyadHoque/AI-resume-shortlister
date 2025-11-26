"""
Test script to match chef resume with marketing job using XGBoost model
Uses the converted text files
"""

import os
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

from matching_engine import MatchingEngine

def test_match():
    """Test matching between chef resume and marketing job"""
    
    # Read converted chef resume
    print("Reading chef_resume_converted.txt...")
    with open('chef_resume_converted.txt', 'r', encoding='utf-8') as f:
        chef_resume = f.read()
    
    # Read converted marketing job
    print("Reading marketing_job_converted.txt...")
    with open('marketing_job_converted.txt', 'r', encoding='utf-8') as f:
        marketing_job = f.read()
    
    # Initialize matching engine
    print("\nInitializing matching engine...")
    engine = MatchingEngine()
    
    # Test match
    print("\n" + "="*60)
    print("MATCHING TEST: Chef Resume vs Marketing Job")
    print("="*60)
    
    score = engine.predict_match(chef_resume, marketing_job)
    category = engine.get_match_category(score)
    
    print(f"\n📊 Match Score: {score}/100")
    print(f"📈 Category: {category}")
    
    print("\n" + "-"*60)
    print("RESUME PREVIEW (first 200 chars):")
    print(chef_resume[:200] + "...")
    
    print("\n" + "-"*60)
    print("JOB PREVIEW (first 200 chars):")
    print(marketing_job[:200] + "...")
    
    print("\n" + "="*60)
    print("ANALYSIS:")
    print("="*60)
    if score < 30:
        print("✓ EXPECTED: Low score for chef resume vs marketing job (mismatch)")
        print("✓ The model correctly identifies this as a poor match")
    elif score > 60:
        print("✗ UNEXPECTED: High score indicates model may need adjustment")
    else:
        print("~ MODERATE: Score in middle range")
    
    print(f"\nScore breakdown:")
    print(f"  - 0-40: Poor match (expected for this test)")
    print(f"  - 40-55: Moderate match")
    print(f"  - 55-70: Good match")
    print(f"  - 70-100: Excellent match")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        test_match()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the converted files exist:")
        print("  - chef_resume_converted.txt")
        print("  - marketing_job_converted.txt")
    except Exception as e:
        print(f"\n❌ Error during matching: {e}")
