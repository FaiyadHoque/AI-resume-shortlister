"""
Matching Engine for Resume-Job Matching
Uses XGBoost semantic model for predictions
"""

import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


class MatchingEngine:
    """Resume-Job matching engine using trained XGBoost model"""
    
    def __init__(self, model_path='xgboost_semantic.pkl', scaler_path='scaler_semantic.pkl'):
        """
        Initialize matching engine
        
        Args:
            model_path: Path to trained XGBoost model
            scaler_path: Path to feature scaler
        """
        try:
            # Load models
            self.xgb_model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
            print(f"✅ Matching engine loaded successfully")
        except Exception as e:
            raise Exception(f"Failed to load matching models: {e}")
    
    def predict_match(self, resume_text: str, job_text: str) -> float:
        """
        Predict match score between resume and job
        
        Args:
            resume_text: Resume text (model-ready format from cnvrt.py)
            job_text: Job description text (model-ready format from cnvrt.py)
        
        Returns:
            Match score as percentage (0-100)
        """
        # Generate embeddings
        resume_emb = self.semantic_model.encode([resume_text])[0]
        job_emb = self.semantic_model.encode([job_text])[0]
        
        # Calculate similarity metrics
        cos_sim = cosine_similarity([resume_emb], [job_emb])[0][0]
        euc_dist = euclidean_distances([resume_emb], [job_emb])[0][0]
        man_dist = np.sum(np.abs(resume_emb - job_emb))
        
        # Create feature vector (384 + 384 + 3 = 771 features)
        X = np.concatenate([resume_emb, job_emb, [cos_sim, euc_dist, man_dist]])
        X_scaled = self.scaler.transform([X])
        
        # Predict
        score = self.xgb_model.predict(X_scaled)[0] * 100
        
        return round(float(score), 2)
    
    def get_match_category(self, score: float) -> str:
        """
        Categorize match score
        
        Args:
            score: Match score (0-100)
        
        Returns:
            Category string
        """
        if score >= 70:
            return "Excellent"
        elif score >= 55:
            return "Good"
        elif score >= 40:
            return "Moderate"
        else:
            return "Poor"
