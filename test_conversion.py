"""
Test script to convert chef resume and marketing job to model-ready format
Uses cnvrt.py functions to process the text files
"""

from cnvrt import condense_resume, condense_job_posting

def convert_files():
    """Convert chef resume and marketing job to model-ready format"""
    
    # Read chef resume
    print("Reading chef_resume_normal.txt...")
    with open('chef_resume_normal.txt', 'r', encoding='utf-8') as f:
        chef_resume_text = f.read()
    
    # Read marketing job
    print("Reading marketing_job_normal.txt...")
    with open('marketing_job_normal.txt', 'r', encoding='utf-8') as f:
        marketing_job_text = f.read()
    
    # Convert chef resume
    print("\nConverting chef resume with Gemini AI...")
    chef_resume_converted = condense_resume(chef_resume_text)
    
    # Convert marketing job
    print("Converting marketing job with Gemini AI...")
    marketing_job_converted = condense_job_posting(marketing_job_text)
    
    # Save converted chef resume
    print("\nSaving chef_resume_converted.txt...")
    with open('chef_resume_converted.txt', 'w', encoding='utf-8') as f:
        f.write(chef_resume_converted)
    
    # Save converted marketing job
    print("Saving marketing_job_converted.txt...")
    with open('marketing_job_converted.txt', 'w', encoding='utf-8') as f:
        f.write(marketing_job_converted)
    
    print("\n" + "="*60)
    print("CONVERSION COMPLETE")
    print("="*60)
    print(f"\nChef Resume - Original length: {len(chef_resume_text)} characters")
    print(f"Chef Resume - Converted length: {len(chef_resume_converted)} characters")
    print(f"\nMarketing Job - Original length: {len(marketing_job_text)} characters")
    print(f"Marketing Job - Converted length: {len(marketing_job_converted)} characters")
    print("\nOutput files created:")
    print("  - chef_resume_converted.txt")
    print("  - marketing_job_converted.txt")
    print("\n" + "="*60)
    
    # Show preview of converted text
    print("\nPREVIEW - Chef Resume (first 200 chars):")
    print("-" * 60)
    print(chef_resume_converted[:200] + "...")
    print()
    
    print("\nPREVIEW - Marketing Job (first 200 chars):")
    print("-" * 60)
    print(marketing_job_converted[:200] + "...")
    print()

if __name__ == "__main__":
    try:
        convert_files()
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Make sure chef_resume_normal.txt and marketing_job_normal.txt exist in the current directory.")
    except Exception as e:
        print(f"\nError during conversion: {e}")
        print("Make sure cnvrt.py is properly configured with Gemini API key.")
