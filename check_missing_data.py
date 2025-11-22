import pandas as pd

# Load data
df = pd.read_csv('resume_data.csv', encoding='utf-8-sig')
df.columns = [col.encode('ascii', 'ignore').decode('ascii').strip() for col in df.columns]

print(f"Total rows: {len(df)}\n")
print("Missing Data Percentage by Column:\n")
print("="*60)

# Calculate missing percentages
missing_stats = []
for col in df.columns:
    null_count = df[col].isna().sum()
    null_pct = (null_count / len(df)) * 100
    missing_stats.append({
        'Column': col,
        'Null Count': null_count,
        'Null %': null_pct
    })

# Sort by null percentage
missing_df = pd.DataFrame(missing_stats).sort_values('Null %', ascending=False)

print(missing_df.to_string(index=False))

print("\n" + "="*60)
print("\nColumns with >40% missing data:")
high_missing = missing_df[missing_df['Null %'] > 40]
print(high_missing['Column'].tolist())

print("\n" + "="*60)
print("\nColumns with <40% missing data (KEEP THESE):")
keep_cols = missing_df[missing_df['Null %'] <= 40]
print(keep_cols['Column'].tolist())

# Categorize columns
resume_potential = ['career_objective', 'skills', 'educational_institution_name', 
                   'degree_names', 'passing_years', 'major_field_of_studies', 
                   'professional_company_names', 'positions', 'responsibilities',
                   'locations', 'extra_curricular_activity_types']

job_potential = ['job_position_name', 'educationaL_requirements', 
                'experiencere_requirement', 'responsibilities.1', 
                'related_skils_in_job', 'skills_required']

print("\n" + "="*60)
print("\nRECOMMENDED RESUME COLUMNS (with <40% missing):")
resume_good = [col for col in resume_potential if col in keep_cols['Column'].values]
print(resume_good)

print("\nRECOMMENDED JOB COLUMNS (with <40% missing):")
job_good = [col for col in job_potential if col in keep_cols['Column'].values]
print(job_good)
