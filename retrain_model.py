"""
Retrain the resume matching model with FIXED feature engineering.
This script corrects the categorical encoding issue.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle

print("="*80)
print("RETRAINING MODEL WITH FIXED FEATURE ENGINEERING")
print("="*80)
print()

# Load cleaned data
print("Loading cleaned_resume_data.csv...")
cleaned_df = pd.read_csv('cleaned_resume_data.csv')
print(f"✓ Loaded {len(cleaned_df)} records")
print()

# Prepare combined text for TF-IDF
print("Creating combined text field...")
if 'combined_text' not in cleaned_df.columns:
    cleaned_df['combined_text'] = (
        cleaned_df['career_objective'].fillna('') + ' ' + 
        cleaned_df['skills'].fillna('') + ' ' + 
        cleaned_df['responsibilities'].fillna('')
    )
print("✓ Combined text created")
print()

# Apply TF-IDF
print("Applying TF-IDF vectorization...")
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
tfidf_matrix = tfidf_vectorizer.fit_transform(cleaned_df['combined_text'])
print(f"✓ TF-IDF matrix shape: {tfidf_matrix.shape}")
print()

# Prepare features and target
y = cleaned_df['matched_score']
X = cleaned_df.drop('matched_score', axis=1)

# FIXED: Only encode truly categorical columns
print("Identifying categorical features to encode...")
categorical_cols = ['﻿job_position_name', 'educationaL_requirements', 'experiencere_requirement']
categorical_cols = [col for col in categorical_cols if col in X.columns]
print(f"✓ Categorical columns: {categorical_cols}")
print()

# One-hot encode ONLY the categorical columns
print("One-hot encoding categorical features...")
X_categorical = pd.get_dummies(X[categorical_cols], dummy_na=False)
X_categorical.index = cleaned_df.index
print(f"✓ Categorical features: {X_categorical.shape[1]} columns")
print()

# Combine categorical and TF-IDF features
print("Combining features...")
X_tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=cleaned_df.index)
# Convert column names to strings to avoid reindex issues later
X_tfidf_df.columns = [str(c) for c in X_tfidf_df.columns]
X_processed = pd.concat([X_categorical, X_tfidf_df], axis=1)
print(f"✓ Total features: {X_processed.shape[1]} columns")
print(f"  - Categorical: {X_categorical.shape[1]}")
print(f"  - TF-IDF: {X_tfidf_df.shape[1]}")
print()

# Clean column names (remove special characters)
print("Cleaning column names...")
X_processed.columns = [str(col).replace('[','').replace(']','').replace('<','') for col in X_processed.columns]
print("✓ Column names cleaned")
print()

# Train/test split
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
print(f"✓ Training set: {X_train.shape}")
print(f"✓ Test set: {X_test.shape}")
print()

# Train model
print("Training XGBoost model...")
xgb_model = XGBRegressor(random_state=42)
xgb_model.fit(X_train, y_train)
print("✓ Model trained!")
print()

# Evaluate
print("Evaluating model...")
y_train_pred = xgb_model.predict(X_train)
y_test_pred = xgb_model.predict(X_test)

mse_train = mean_squared_error(y_train, y_train_pred)
rmse_train = np.sqrt(mse_train)
mae_train = mean_absolute_error(y_train, y_train_pred)
r2_train = r2_score(y_train, y_train_pred)

mse_test = mean_squared_error(y_test, y_test_pred)
rmse_test = np.sqrt(mse_test)
mae_test = mean_absolute_error(y_test, y_test_pred)
r2_test = r2_score(y_test, y_test_pred)

print("Training Set Metrics:")
print(f"  MSE: {mse_train:.4f}")
print(f"  RMSE: {rmse_train:.4f}")
print(f"  MAE: {mae_train:.4f}")
print(f"  R-squared: {r2_train:.4f}")

print("\nTest Set Metrics:")
print(f"  MSE: {mse_test:.4f}")
print(f"  RMSE: {rmse_test:.4f}")
print(f"  MAE: {mae_test:.4f}")
print(f"  R-squared: {r2_test:.4f}")
print()

# Save artifacts
print("Saving model artifacts...")
with open('xgb_model.pkl', 'wb') as f:
    pickle.dump(xgb_model, f)
print("✓ Saved: xgb_model.pkl")

with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf_vectorizer, f)
print("✓ Saved: tfidf_vectorizer.pkl")

with open('X_columns.pkl', 'wb') as f:
    pickle.dump(list(X_processed.columns), f)
print("✓ Saved: X_columns.pkl")

print()
print("="*80)
print("RETRAINING COMPLETE!")
print("="*80)
print(f"New model has {len(X_processed.columns)} features:")
print(f"  - {X_categorical.shape[1]} categorical features (job position, education, experience)")
print(f"  - {X_tfidf_df.shape[1]} TF-IDF features (from combined text)")
print()
print("Old model had 6,122 features (incorrectly encoded free-text fields)")
print(f"New model has {len(X_processed.columns)} features (correctly engineered)")
print()
print("Next step: Run test_model.py to test with sample resumes")
