import pandas as pd

print("Testing CSV loading...\n")

# Try loading the CSV
df = pd.read_csv('resume_data.csv', encoding='utf-8-sig')

print(f"Raw shape: {df.shape}")
print(f"Raw columns: {df.columns.tolist()}\n")

# Clean column names
df.columns = [col.encode('ascii', 'ignore').decode('ascii').strip() for col in df.columns]

print(f"Cleaned columns: {df.columns.tolist()}\n")

# Check actual data in first row
print("First row raw data:")
print(df.iloc[0])

print("\n\nNull counts:")
for col in df.columns:
    null_count = df[col].isna().sum()
    null_pct = (null_count / len(df)) * 100
    print(f"{col}: {null_count}/{len(df)} ({null_pct:.1f}% null)")

print("\n\nFirst row actual values (not null check):")
for col in df.columns[:10]:
    val = df[col].iloc[0]
    print(f"{col}: type={type(val)}, isna={pd.isna(val)}, value='{val}'")
