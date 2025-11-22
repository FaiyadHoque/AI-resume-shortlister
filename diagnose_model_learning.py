"""
Diagnose what the model actually learned
Test with synthetic training samples to see if model can predict low scores AT ALL
"""
import joblib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

print("=" * 70)
print("🔬 DIAGNOSING MODEL LEARNING")
print("=" * 70)

# Load trained models
print("\n📦 Loading models...")
xgb_model = joblib.load('xgboost_semantic.pkl')
rf_model = joblib.load('random_forest_semantic.pkl')
scaler = joblib.load('scaler_semantic.pkl')
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load training data
print("📂 Loading training data...")
df = pd.read_csv('resume_data_augmented.csv', encoding='utf-8-sig', index_col=False)

# Get synthetic samples (should have low scores ~0.14)
synthetic_samples = df[df['is_synthetic'] == True].sample(n=10, random_state=42)
# Get original samples (should have high scores ~0.66)
original_samples = df[df['is_synthetic'] == False].sample(n=10, random_state=42)

print(f"\n📊 Sample scores:")
print(f"   Synthetic avg: {df[df['is_synthetic']==True]['matched_score'].mean():.3f}")
print(f"   Original avg:  {df[df['is_synthetic']==False]['matched_score'].mean():.3f}")

# Process samples
import ast

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

def process_sample(row):
    resume_text = ' '.join([safe_extract(row[col]) for col in resume_cols if col in df.columns])
    job_text = ' '.join([safe_extract(row[col]) for col in job_cols if col in df.columns])
    
    # Generate embeddings
    resume_emb = semantic_model.encode([resume_text])[0]
    job_emb = semantic_model.encode([job_text])[0]
    
    # Calculate features
    cos_sim = cosine_similarity([resume_emb], [job_emb])[0][0]
    euc_dist = euclidean_distances([resume_emb], [job_emb])[0][0]
    man_dist = np.sum(np.abs(resume_emb - job_emb))
    
    X = np.concatenate([resume_emb, job_emb, [cos_sim, euc_dist, man_dist]])
    X_scaled = scaler.transform([X])
    
    xgb_pred = xgb_model.predict(X_scaled)[0]
    rf_pred = rf_model.predict(X_scaled)[0]
    
    return {
        'actual': row['matched_score'],
        'xgb': xgb_pred,
        'rf': rf_pred,
        'cos_sim': cos_sim
    }

print("\n" + "=" * 70)
print("🔴 SYNTHETIC SAMPLES (Should predict LOW ~0.14):")
print("=" * 70)

synth_results = []
for idx, row in synthetic_samples.iterrows():
    result = process_sample(row)
    synth_results.append(result)
    print(f"\nSample {len(synth_results)}:")
    print(f"   Actual score: {result['actual']:.3f}")
    print(f"   XGBoost pred: {result['xgb']:.3f} (error: {abs(result['xgb']-result['actual']):.3f})")
    print(f"   RF pred:      {result['rf']:.3f} (error: {abs(result['rf']-result['actual']):.3f})")
    print(f"   Cosine sim:   {result['cos_sim']:.3f}")

print("\n" + "=" * 70)
print("🟢 ORIGINAL SAMPLES (Should predict HIGH ~0.66):")
print("=" * 70)

orig_results = []
for idx, row in original_samples.iterrows():
    result = process_sample(row)
    orig_results.append(result)
    print(f"\nSample {len(orig_results)}:")
    print(f"   Actual score: {result['actual']:.3f}")
    print(f"   XGBoost pred: {result['xgb']:.3f} (error: {abs(result['xgb']-result['actual']):.3f})")
    print(f"   RF pred:      {result['rf']:.3f} (error: {abs(result['rf']-result['actual']):.3f})")
    print(f"   Cosine sim:   {result['cos_sim']:.3f}")

# Summary
synth_xgb_avg = np.mean([r['xgb'] for r in synth_results])
synth_rf_avg = np.mean([r['rf'] for r in synth_results])
orig_xgb_avg = np.mean([r['xgb'] for r in orig_results])
orig_rf_avg = np.mean([r['rf'] for r in orig_results])

print("\n" + "=" * 70)
print("📊 SUMMARY:")
print("=" * 70)
print(f"\nSynthetic samples (actual avg: 0.14):")
print(f"   XGBoost predicted: {synth_xgb_avg:.3f}")
print(f"   Random Forest predicted: {synth_rf_avg:.3f}")

print(f"\nOriginal samples (actual avg: 0.66):")
print(f"   XGBoost predicted: {orig_xgb_avg:.3f}")
print(f"   Random Forest predicted: {orig_rf_avg:.3f}")

print(f"\n📈 Model discrimination on TRAINING data:")
print(f"   XGBoost gap: {abs(orig_xgb_avg - synth_xgb_avg):.3f}")
print(f"   Random Forest gap: {abs(orig_rf_avg - synth_rf_avg):.3f}")

if abs(orig_xgb_avg - synth_xgb_avg) < 0.1:
    print(f"\n❌ CRITICAL: Model predicts ~{orig_xgb_avg:.2f} for EVERYTHING!")
    print(f"   The model has NOT learned from the synthetic data at all.")
    print(f"   Solution: Model needs to be RETRAINED with sample weights.")
else:
    print(f"\n✅ Model CAN discriminate on training data!")
    print(f"   Issue is likely with test data format or model generalization.")
