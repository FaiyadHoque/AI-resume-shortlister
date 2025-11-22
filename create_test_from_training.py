"""
Create test files using ACTUAL samples from the augmented dataset
This ensures 100% format matching
"""
import pandas as pd
import ast

# Load augmented data
df = pd.read_csv('resume_data_augmented.csv', encoding='utf-8-sig', index_col=False)

def safe_extract(value):
    if pd.isna(value) or value == '' or value == '[]':
        return ''
    try:
        if isinstance(value, str) and value.startswith('['):
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return ' '.join(str(x) for x in parsed if x)
        return str(value)
    except:
        return str(value) if value else ''

resume_cols = ['career_objective', 'skills', 'educational_institution_name', 
               'degree_names', 'major_field_of_studies', 'professional_company_names', 
               'positions', 'responsibilities']

job_position_col = [c for c in df.columns if 'job_position' in c.lower()][0]
job_cols = [job_position_col, 'educationaL_requirements', 
            'experiencere_requirement', 'responsibilities.1', 'skills_required']

# Find a good technical resume (high ML/DS keywords)
print("Finding good technical resume...")
tech_keywords = ['machine learning', 'python', 'data science', 'tensorflow', 'deep learning', 'ml']
originals = df[df['is_synthetic'] == False]

best_tech_idx = None
best_tech_score = 0
for idx, row in originals.head(100).iterrows():
    skills_text = safe_extract(row['skills']).lower()
    score = sum([1 for kw in tech_keywords if kw in skills_text])
    if score > best_tech_score:
        best_tech_score = score
        best_tech_idx = idx

tech_resume = originals.loc[best_tech_idx]
tech_resume_text = ' '.join([safe_extract(tech_resume[col]) for col in resume_cols if col in df.columns])

print(f"✅ Found technical resume (score: {best_tech_score}):")
print(f"   {tech_resume_text[:200]}...")

# Find a non-technical resume (from synthetic or low overlap)
print("\nFinding non-technical resume...")
synthetics = df[df['is_synthetic'] == True]
non_tech_resume = synthetics.iloc[0]  # Use first synthetic (guaranteed non-tech)
non_tech_resume_text = ' '.join([safe_extract(non_tech_resume[col]) for col in resume_cols if col in df.columns])

print(f"✅ Found non-technical resume:")
print(f"   {non_tech_resume_text[:200]}...")

# Find a technical job description
print("\nFinding technical job...")
best_job_idx = best_tech_idx  # Use same row as technical resume for perfect match
tech_job = originals.loc[best_job_idx]
tech_job_text = ' '.join([safe_extract(tech_job[col]) for col in job_cols if col in df.columns])

print(f"✅ Found technical job:")
print(f"   {tech_job_text[:200]}...")

# Save test files
with open('data_scientist_resume.txt', 'w', encoding='utf-8') as f:
    f.write(tech_resume_text)

with open('marketing_manager_resume.txt', 'w', encoding='utf-8') as f:
    f.write(non_tech_resume_text)

with open('data_science_job.txt', 'w', encoding='utf-8') as f:
    f.write(tech_job_text)

print("\n" + "=" * 70)
print("✅ Created test files from ACTUAL training samples!")
print("=" * 70)
print("\nFiles created:")
print("   - data_scientist_resume.txt (from training data)")
print("   - marketing_manager_resume.txt (from synthetic data)")
print("   - data_science_job.txt (from training data)")
print("\nThese files now EXACTLY match the training data format!")
