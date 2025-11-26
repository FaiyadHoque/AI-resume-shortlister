"""
Comprehensive Test: Match Different Resumes with Different Job Descriptions
Tests all resume-job combinations to evaluate the matching system
"""
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import os

print("=" * 80)
print("🎯 RESUME-JOB MATCHING TEST")
print("=" * 80)

# Load models
print("\n📦 Loading models...")
try:
    xgb_model = joblib.load('xgboost_semantic.pkl')
    rf_model = joblib.load('random_forest_semantic.pkl')
    scaler = joblib.load('scaler_semantic.pkl')
    semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Models loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    exit(1)

# Define test files
RESUME_FILES = {
    'Data Scientist': 'data_scientist_resume.txt',
    'Marketing Manager': 'marketing_manager_resume.txt',
    'Chef': 'chef_resume.txt'
}

JOB_FILES = {
    'Data Science': 'data_science_job.txt',
    'Marketing': 'marketing_job.txt'
}

def read_file(filename):
    """Read text file content"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"⚠️  File not found: {filename}")
        return None
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
        return None

def calculate_match_score(resume_text, job_text):
    """Calculate match score between resume and job description"""
    # Generate embeddings
    resume_emb = semantic_model.encode([resume_text])[0]
    job_emb = semantic_model.encode([job_text])[0]
    
    # Calculate similarity features
    cos_sim = cosine_similarity([resume_emb], [job_emb])[0][0]
    euc_dist = euclidean_distances([resume_emb], [job_emb])[0][0]
    man_dist = np.sum(np.abs(resume_emb - job_emb))
    
    # Combine features
    X = np.concatenate([resume_emb, job_emb, [cos_sim, euc_dist, man_dist]])
    X_scaled = scaler.transform([X])
    
    # Get predictions from both models
    xgb_score = xgb_model.predict(X_scaled)[0]
    rf_score = rf_model.predict(X_scaled)[0]
    
    # Average the predictions
    avg_score = (xgb_score + rf_score) / 2
    
    return {
        'xgboost': xgb_score,
        'random_forest': rf_score,
        'average': avg_score,
        'cosine_similarity': cos_sim
    }

def interpret_score(score):
    """Interpret the matching score"""
    if score >= 0.7:
        return "🟢 Excellent Match"
    elif score >= 0.5:
        return "🟡 Good Match"
    elif score >= 0.3:
        return "🟠 Moderate Match"
    else:
        return "🔴 Poor Match"

# Load all resume and job texts
print("\n📄 Loading files...")
resumes = {}
jobs = {}

for resume_name, filename in RESUME_FILES.items():
    content = read_file(filename)
    if content:
        resumes[resume_name] = content
        print(f"   ✅ {resume_name} resume loaded")

for job_name, filename in JOB_FILES.items():
    content = read_file(filename)
    if content:
        jobs[job_name] = content
        print(f"   ✅ {job_name} job description loaded")

# Test all combinations
print("\n" + "=" * 80)
print("🔍 TESTING ALL RESUME-JOB COMBINATIONS")
print("=" * 80)

results = []

for resume_name, resume_text in resumes.items():
    for job_name, job_text in jobs.items():
        print(f"\n{'─' * 80}")
        print(f"📋 Resume: {resume_name}")
        print(f"💼 Job: {job_name}")
        print(f"{'─' * 80}")
        
        scores = calculate_match_score(resume_text, job_text)
        
        print(f"\n📊 Matching Scores:")
        print(f"   XGBoost:           {scores['xgboost']:.3f}")
        print(f"   Random Forest:     {scores['random_forest']:.3f}")
        print(f"   Average:           {scores['average']:.3f}")
        print(f"   Cosine Similarity: {scores['cosine_similarity']:.3f}")
        print(f"\n   {interpret_score(scores['average'])}")
        
        results.append({
            'resume': resume_name,
            'job': job_name,
            'score': scores['average'],
            'xgb': scores['xgboost'],
            'rf': scores['random_forest'],
            'cos_sim': scores['cosine_similarity']
        })

# Summary report
print("\n" + "=" * 80)
print("📈 SUMMARY REPORT")
print("=" * 80)

# Sort by score
results_sorted = sorted(results, key=lambda x: x['score'], reverse=True)

print("\n🏆 Rankings (Best to Worst):")
for i, result in enumerate(results_sorted, 1):
    print(f"\n{i}. {result['resume']} → {result['job']}")
    print(f"   Score: {result['score']:.3f} {interpret_score(result['score'])}")

# Expected matches analysis
print("\n" + "=" * 80)
print("🎯 EXPECTED MATCHES ANALYSIS")
print("=" * 80)

expected_matches = [
    ('Data Scientist', 'Data Science'),
    ('Marketing Manager', 'Marketing')
]

print("\nExpected good matches:")
for resume, job in expected_matches:
    match = next((r for r in results if r['resume'] == resume and r['job'] == job), None)
    if match:
        print(f"   {resume} → {job}: {match['score']:.3f} {interpret_score(match['score'])}")

print("\nExpected poor matches:")
poor_matches = [
    ('Chef', 'Data Science'),
    ('Chef', 'Marketing'),
    ('Data Scientist', 'Marketing'),
    ('Marketing Manager', 'Data Science')
]

for resume, job in poor_matches:
    match = next((r for r in results if r['resume'] == resume and r['job'] == job), None)
    if match:
        print(f"   {resume} → {job}: {match['score']:.3f} {interpret_score(match['score'])}")

print("\n" + "=" * 80)
print("✅ TEST COMPLETE")
print("=" * 80)
