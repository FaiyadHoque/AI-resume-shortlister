"""
Generate synthetic negative samples: TECHNICAL resumes × NON-TECHNICAL jobs
This complements the existing synthetic data (non-tech resumes × tech jobs)
"""

import pandas as pd
import numpy as np
import ast

# Load augmented dataset
df = pd.read_csv('resume_data_augmented.csv', encoding='utf-8-sig', index_col=False)

# Get original samples only
originals = df[df['is_synthetic'] == False].copy()

print(f"Original samples: {len(originals)}")

# Find technical resumes from original data
tech_keywords = ['python', 'machine learning', 'data science', 'tensorflow', 
                 'software', 'programming', 'engineering', 'java', 'c++']

def safe_extract(value):
    if pd.isna(value) or value == '':
        return ''
    try:
        if isinstance(value, str) and value.startswith('['):
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return ' '.join(str(x) for x in parsed if x)
        return str(value)
    except:
        return str(value) if value else ''

# Find technical resumes
tech_resumes = []
for idx, row in originals.iterrows():
    skills_text = safe_extract(row['skills']).lower()
    score = sum([1 for kw in tech_keywords if kw in skills_text])
    if score >= 2:  # At least 2 technical keywords
        tech_resumes.append(row)

print(f"Found {len(tech_resumes)} technical resumes")

# Non-technical job templates
non_tech_jobs = [
    {
        'job_position_name': 'Marketing Manager',
        'educationaL_requirements': 'Bachelor Degree Marketing Business Administration',
        'experiencere_requirement': '3-5 years Marketing Management',
        'responsibilities.1': 'Social Media Marketing Campaign Management Brand Strategy Customer Engagement Content Creation Market Research Analytics',
        'related_skils_in_job': 'Social Media Facebook Instagram Twitter LinkedIn TikTok Email Marketing SEO SEM Google Analytics',
        'skills_required': 'Marketing Strategy Brand Management Social Media Content Marketing Campaign Management Customer Relationship Management CRM Market Analysis'
    },
    {
        'job_position_name': 'Human Resources Manager', 
        'educationaL_requirements': 'Bachelor Degree Human Resources Business Administration',
        'experiencere_requirement': '5+ years HR Management',
        'responsibilities.1': 'Recruitment Employee Relations Performance Management Training Development Compensation Benefits Policy Implementation',
        'related_skils_in_job': 'Recruitment Interviewing Onboarding Employee Relations Performance Management Conflict Resolution',
        'skills_required': 'HR Management Recruitment Training Development Employee Relations Labor Law Performance Management Benefits Administration'
    },
    {
        'job_position_name': 'Sales Manager',
        'educationaL_requirements': 'Bachelor Degree Business Sales Marketing',
        'experiencere_requirement': '3-5 years Sales Management',
        'responsibilities.1': 'Sales Strategy Client Acquisition Account Management Team Leadership Revenue Growth Forecasting CRM Management',
        'related_skils_in_job': 'Sales Strategy Client Relationship B2B B2C Negotiation Closing Cold Calling Account Management',
        'skills_required': 'Sales Management Business Development Client Acquisition Account Management Team Leadership CRM Salesforce Negotiation'
    },
    {
        'job_position_name': 'Operations Manager',
        'educationaL_requirements': 'Bachelor Degree Business Operations Management',
        'experiencere_requirement': '5+ years Operations Management',
        'responsibilities.1': 'Operations Planning Process Improvement Supply Chain Management Budget Management Team Coordination Quality Control',
        'related_skils_in_job': 'Operations Planning Supply Chain Logistics Inventory Management Process Improvement Quality Assurance',
        'skills_required': 'Operations Management Process Improvement Supply Chain Management Budget Planning Team Leadership Quality Control'
    }
]

# Generate synthetic samples
synthetic_samples = []
target_samples = 1000  # Generate 1000 tech × non-tech mismatches

np.random.seed(42)

for i in range(target_samples):
    # Pick random technical resume
    tech_resume = tech_resumes[i % len(tech_resumes)]
    
    # Pick random non-technical job
    job = non_tech_jobs[i % len(non_tech_jobs)]
    
    # Create mismatch with low score (0.05 to 0.25)
    base_score = np.random.uniform(0.10, 0.18)
    noise = np.random.uniform(-0.03, 0.03)
    final_score = np.clip(base_score + noise, 0.05, 0.25)
    
    # Create synthetic sample
    sample = {
        'career_objective': tech_resume['career_objective'],
        'skills': tech_resume['skills'],
        'educational_institution_name': tech_resume['educational_institution_name'],
        'degree_names': tech_resume['degree_names'],
        'major_field_of_studies': tech_resume['major_field_of_studies'],
        'related_skils_in_job': job['related_skils_in_job'],
        'positions': tech_resume['positions'],
        'responsibilities': tech_resume['responsibilities'],
        'professional_company_names': tech_resume.get('professional_company_names', ''),
        'job_position_name': job['job_position_name'],
        'educationaL_requirements': job['educationaL_requirements'],
        'experiencere_requirement': job['experiencere_requirement'],
        'responsibilities.1': job['responsibilities.1'],
        'skills_required': job['skills_required'],
        'matched_score': final_score,
        'is_synthetic': True
    }
    
    synthetic_samples.append(sample)

# Create DataFrame
synthetic_df = pd.DataFrame(synthetic_samples)

print(f"\n✅ Generated {len(synthetic_df)} synthetic samples")
print(f"   Type: Technical resumes × Non-technical jobs")
print(f"   Score range: {synthetic_df['matched_score'].min():.3f} - {synthetic_df['matched_score'].max():.3f}")
print(f"   Score mean: {synthetic_df['matched_score'].mean():.3f}")

# Combine with existing augmented dataset
combined_df = pd.concat([df, synthetic_df], ignore_index=True)

# Save
combined_df.to_csv('resume_data_augmented_v2.csv', index=False, encoding='utf-8-sig')

print(f"\n✅ Saved to resume_data_augmented_v2.csv")
print(f"   Original samples: {len(df[df['is_synthetic'] == False])}")
print(f"   Synthetic (non-tech × tech): {len(df[df['is_synthetic'] == True])}")
print(f"   Synthetic (tech × non-tech): {len(synthetic_df)}")
print(f"   Total samples: {len(combined_df)}")
print(f"   Synthetic percentage: {len(combined_df[combined_df['is_synthetic'] == True]) / len(combined_df) * 100:.1f}%")
