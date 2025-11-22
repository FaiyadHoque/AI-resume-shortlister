"""
Test all three resumes against the data science job
"""
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

print("=" * 70)
print("🧪 TESTING ALL RESUMES")
print("=" * 70)

# Load trained models
print("\n📦 Loading trained models...")
xgb_model = joblib.load('xgboost_semantic.pkl')
rf_model = joblib.load('random_forest_semantic.pkl')
scaler = joblib.load('scaler_semantic.pkl')
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Models loaded\n")

# Load test files
print("📄 Loading test resumes and job...")
with open('data_scientist_resume.txt', 'r') as f:
    data_scientist = f.read()
with open('marketing_manager_resume.txt', 'r') as f:
    marketing = f.read()
with open('chef_resume.txt', 'r') as f:
    chef = f.read()
with open('data_science_job.txt', 'r') as f:
    job_desc = f.read()

print("✅ Loaded all test files\n")

# Function to predict match score
def predict_match(resume_text, job_text, resume_name):
    # Generate embeddings
    resume_emb = semantic_model.encode([resume_text])[0]
    job_emb = semantic_model.encode([job_text])[0]
    
    # Calculate similarities
    cos_sim = cosine_similarity([resume_emb], [job_emb])[0][0]
    euc_dist = euclidean_distances([resume_emb], [job_emb])[0][0]
    man_dist = np.sum(np.abs(resume_emb - job_emb))
    
    # Create feature vector
    X = np.concatenate([resume_emb, job_emb, [cos_sim, euc_dist, man_dist]])
    X_scaled = scaler.transform([X])
    
    # Predict with both models
    xgb_score = xgb_model.predict(X_scaled)[0] * 100
    rf_score = rf_model.predict(X_scaled)[0] * 100
    
    return {
        'name': resume_name,
        'xgb': xgb_score,
        'rf': rf_score,
        'cos_sim': cos_sim
    }

# Test all resumes
print("🧠 Generating predictions...\n")
results = [
    predict_match(data_scientist, job_desc, "Data Scientist"),
    predict_match(marketing, job_desc, "Marketing Manager"),
    predict_match(chef, job_desc, "Chef")
]

# Display results
print("=" * 70)
print("🎯 TEST RESULTS: Resume → Data Science Job")
print("=" * 70)

print("\n📊 XGBoost Model:")
for r in results:
    emoji = "✅" if r['xgb'] > 60 else "⚠️" if r['xgb'] > 40 else "❌"
    print(f"   {emoji} {r['name']:20s} → {r['xgb']:5.2f}/100  (similarity: {r['cos_sim']:.3f})")

print("\n📊 Random Forest Model:")
for r in results:
    emoji = "✅" if r['rf'] > 60 else "⚠️" if r['rf'] > 40 else "❌"
    print(f"   {emoji} {r['name']:20s} → {r['rf']:5.2f}/100  (similarity: {r['cos_sim']:.3f})")

# Calculate discrimination
print("\n" + "=" * 70)
print("📈 DISCRIMINATION ANALYSIS")
print("=" * 70)

print("\nXGBoost Discrimination:")
print(f"   Data Scientist vs Marketing: {abs(results[0]['xgb'] - results[1]['xgb']):.2f} points")
print(f"   Data Scientist vs Chef:      {abs(results[0]['xgb'] - results[2]['xgb']):.2f} points")
print(f"   Marketing vs Chef:           {abs(results[1]['xgb'] - results[2]['xgb']):.2f} points")

print("\nRandom Forest Discrimination:")
print(f"   Data Scientist vs Marketing: {abs(results[0]['rf'] - results[1]['rf']):.2f} points")
print(f"   Data Scientist vs Chef:      {abs(results[0]['rf'] - results[2]['rf']):.2f} points")
print(f"   Marketing vs Chef:           {abs(results[1]['rf'] - results[2]['rf']):.2f} points")

# Success check
xgb_gap_chef = abs(results[0]['xgb'] - results[2]['xgb'])
rf_gap_chef = abs(results[0]['rf'] - results[2]['rf'])

print("\n" + "=" * 70)
if xgb_gap_chef > 20 and rf_gap_chef > 20:
    print("✅ SUCCESS! Both models discriminate well (>20 points)")
elif xgb_gap_chef > 20 or rf_gap_chef > 20:
    print("⚠️  PARTIAL: One model discriminates well")
else:
    print("❌ NEEDS IMPROVEMENT: Discrimination < 20 points")
print("=" * 70)
