"""
Test script to verify chef resume vs marketing job (should be rejected)
"""

import os
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

from matching_engine import MatchingEngine

def test_mismatch():
    """Test chef resume with marketing job (should not be shortlisted)"""
    
    # Read chef resume
    with open('chef_resume_converted.txt', 'r', encoding='utf-8') as f:
        chef_resume = f.read()
    
    # Read marketing job
    with open('marketing_job_converted.txt', 'r', encoding='utf-8') as f:
        marketing_job = f.read()
    
    # Initialize matching engine
    print("Initializing matching engine...\n")
    engine = MatchingEngine()
    
    # Test match
    print("="*60)
    print("MISMATCH TEST: Chef Resume vs Marketing Job")
    print("="*60)
    
    score = engine.predict_match(chef_resume, marketing_job)
    category = engine.get_match_category(score)
    
    print(f"\n📊 Match Score: {score}/100")
    print(f"📈 Category: {category}")
    
    print("\n" + "="*60)
    print("ANALYSIS:")
    print("="*60)
    if score < 65:
        print("✓ EXPECTED: Below threshold - candidate NOT SHORTLISTED")
        print("✓ Chef resume correctly rejected for marketing job")
        print("✓ Domain mismatch penalty working correctly")
    else:
        print("✗ UNEXPECTED: Above threshold - candidate shortlisted")
        print("✗ Chef should not match marketing job")
        print("⚠ Domain penalty may need to be increased")
    
    print(f"\nShortlisting Threshold:")
    print(f"  - Below 65: NOT SHORTLISTED")
    print(f"  - 65 and above: SHORTLISTED")
    print("="*60)

if __name__ == "__main__":
    try:
        test_mismatch()
    except Exception as e:
        print(f"\n❌ Error: {e}")
