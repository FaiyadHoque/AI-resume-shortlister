import pandas as pd
import ast

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

# Process original
print("=" * 70)
print("ORIGINAL DATA (from real resumes):")
print("=" * 70)
orig = df[df['is_synthetic']==False].iloc[0]
orig_text = ' '.join([safe_extract(orig[col]) for col in resume_cols if col in df.columns])
print(orig_text[:400])
print(f"\nLength: {len(orig_text)} chars")

# Process synthetic  
print("\n" + "=" * 70)
print("SYNTHETIC DATA (generated):")
print("=" * 70)
synth = df[df['is_synthetic']==True].iloc[0]
synth_text = ' '.join([safe_extract(synth[col]) for col in resume_cols if col in df.columns])
print(synth_text[:400])
print(f"\nLength: {len(synth_text)} chars")

# Check test file
print("\n" + "=" * 70)
print("TEST RESUME (data_scientist_resume.txt):")
print("=" * 70)
with open('data_scientist_resume.txt', 'r') as f:
    test_text = f.read()
print(test_text[:400])
print(f"\nLength: {len(test_text)} chars")

print("\n" + "=" * 70)
print("ANALYSIS:")
print("=" * 70)
print(f"Original format: List strings → Space-separated words")
print(f"Synthetic format: Plain text sentences")
print(f"Test file format: Plain text with formatting")
print(f"\n❌ PROBLEM: Test files don't match training data format!")
print(f"Test files need to be in the SAME format as training data")
