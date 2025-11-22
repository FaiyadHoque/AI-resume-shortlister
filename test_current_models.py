"""
Test the trained models with the sample files
"""
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

print("=" * 70)
print("🧪 TESTING TRAINED MODELS")
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
    good_resume = f.read()
with open('marketing_manager_resume.txt', 'r') as f:
    bad_resume = f.read()
with open('data_science_job.txt', 'r') as f:
    job_desc = f.read()

# Generate embeddings
print("🧠 Generating embeddings...")
good_resume_emb = semantic_model.encode([good_resume])[0]
bad_resume_emb = semantic_model.encode([bad_resume])[0]
job_emb = semantic_model.encode([job_desc])[0]

# Calculate similarities for good match
cos_sim_good = cosine_similarity([good_resume_emb], [job_emb])[0][0]
euc_dist_good = euclidean_distances([good_resume_emb], [job_emb])[0][0]
man_dist_good = np.sum(np.abs(good_resume_emb - job_emb))

# Calculate similarities for bad match
cos_sim_bad = cosine_similarity([bad_resume_emb], [job_emb])[0][0]
euc_dist_bad = euclidean_distances([bad_resume_emb], [job_emb])[0][0]
man_dist_bad = np.sum(np.abs(bad_resume_emb - job_emb))

# Create feature vectors
X_good = np.concatenate([good_resume_emb, job_emb, [cos_sim_good, euc_dist_good, man_dist_good]])
X_bad = np.concatenate([bad_resume_emb, job_emb, [cos_sim_bad, euc_dist_bad, man_dist_bad]])

# Scale and predict
X_good_scaled = scaler.transform([X_good])
X_bad_scaled = scaler.transform([X_bad])

xgb_good_score = xgb_model.predict(X_good_scaled)[0] * 100
xgb_bad_score = xgb_model.predict(X_bad_scaled)[0] * 100

rf_good_score = rf_model.predict(X_good_scaled)[0] * 100
rf_bad_score = rf_model.predict(X_bad_scaled)[0] * 100

print("\n" + "=" * 70)
print("🎯 CURRENT MODEL PERFORMANCE")
print("=" * 70)

print("\nXGBoost Model:")
print(f"  ✅ Data Scientist → Data Science Job: {xgb_good_score:.2f}/100")
print(f"  ❌ Marketing Manager → Data Science Job: {xgb_bad_score:.2f}/100")
print(f"  📊 Discrimination Power: {abs(xgb_good_score - xgb_bad_score):.2f} points")

print("\nRandom Forest Model:")
print(f"  ✅ Data Scientist → Data Science Job: {rf_good_score:.2f}/100")
print(f"  ❌ Marketing Manager → Data Science Job: {rf_bad_score:.2f}/100")
print(f"  📊 Discrimination Power: {abs(rf_good_score - rf_bad_score):.2f} points")

print("\n" + "=" * 70)

# Semantic similarity analysis
print(f"\n📊 Semantic Similarity Analysis:")
print(f"   Data Scientist <→> Job: {cos_sim_good:.4f} (cosine similarity)")
print(f"   Marketing <→> Job:      {cos_sim_bad:.4f} (cosine similarity)")
print(f"   Raw embedding difference: {cos_sim_good - cos_sim_bad:.4f}")

if abs(xgb_good_score - xgb_bad_score) > 20:
    print("\n✅ SUCCESS! Model can discriminate!")
else:
    print("\n❌ PROBLEM: Model still cannot discriminate properly")
    print("\nPossible issues:")
    print("  1. Semantic embeddings are too similar (check cosine similarity above)")
    print("  2. Need MORE synthetic negative samples (currently 1000)")
    print("  3. Synthetic samples may need lower scores (< 0.20)")
