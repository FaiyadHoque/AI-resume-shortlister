"""
Verify the augmented dataset has proper structure
"""
import pandas as pd
import numpy as np

print("=" * 70)
print("🔍 VERIFYING AUGMENTED DATASET")
print("=" * 70)

# Load augmented data
df = pd.read_csv('resume_data_augmented.csv', encoding='utf-8-sig', index_col=False)

print(f"\n✅ Loaded augmented dataset")
print(f"   Total rows: {len(df)}")
print(f"   Total columns: {len(df.columns)}")

# Check synthetic rows
synthetic_count = df['is_synthetic'].sum()
original_count = len(df) - synthetic_count

print(f"\n📊 Dataset composition:")
print(f"   Original samples: {original_count}")
print(f"   Synthetic samples: {synthetic_count}")
print(f"   Synthetic ratio: {synthetic_count/len(df)*100:.1f}%")

# Check scores
print(f"\n📈 Score distribution:")
print(f"   All data - Mean: {df['matched_score'].mean():.3f}, Std: {df['matched_score'].std():.3f}")
print(f"   Original - Mean: {df[df['is_synthetic']==False]['matched_score'].mean():.3f}")
print(f"   Synthetic - Mean: {df[df['is_synthetic']==True]['matched_score'].mean():.3f}")

# Check if resume_text can be created from columns
resume_cols = ['career_objective', 'skills', 'educational_institution_name', 
               'degree_names', 'major_field_of_studies', 'professional_company_names', 
               'positions', 'responsibilities']

print(f"\n🔧 Testing resume_text creation...")
df['resume_text'] = df[resume_cols].fillna('').agg(' '.join, axis=1)

# Check synthetic rows have content
synthetic_sample = df[df['is_synthetic'] == True].iloc[0]
print(f"\n✅ Sample synthetic resume_text (first 150 chars):")
print(f"   {synthetic_sample['resume_text'][:150]}...")
print(f"   Length: {len(synthetic_sample['resume_text'])} characters")
print(f"   Match score: {synthetic_sample['matched_score']:.3f}")

# Check job_text creation
job_cols = ['job_position_name', 'educationaL_requirements', 
            'experiencere_requirement', 'responsibilities.1', 'skills_required']

# Handle BOM in column name
job_cols_cleaned = []
for col in job_cols:
    matching = [c for c in df.columns if col.replace('job_position_name', '').replace('_', '') in c.replace('_', '')]
    if matching:
        job_cols_cleaned.append(matching[0])
    elif col in df.columns:
        job_cols_cleaned.append(col)

# Find the job position column with BOM
job_position_col = [c for c in df.columns if 'job_position' in c.lower()][0]
job_cols_cleaned = [job_position_col, 'educationaL_requirements', 
                   'experiencere_requirement', 'responsibilities.1', 'skills_required']

df['job_text'] = df[job_cols_cleaned].fillna('').agg(' '.join, axis=1)

synthetic_sample_idx = df[df['is_synthetic'] == True].index[0]
print(f"\n✅ Sample synthetic job_text (first 150 chars):")
print(f"   {df.loc[synthetic_sample_idx, 'job_text'][:150]}...")

# Check for empty texts
empty_resume = (df['resume_text'].str.strip() == '').sum()
empty_job = (df['job_text'].str.strip() == '').sum()

print(f"\n⚠️  Empty texts check:")
print(f"   Empty resume_text: {empty_resume} rows")
print(f"   Empty job_text: {empty_job} rows")

if empty_resume == 0 and empty_job == 0:
    print(f"\n✅ ALL CHECKS PASSED!")
    print(f"   The augmented dataset is properly structured.")
    print(f"   Ready to train the model!")
else:
    print(f"\n❌ WARNING: Some rows have empty text fields")
    print(f"   These will be filtered out during training")

print("\n" + "=" * 70)
