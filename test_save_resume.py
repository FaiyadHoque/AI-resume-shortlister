"""
Test script to verify resume saving to database
"""
from database.db_manager import get_db
from pdf_extractor import extract_resume
import sys

def test_save_resume(pdf_path):
    """Test extracting and saving a resume"""
    print(f"\n{'='*60}")
    print(f"Testing Resume Save: {pdf_path}")
    print(f"{'='*60}\n")
    
    # Initialize database
    db = get_db()
    print("✅ Database connection established")
    
    # Extract resume
    print(f"\n📄 Extracting resume from: {pdf_path}")
    try:
        resume_data = extract_resume(pdf_path)
        print("✅ Resume extracted successfully!")
        print(f"\nExtracted Data:")
        print(f"  Name: {resume_data.get('name', 'N/A')}")
        print(f"  Email: {resume_data.get('email', 'N/A')}")
        print(f"  Phone: {resume_data.get('phone', 'N/A')}")
        print(f"  Experience: {resume_data.get('experience_years', 0)} years")
        print(f"  Skills length: {len(resume_data.get('skills', ''))} chars")
    except Exception as e:
        print(f"❌ Error extracting resume: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Save to database
    print(f"\n💾 Saving to database...")
    try:
        resume_data['resume_filename'] = pdf_path
        candidate_id = db.add_candidate(resume_data)
        print(f"✅ Candidate saved with ID: {candidate_id}")
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Verify by retrieving
    print(f"\n🔍 Verifying by retrieving candidate...")
    try:
        candidate = db.get_candidate(candidate_id)
        if candidate:
            print(f"✅ Retrieved candidate:")
            print(f"  ID: {candidate['id']}")
            print(f"  Name: {candidate['name']}")
            print(f"  Email: {candidate['email']}")
            print(f"  Phone: {candidate['phone']}")
        else:
            print(f"❌ Could not retrieve candidate with ID {candidate_id}")
            return False
    except Exception as e:
        print(f"❌ Error retrieving candidate: {e}")
        return False
    
    print(f"\n{'='*60}")
    print("✅ ALL TESTS PASSED!")
    print(f"{'='*60}\n")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        print("Usage: python test_save_resume.py <path_to_pdf>")
        print("\nNo PDF provided. Testing with sample text file instead...")
        
        # Create a test with dummy data
        from database.db_manager import get_db
        
        db = get_db()
        test_data = {
            'name': 'Test Candidate',
            'email': 'test@example.com',
            'phone': '+1-123-456-7890',
            'objective': 'Test objective',
            'education': 'Test University - BS Computer Science',
            'skills': 'Python, Java, SQL',
            'experience_years': 3,
            'experience_details': 'Software Engineer at Test Co.',
            'projects': 'Test project description',
            'certifications': 'AWS Certified',
            'resume_text': 'Full resume text here',
            'resume_filename': 'test_resume.pdf'
        }
        
        print("\n📝 Testing with dummy data...")
        try:
            candidate_id = db.add_candidate(test_data)
            print(f"✅ Test candidate saved with ID: {candidate_id}")
            
            # Retrieve and verify
            candidate = db.get_candidate(candidate_id)
            if candidate:
                print(f"✅ Retrieved test candidate:")
                print(f"  ID: {candidate['id']}")
                print(f"  Name: {candidate['name']}")
                print(f"  Email: {candidate['email']}")
                print("\n✅ Database save functionality is working!")
            else:
                print("❌ Failed to retrieve test candidate")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
