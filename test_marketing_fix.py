import pandas as pd
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# Load models from notebook variables (assuming notebook is still running)
print("Loading models from saved files...")

model = SentenceTransformer('all-MiniLM-L6-v2')

# Try loading with binary mode
with open('xgboost_semantic.pkl', 'rb') as f:
    xgb = pickle.load(f)
with open('random_forest_semantic.pkl', 'rb') as f:
    rf = pickle.load(f)
with open('scaler_semantic.pkl', 'rb') as f:
    scaler = pickle.load(f)

def predict(resume, job):
    """Predict match score for resume and job"""
    r = model.encode([resume])[0]
    j = model.encode([job])[0]
    
    cos = np.dot(r, j) / (np.linalg.norm(r) * np.linalg.norm(j))
    euc = np.linalg.norm(r - j)
    man = np.sum(np.abs(r - j))
    
    X = np.concatenate([r, j, [cos, euc, man]]).reshape(1, -1)
    X_scaled = scaler.transform(X)
    
    return xgb.predict(X_scaled)[0] * 100, rf.predict(X_scaled)[0] * 100, cos

# Load test files
ds = open('data_scientist_resume.txt', encoding='utf-8').read()
mk = open('marketing_manager_resume.txt', encoding='utf-8').read()
job = open('marketing_job.txt', encoding='utf-8').read()

print("\nTesting Data Scientist -> Marketing Job...")
xgb1, rf1, sim1 = predict(ds, job)

print("\nTesting Marketing Manager (NEW from original) -> Marketing Job...")
xgb2, rf2, sim2 = predict(mk, job)

print("\n" + "="*60)
print("RESULTS:")
print("="*60)
print(f'\nData Scientist -> Marketing Job:')
print(f'  XGBoost: {xgb1:.2f}, RF: {rf1:.2f}, Sim: {sim1:.3f}')

print(f'\nMarketing Manager (NEW from original) -> Marketing Job:')
print(f'  XGBoost: {xgb2:.2f}, RF: {rf2:.2f}, Sim: {sim2:.3f}')

print(f'\nDiscrimination:')
print(f'  XGBoost gap: {abs(xgb1-xgb2):.2f} points')
print(f'  RF gap: {abs(rf1-rf2):.2f} points')

print(f'\nExpected: DS<40 (mismatch), Marketing>60 (match)')
print("="*60)
