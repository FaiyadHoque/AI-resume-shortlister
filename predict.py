"""
AI Resume-Job Matcher - Prediction Script
==========================================
Load trained models and predict resume-job match scores.

Usage:
    python predict.py --resume "resume.txt" --job "job.txt"

Or programmatically:
    from predict import ResumeJobMatcher
    matcher = ResumeJobMatcher()
    score = matcher.predict(resume_text, job_text)
"""

import joblib
import json
import pandas as pd
import numpy as np
import re
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')


class ResumeJobMatcher:
    """AI-powered Resume-Job Matching System"""

    def __init__(self, model_type='xgboost'):
        """
        Initialize the matcher with trained models.

        Args:
            model_type: 'xgboost' or 'random_forest'
        """
        print("🔄 Loading AI Resume-Job Matcher...")

        # Load models and components
        if model_type == 'xgboost':
            self.model = joblib.load('xgboost_model.pkl')
        else:
            self.model = joblib.load('random_forest_model.pkl')

        self.resume_vectorizer = joblib.load('resume_vectorizer.pkl')
        self.job_vectorizer = joblib.load('job_vectorizer.pkl')
        self.scaler = joblib.load('feature_scaler.pkl')

        # Load metadata
        with open('model_metadata.json', 'r') as f:
            self.metadata = json.load(f)

        print(f"✅ Loaded {model_type} model")
        print(f"📊 Model trained on {self.metadata['dataset_size']} samples")
        print(f"🎯 Test R²: {self.metadata['models'][model_type.replace('_', '')]['test_r2']:.4f}")

    def clean_text(self, text):
        """Clean and preprocess text"""
        if pd.isna(text) or text == '' or text == 'N/A':
            return ''

        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = ' '.join(text.split())

        return text

    def extract_features(self, resume_text, job_text):
        """Extract all features from resume and job text"""

        # Clean text
        resume_clean = self.clean_text(resume_text)
        job_clean = self.clean_text(job_text)

        # TF-IDF features
        resume_tfidf = self.resume_vectorizer.transform([resume_clean]).toarray()[0]
        job_tfidf = self.job_vectorizer.transform([job_clean]).toarray()[0]

        # TF-IDF similarity
        tfidf_similarity = cosine_similarity(
            resume_tfidf.reshape(1, -1),
            job_tfidf.reshape(1, -1)
        )[0][0]

        # Combine all features
        features = np.concatenate([
            resume_tfidf,
            job_tfidf,
            [tfidf_similarity]
        ])

        return features.reshape(1, -1)

    def predict(self, resume_text, job_text):
        """
        Predict match score between resume and job description.

        Args:
            resume_text: Full resume text (string)
            job_text: Full job description text (string)

        Returns:
            float: Predicted match score (0-100)
        """
        # Extract features
        features = self.extract_features(resume_text, job_text)

        # Scale features
        features_scaled = self.scaler.transform(features)

        # Predict
        score = self.model.predict(features_scaled)[0]

        # Clip to valid range
        score = np.clip(score, 0, 100)

        return score

    def predict_batch(self, resume_job_pairs):
        """
        Predict match scores for multiple resume-job pairs.

        Args:
            resume_job_pairs: List of (resume_text, job_text) tuples

        Returns:
            list: Predicted match scores
        """
        scores = []
        for resume_text, job_text in resume_job_pairs:
            score = self.predict(resume_text, job_text)
            scores.append(score)
        return scores


def main():
    """Command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description='AI Resume-Job Matcher')
    parser.add_argument('--resume', required=True, help='Path to resume text file')
    parser.add_argument('--job', required=True, help='Path to job description text file')
    parser.add_argument('--model', default='xgboost', choices=['xgboost', 'random_forest'],
                       help='Model to use (default: xgboost)')

    args = parser.parse_args()

    # Read files
    with open(args.resume, 'r', encoding='utf-8') as f:
        resume_text = f.read()

    with open(args.job, 'r', encoding='utf-8') as f:
        job_text = f.read()

    # Initialize matcher and predict
    matcher = ResumeJobMatcher(model_type=args.model)
    score = matcher.predict(resume_text, job_text)

    print(f"\n{'='*60}")
    print(f"MATCH SCORE: {score:.2f}/100")
    print(f"{'='*60}")

    if score >= 80:
        print("🟢 Excellent Match - Highly Recommended")
    elif score >= 60:
        print("🟡 Good Match - Recommended")
    elif score >= 40:
        print("🟠 Moderate Match - Consider with caution")
    else:
        print("🔴 Poor Match - Not Recommended")


if __name__ == "__main__":
    main()
