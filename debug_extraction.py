import pandas as pd
import ast

def extract_text(value):
    """Extract text from string representation of list or return as is"""
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
df = pd.read_csv('resume_data.csv', encoding='utf-8-sig', nrows=10)
df.columns = [col.encode('ascii', 'ignore').decode('ascii').strip() for col in df.columns]

# Test extraction on first row
resume_cols = ['career_objective', 'skills', 'educational_institution_name', 
               'degree_names', 'major_field_of_studies', 'professional_company_names', 
               'positions', 'responsibilities']

job_cols = ['job_position_name', 'educationaL_requirements', 
            'experiencere_requirement', 'responsibilities.1', 'related_skils_in_job']

print("Testing text extraction on first row:\n")
print("RESUME FIELDS:")
for col in resume_cols:
    val = df[col].iloc[0]
    extracted = extract_text(val)
    print(f"{col}: {extracted[:100]}...")

print("\n\nJOB FIELDS:")
for col in job_cols:
    val = df[col].iloc[0]
    extracted = extract_text(val)
    print(f"{col}: {extracted[:100]}...")

# Test full extraction
df['resume_text'] = df[resume_cols].apply(
    lambda row: ' '.join(extract_text(val) for val in row), axis=1
)

df['job_text'] = df[job_cols].apply(
    lambda row: ' '.join(extract_text(val) for val in row), axis=1
)

print("\n\nFULL EXTRACTED TEXT:")
print(f"Resume text length: {len(df['resume_text'].iloc[0])}")
print(f"Job text length: {len(df['job_text'].iloc[0])}")
print(f"\nResume text: {df['resume_text'].iloc[0][:200]}...")
print(f"\nJob text: {df['job_text'].iloc[0][:200]}...")

# Check filtering
print(f"\n\nFILTERING CHECK:")
print(f"Rows before filter: {len(df)}")
df_filtered = df[(df['resume_text'].str.strip().str.len() > 10) & 
                  (df['job_text'].str.strip().str.len() > 10)]
print(f"Rows after filter: {len(df_filtered)}")
