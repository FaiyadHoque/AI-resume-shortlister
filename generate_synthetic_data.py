"""
Synthetic Data Generator using Gemini API
==========================================
This script creates diverse cross-domain resume-job pairs to fix model discrimination.

Steps:
1. Load existing dataset
2. Create cross-domain pairs (marketing → engineering, chef → data science, etc.)
3. Use Gemini API to score each pair
4. Save augmented dataset

Free Tier: 1000 matches per day (1M tokens)
"""

import pandas as pd
import numpy as np
import google.generativeai as genai
import time
import json
from tqdm import tqdm
import random

# ================== CONFIGURATION ==================

# Get your API key from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "AIzaSyBt-k8WBNysaok0loP3brx_HkVpiYLZoGU"  # Replace with your actual key

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')  # Updated to latest available model

# How many synthetic pairs to generate (start small for testing)
NUM_SYNTHETIC_PAIRS = 500  # Reduced from 2000 - will take ~15-20 minutes

# Output file
OUTPUT_FILE = "resume_data_augmented.csv"

# ================== DIVERSE RESUME TEMPLATES ==================

# Non-technical resumes for creating mismatches
NON_TECH_RESUMES = {
    "marketing_manager": """
Marketing Manager with 5+ years experience in digital marketing, brand strategy, and campaign management.
Skills: SEO/SEM, Google Analytics, Social Media Marketing, Content Strategy, Email Marketing, Adobe Creative Suite
Experience: Led campaigns generating $2M revenue, managed social media with 150% engagement increase
Education: BA in Marketing, Google Digital Marketing Certificate
""",
    
    "sales_executive": """
Sales Executive with 6 years in B2B sales, account management, and business development.
Skills: CRM (Salesforce), Negotiation, Client Relations, Pipeline Management, Presentation Skills
Experience: Closed $5M in deals, managed 50+ enterprise accounts, exceeded quota by 130%
Education: BBA in Business Administration
""",
    
    "hr_manager": """
Human Resources Manager with 7 years in recruitment, employee relations, and talent development.
Skills: Recruiting, HRIS Systems, Performance Management, Training & Development, Conflict Resolution
Experience: Hired 200+ employees, reduced turnover by 25%, implemented new onboarding program
Education: BA in Human Resources Management, SHRM-CP Certified
""",
    
    "accountant": """
Senior Accountant with 8 years in financial reporting, auditing, and tax preparation.
Skills: QuickBooks, Excel, GAAP, Financial Analysis, Budgeting, Tax Compliance, Auditing
Experience: Managed $10M budget, conducted quarterly audits, prepared financial statements
Education: BS in Accounting, CPA Certified
""",
    
    "graphic_designer": """
Graphic Designer with 5 years in visual design, branding, and creative production.
Skills: Adobe Photoshop, Illustrator, InDesign, UI/UX Design, Typography, Branding
Experience: Created 100+ brand identities, designed marketing materials, led creative campaigns
Education: BFA in Graphic Design
""",
    
    "project_manager": """
Project Manager with 6 years in agile project management, stakeholder coordination, and delivery.
Skills: Agile/Scrum, JIRA, Risk Management, Budget Planning, Team Leadership
Experience: Delivered 30+ projects on time, managed $3M budgets, led cross-functional teams
Education: BS in Business Administration, PMP Certified
""",
    
    "content_writer": """
Content Writer with 4 years in copywriting, blog writing, and content strategy.
Skills: SEO Writing, Content Marketing, WordPress, Research, Editing, Social Media Copy
Experience: Published 500+ articles, increased organic traffic by 200%, managed content calendar
Education: BA in English Literature
""",
    
    "chef": """
Executive Chef with 10 years in culinary arts, menu development, and kitchen management.
Skills: French Cuisine, Recipe Development, Food Safety, Inventory Management, Staff Training
Experience: Managed kitchen of 15 staff, created award-winning menus, reduced food costs by 20%
Education: Culinary Arts Diploma, ServSafe Certified
""",
    
    "nurse": """
Registered Nurse with 8 years in patient care, emergency medicine, and health assessment.
Skills: Patient Assessment, IV Therapy, Emergency Care, Electronic Health Records, CPR/BLS
Experience: Provided care for 1000+ patients, worked in ER and ICU, trained new nurses
Education: BSN in Nursing, RN License
""",
    
    "teacher": """
High School Teacher with 7 years in education, curriculum development, and student assessment.
Skills: Lesson Planning, Classroom Management, Educational Technology, Student Assessment
Experience: Taught 500+ students, improved test scores by 15%, developed new curriculum
Education: MS in Education, State Teaching License
"""
}

# ================== SCORING FUNCTION ==================

def score_resume_job_with_gemini(resume_text, job_text, retries=3):
    """
    Use Gemini API to score resume-job match on 0-100 scale
    """
    prompt = f"""You are an expert HR recruiter. Rate how well this resume matches the job description.

**Job Description:**
{job_text[:1000]}

**Resume:**
{resume_text[:1000]}

**Scoring Guidelines:**
- 90-100: Perfect match - candidate exceeds all requirements
- 70-89: Strong match - meets most key requirements
- 50-69: Moderate match - some relevant skills but gaps exist
- 30-49: Weak match - limited relevance, different domain
- 10-29: Poor match - minimal overlap, wrong field entirely
- 0-9: No match - completely unrelated

Consider:
1. **Domain alignment** (tech vs non-tech, industry match)
2. **Required skills** vs possessed skills
3. **Experience level** match
4. **Education requirements** alignment

Provide ONLY a number between 0-100. No explanation, just the score.
Your response:"""

    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            score_text = response.text.strip()
            
            # Extract number from response
            import re
            numbers = re.findall(r'\d+', score_text)
            if numbers:
                score = int(numbers[0])
                # Normalize to 0-1 range for consistency with dataset
                return min(max(score, 0), 100) / 100.0
            else:
                print(f"⚠️ Could not parse score from: {score_text}")
                return None
                
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)  # Wait before retry
            else:
                print(f"❌ All attempts failed for this pair")
                return None
    
    return None

# ================== MAIN GENERATION LOGIC ==================

def load_existing_data():
    """Load the original resume dataset"""
    print("📂 Loading existing dataset...")
    
    encodings = ['utf-8-sig', 'utf-8', 'latin-1']
    for encoding in encodings:
        try:
            df = pd.read_csv('resume_data.csv', encoding=encoding, index_col=False)
            print(f"✅ Loaded {len(df)} samples with encoding: {encoding}")
            return df
        except:
            continue
    
    raise Exception("❌ Could not load resume_data.csv")

def extract_text(value):
    """Extract text from list-formatted strings"""
    if pd.isna(value) or value == '' or value == '[]':
        return ''
    try:
        import ast
        if isinstance(value, str) and value.startswith('['):
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return ' '.join(str(x) for x in parsed if x)
        return str(value)
    except:
        return str(value) if value else ''

def generate_synthetic_pairs(df, num_pairs=2000):
    """
    Generate synthetic cross-domain pairs
    """
    print(f"\n🔧 Generating {num_pairs} synthetic pairs...")
    
    # Extract job descriptions from existing data
    job_cols = ['job_position_name', 'educationaL_requirements', 
                'experiencere_requirement', 'responsibilities.1', 
                'related_skils_in_job']
    job_cols = [col for col in job_cols if col in df.columns]
    
    print("📋 Creating job descriptions from dataset...")
    jobs = []
    for idx, row in df.iterrows():
        job_text = ' '.join(extract_text(row[col]) for col in job_cols)
        if len(job_text) > 50:  # Only use jobs with substantial text
            jobs.append({
                'text': job_text,
                'position': extract_text(row.get('job_position_name', 'Unknown'))
            })
        
        if len(jobs) >= 500:  # We don't need all jobs
            break
    
    print(f"✅ Extracted {len(jobs)} job descriptions")
    
    # Generate pairs
    synthetic_pairs = []
    success_count = 0
    
    # Strategy: Create intentional mismatches
    resumes_list = list(NON_TECH_RESUMES.keys())
    
    print("\n🎯 Generating cross-domain pairs...")
    print("This will use Gemini API to score each pair (FREE tier: 1000/day)")
    print("Estimated time: 15-20 minutes for 500 pairs\n")
    
    for i in tqdm(range(num_pairs), desc="Generating pairs"):
        # Randomly pick a non-tech resume and a job
        resume_type = random.choice(resumes_list)
        resume_text = NON_TECH_RESUMES[resume_type]
        job = random.choice(jobs)
        
        # Score with Gemini
        score = score_resume_job_with_gemini(resume_text, job['text'])
        
        if score is not None:
            success_count += 1
            synthetic_pairs.append({
                'resume_type': resume_type,
                'resume_text': resume_text,
                'job_text': job['text'],
                'job_position': job['position'],
                'matched_score': score,
                'is_synthetic': True
            })
            
            # Print progress every 50 successful pairs
            if success_count % 50 == 0:
                print(f"\n✅ Successfully scored {success_count} pairs so far...")
        
        # Rate limiting: 15 requests per minute for free tier
        if (i + 1) % 15 == 0:
            print(f"⏸️ Rate limit pause (completed {i+1}/{num_pairs})...")
            time.sleep(60)  # Wait 1 minute after every 15 requests
    
    print(f"\n✅ Generated {len(synthetic_pairs)} synthetic pairs (success rate: {len(synthetic_pairs)/num_pairs*100:.1f}%)")
    return synthetic_pairs

def create_augmented_dataset(df, synthetic_pairs):
    """
    Merge synthetic pairs with existing dataset
    """
    print("\n🔄 Creating augmented dataset...")
    
    # Prepare synthetic dataframe
    synthetic_df = pd.DataFrame(synthetic_pairs)
    
    # Ensure we have the necessary columns from original dataset
    resume_cols = ['career_objective', 'skills', 'educational_institution_name', 
                   'degree_names', 'major_field_of_studies', 'positions', 'responsibilities']
    job_cols = ['job_position_name', 'educationaL_requirements', 
                'experiencere_requirement', 'responsibilities.1', 
                'related_skils_in_job']
    
    # Create minimal synthetic rows that match original schema
    synthetic_rows = []
    for _, synth in synthetic_df.iterrows():
        row = {}
        
        # Fill with synthetic data
        row['resume_text'] = synth['resume_text']
        row['job_text'] = synth['job_text']
        row['matched_score'] = synth['matched_score']
        row['is_synthetic'] = True
        
        # Add placeholder columns to match original schema
        for col in df.columns:
            if col not in row:
                row[col] = ''
        
        synthetic_rows.append(row)
    
    synthetic_final = pd.DataFrame(synthetic_rows)
    
    # Add is_synthetic column to original data
    df['is_synthetic'] = False
    
    # Combine datasets
    augmented_df = pd.concat([df, synthetic_final], ignore_index=True)
    
    print(f"✅ Augmented dataset created!")
    print(f"   Original samples: {len(df)}")
    print(f"   Synthetic samples: {len(synthetic_final)}")
    print(f"   Total samples: {len(augmented_df)}")
    
    # Show score distribution
    print(f"\n📊 Score Distribution:")
    print(f"   0.0-0.3 (Poor):     {(augmented_df['matched_score'] < 0.3).sum()} samples")
    print(f"   0.3-0.5 (Weak):     {((augmented_df['matched_score'] >= 0.3) & (augmented_df['matched_score'] < 0.5)).sum()} samples")
    print(f"   0.5-0.7 (Moderate): {((augmented_df['matched_score'] >= 0.5) & (augmented_df['matched_score'] < 0.7)).sum()} samples")
    print(f"   0.7-1.0 (Strong):   {(augmented_df['matched_score'] >= 0.7).sum()} samples")
    
    return augmented_df

# ================== MAIN EXECUTION ==================

def main():
    print("=" * 70)
    print("🚀 SYNTHETIC DATA GENERATOR FOR RESUME MATCHING")
    print("=" * 70)
    
    # Check API key
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print("\n❌ ERROR: Please set your Gemini API key!")
        print("   1. Get free API key: https://aistudio.google.com/app/apikey")
        print("   2. Replace 'YOUR_API_KEY_HERE' in this script")
        return
    
    # Load existing data
    df = load_existing_data()
    
    # Generate synthetic pairs
    synthetic_pairs = generate_synthetic_pairs(df, num_pairs=NUM_SYNTHETIC_PAIRS)
    
    # Create augmented dataset
    augmented_df = create_augmented_dataset(df, synthetic_pairs)
    
    # Save to file
    print(f"\n💾 Saving augmented dataset to {OUTPUT_FILE}...")
    augmented_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"✅ Saved successfully!")
    
    # Save metadata
    metadata = {
        'original_samples': len(df),
        'synthetic_samples': len(synthetic_pairs),
        'total_samples': len(augmented_df),
        'generation_date': pd.Timestamp.now().isoformat(),
        'gemini_model': 'gemini-1.5-flash',
        'non_tech_resume_types': list(NON_TECH_RESUMES.keys())
    }
    
    with open('augmented_data_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n" + "=" * 70)
    print("✅ DATASET AUGMENTATION COMPLETE!")
    print("=" * 70)
    print(f"\nNext steps:")
    print(f"1. Open your notebook: AI_Resume_Matcher_SEMANTIC.ipynb")
    print(f"2. Change line: df = pd.read_csv('resume_data.csv')")
    print(f"   To:          df = pd.read_csv('{OUTPUT_FILE}')")
    print(f"3. Re-run training cells")
    print(f"\nExpected improvement:")
    print(f"  Marketing → Data Science: 65-70 → 20-25 (MUCH BETTER!)")
    print(f"  Data Scientist → Data Science: 70-80 → 85-95 (BETTER!)")

if __name__ == "__main__":
    main()
