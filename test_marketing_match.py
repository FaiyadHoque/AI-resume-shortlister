"""
Test script to match marketing resume with marketing job
Tests same-domain matching (should be shortlisted)
"""

import os
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

from matching_engine import MatchingEngine

def test_marketing_match():
    """Test matching between marketing resume and marketing job"""
    
    # Read marketing resume (converted format - properly formatted for model)
    print("Reading marketing_resume_converted.txt...")
    with open('marketing_resume_converted.txt', 'r', encoding='utf-8') as f:
        marketing_resume_converted = f.read()
    
    # Read marketing job (converted format - properly formatted for model)
    print("Reading marketing_job_converted.txt...")
    with open('marketing_job_converted.txt', 'r', encoding='utf-8') as f:
        marketing_job = f.read()
    
    # Initialize matching engine
    print("\nInitializing matching engine...")
    engine = MatchingEngine()
    
    # Test match
    print("\n" + "="*60)
    print("MATCHING TEST: Marketing Resume vs Marketing Job")
    print("="*60)
    
    score = engine.predict_match(marketing_resume_converted, marketing_job)
    category = engine.get_match_category(score)
    
    print(f"\n📊 Match Score: {score}/100")
    print(f"📈 Category: {category}")
    
    print("\n" + "-"*60)
    print("RESUME PREVIEW (first 200 chars):")
    print(marketing_resume_converted[:200] + "...")
    
    print("\n" + "-"*60)
    print("JOB PREVIEW (first 200 chars):")
    print(marketing_job[:200] + "...")
    
    print("\n" + "="*60)
    print("ANALYSIS:")
    print("="*60)
    if score >= 65:
        print("✓ EXPECTED: Above threshold - candidate SHORTLISTED")
        print("✓ Marketing resume correctly matches marketing job")
        print("✓ Same domain (marketing) - no penalty applied")
    else:
        print("✗ UNEXPECTED: Below threshold - candidate not shortlisted")
        print("✗ Marketing resume should match marketing job")
        print("⚠ May need to adjust threshold or check domain detection")
    
    print(f"\nShortlisting Threshold:")
    print(f"  - Below 65: NOT SHORTLISTED")
    print(f"  - 65 and above: SHORTLISTED")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        test_marketing_match()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the files exist:")
        print("  - marketing_resume_normal.txt")
        print("  - marketing_job.txt")
    except Exception as e:
        print(f"\n❌ Error during matching: {e}")
