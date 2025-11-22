"""
Generate synthetic POSITIVE samples: Marketing resumes × Marketing jobs
This teaches the model that non-tech matches should score HIGH
"""

import pandas as pd
import numpy as np
import ast

# Load current dataset
df = pd.read_csv('resume_data_augmented_v2.csv', encoding='utf-8-sig', index_col=False)

# Get original samples only
originals = df[df['is_synthetic'] == False].copy()

print(f"Original samples: {len(originals)}")

# Find marketing/sales/business resumes from original data
marketing_keywords = ['marketing', 'sales', 'business', 'advertising', 
                      'brand', 'social media', 'customer', 'client',
                      'promotional', 'campaign', 'outreach']

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

# Find marketing-related resumes
marketing_resumes = []
for idx, row in originals.iterrows():
    text = (safe_extract(row['skills']) + ' ' + 
            safe_extract(row['career_objective']) + ' ' +
            safe_extract(row['responsibilities'])).lower()
    score = sum([1 for kw in marketing_keywords if kw in text])
    if score >= 2:  # At least 2 marketing keywords
        marketing_resumes.append(row)

print(f"Found {len(marketing_resumes)} marketing-related resumes")

# Marketing job templates
marketing_jobs = [
    {
        'educationaL_requirements': 'Bachelor Degree Marketing Business Administration',
        'experiencere_requirement': '3-5 years Marketing Management',
        'responsibilities.1': 'Social Media Marketing Campaign Management Brand Strategy Customer Engagement Content Creation Market Research Analytics',
        'related_skils_in_job': 'Social Media Facebook Instagram Twitter LinkedIn TikTok Email Marketing SEO SEM Google Analytics',
        'skills_required': 'Marketing Strategy Brand Management Social Media Content Marketing Campaign Management Customer Relationship Management CRM Market Analysis'
    },
    {
        'educationaL_requirements': 'Bachelor Degree Business Marketing Sales',
        'experiencere_requirement': '3-5 years Sales Management',
        'responsibilities.1': 'Sales Strategy Client Acquisition Account Management Team Leadership Revenue Growth Forecasting CRM Management',
        'related_skils_in_job': 'Sales Strategy Client Relationship B2B B2C Negotiation Closing Cold Calling Account Management',
        'skills_required': 'Sales Management Business Development Client Acquisition Account Management Team Leadership CRM Salesforce Negotiation'
    },
    {
        'educationaL_requirements': 'Bachelor Degree Marketing Communications',
        'experiencere_requirement': '2-4 years Digital Marketing',
        'responsibilities.1': 'Digital Marketing Social Media Management Content Creation SEO SEM Email Marketing Analytics Campaign Management',
        'related_skils_in_job': 'Digital Marketing Social Media SEO SEM Google Ads Facebook Ads Content Marketing Email Marketing Analytics',
        'skills_required': 'Digital Marketing Social Media Marketing SEO SEM Content Marketing Email Marketing Google Analytics Campaign Management'
    },
    {
        'educationaL_requirements': 'Bachelor Degree Business Administration',
        'experiencere_requirement': '3-5 years Customer Success',
        'responsibilities.1': 'Customer Relationship Management Client Success Account Management Customer Support Customer Retention Satisfaction',
        'related_skils_in_job': 'Customer Success Client Management Account Management CRM Customer Support Relationship Building',
        'skills_required': 'Customer Relationship Management Client Success Account Management Communication Problem Solving CRM Salesforce'
    }
]

# Generate synthetic POSITIVE samples
synthetic_samples = []
target_samples = 2000  # Generate 2000 marketing × marketing MATCHES

np.random.seed(43)

for i in range(target_samples):
    # Pick random marketing resume
    if len(marketing_resumes) > 0:
        mk_resume = marketing_resumes[i % len(marketing_resumes)]
    else:
        print("WARNING: No marketing resumes found!")
        break
    
    # Pick random marketing job
    job = marketing_jobs[i % len(marketing_jobs)]
    
    # Create MATCH with HIGH score (0.60 to 0.85)
    base_score = np.random.uniform(0.65, 0.78)
    noise = np.random.uniform(-0.03, 0.03)
    final_score = np.clip(base_score + noise, 0.60, 0.85)
    
    # Create synthetic sample
    sample = {
        'career_objective': mk_resume['career_objective'],
        'skills': mk_resume['skills'],
        'educational_institution_name': mk_resume['educational_institution_name'],
        'degree_names': mk_resume['degree_names'],
        'major_field_of_studies': mk_resume.get('major_field_of_studies', ''),
        'related_skils_in_job': job['related_skils_in_job'],
        'positions': mk_resume.get('positions', ''),
        'responsibilities': mk_resume.get('responsibilities', ''),
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

print(f"\n✅ Generated {len(synthetic_df)} synthetic POSITIVE samples")
print(f"   Type: Marketing resumes × Marketing jobs (MATCHES)")
print(f"   Score range: {synthetic_df['matched_score'].min():.3f} - {synthetic_df['matched_score'].max():.3f}")
print(f"   Score mean: {synthetic_df['matched_score'].mean():.3f}")

# Combine with existing dataset
combined_df = pd.concat([df, synthetic_df], ignore_index=True)

# Save
combined_df.to_csv('resume_data_augmented_v3.csv', index=False, encoding='utf-8-sig')

print(f"\n✅ Saved to resume_data_augmented_v3.csv")
print(f"   Original samples: {len(df[df['is_synthetic'] == False])}")
print(f"   Synthetic negatives: {len(df[df['is_synthetic'] == True])}")
print(f"   Synthetic positives (marketing): {len(synthetic_df)}")
print(f"   Total samples: {len(combined_df)}")
print(f"   Synthetic percentage: {len(combined_df[combined_df['is_synthetic'] == True]) / len(combined_df) * 100:.1f}%")
