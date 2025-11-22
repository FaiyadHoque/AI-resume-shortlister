import pandas as pd

df = pd.read_csv('resume_data.csv', encoding='utf-8-sig', nrows=5)
df.columns = [col.encode('ascii', 'ignore').decode('ascii').strip() for col in df.columns]

print('Column names:')
for i, col in enumerate(df.columns, 1):
    print(f'{i}. "{col}"')

print('\n\nFirst row sample data:')
for col in df.columns[:8]:
    val = str(df[col].iloc[0])[:50]
    print(f'{col}: {val}...')

print(f'\n\nTotal columns: {len(df.columns)}')
print(f'Total rows: {len(df)}')
