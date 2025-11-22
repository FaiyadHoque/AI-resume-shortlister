import pandas as pd
import ast

def extract_text(value):
    if pd.isna(value):
        return ''
    try:
        parsed = ast.literal_eval(str(value))
        if isinstance(parsed, list):
            return ' '.join(str(item) for item in parsed if item)
        return str(value)
    except:
        return str(value)

# Load data
df = pd.read_csv('resume_data.csv', encoding='utf-8-sig')
df.columns = [col.encode('ascii', 'ignore').decode('ascii').strip() for col in df.columns]

print(f"Total rows in CSV: {len(df)}\n")

# Check null percentages
resume_cols = ['career_objective', 'skills', 'educational_institution_name', 
               'degree_names', 'major_field_of_studies', 'professional_company_names', 
               'positions', 'responsibilities']

job_cols = ['job_position_name', 'educationaL_requirements', 
            'experiencere_requirement', 'responsibilities.1', 'related_skils_in_job']

print("NULL PERCENTAGES:")
print("\nResume columns:")
for col in resume_cols:
    null_pct = (df[col].isna().sum() / len(df)) * 100
    print(f"  {col}: {null_pct:.1f}%")

print("\nJob columns:")
for col in job_cols:
    null_pct = (df[col].isna().sum() / len(df)) * 100
    print(f"  {col}: {null_pct:.1f}%")

# Extract text
df['resume_text'] = df[resume_cols].apply(
    lambda row: ' '.join(extract_text(val) for val in row), axis=1
)

df['job_text'] = df[job_cols].apply(
    lambda row: ' '.join(extract_text(val) for val in row), axis=1
)

# Check text lengths
df['resume_len'] = df['resume_text'].str.len()
df['job_len'] = df['job_text'].str.len()

print(f"\n\nTEXT LENGTH STATISTICS:")
print(f"Resume text length - min: {df['resume_len'].min()}, max: {df['resume_len'].max()}, mean: {df['resume_len'].mean():.0f}")
print(f"Job text length - min: {df['job_len'].min()}, max: {df['job_len'].max()}, mean: {df['job_len'].mean():.0f}")

print(f"\n\nFILTERING RESULTS:")
print(f"Rows with resume_len > 10: {(df['resume_len'] > 10).sum()}")
print(f"Rows with job_len > 10: {(df['job_len'] > 10).sum()}")
print(f"Rows with BOTH > 10: {((df['resume_len'] > 10) & (df['job_len'] > 10)).sum()}")

# Show some examples
print(f"\n\nSAMPLE ROWS WITH SHORT TEXT:")
short_rows = df[(df['resume_len'] <= 10) | (df['job_len'] <= 10)].head(3)
for idx, row in short_rows.iterrows():
    print(f"\nRow {idx}:")
    print(f"  Resume: '{row['resume_text']}'")
    print(f"  Job: '{row['job_text']}'")
