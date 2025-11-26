"""
Matching Engine for Resume-Job Matching
Uses XGBoost semantic model for predictions
"""

import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


class MatchingEngine:
    """Resume-Job matching engine using hybrid XGBoost + Cosine similarity"""
    
    def __init__(self, model_path='xgboost_semantic.pkl', scaler_path='scaler_semantic.pkl', 
                 cosine_weight=0.6, xgb_weight=0.4):
        """
        Initialize matching engine
        
        Args:
            model_path: Path to trained XGBoost model
            scaler_path: Path to feature scaler
            cosine_weight: Weight for cosine similarity (default 0.6 = 60%)
            xgb_weight: Weight for XGBoost prediction (default 0.4 = 40%)
        """
        try:
            # Load models
            self.xgb_model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Set scoring weights
            self.cosine_weight = cosine_weight
            self.xgb_weight = xgb_weight
            assert abs(cosine_weight + xgb_weight - 1.0) < 0.01, "Weights must sum to 1.0"
            
            # Define domain keywords for penalty calculation
            self.domain_keywords = {
                'culinary': ['chef', 'cook', 'culinary', 'kitchen', 'food', 'menu', 'recipe', 'cuisine', 'restaurant', 'cooking', 'baking', 'pastry', 'catering'],
                'marketing': ['marketing', 'seo', 'sem', 'social media', 'google analytics', 'facebook ads', 'content marketing', 'email marketing', 'brand', 'campaign', 'digital marketing'],
                'technology': ['python', 'java', 'javascript', 'software', 'programming', 'developer', 'engineer', 'coding', 'machine learning', 'data science', 'sql', 'aws', 'cloud'],
                'healthcare': ['nurse', 'doctor', 'patient', 'medical', 'healthcare', 'clinical', 'hospital', 'nursing', 'physician', 'diagnosis', 'treatment'],
                'finance': ['accounting', 'finance', 'financial', 'audit', 'bookkeeping', 'tax', 'cpa', 'budget', 'investment', 'banking'],
            }
            
            print(f"✅ Matching engine loaded successfully")
            print(f"   Hybrid scoring: {self.cosine_weight*100:.0f}% Cosine + {self.xgb_weight*100:.0f}% XGBoost")
        except Exception as e:
            raise Exception(f"Failed to load matching models: {e}")
    
    def _detect_domain(self, text: str) -> str:
        """
        Detect the primary domain of a text based on keywords
        
        Args:
            text: Text to analyze
            
        Returns:
            Domain name or 'general'
        """
        text_lower = text.lower()
        domain_scores = {}
        
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            domain_scores[domain] = score
        
        max_score = max(domain_scores.values())
        if max_score >= 2:  # At least 2 keyword matches required
            return max(domain_scores, key=domain_scores.get)
        return 'general'
    
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
        
        # Get both scores
        xgb_score = self.xgb_model.predict(X_scaled)[0] * 100
        cosine_score = cos_sim * 100
        
        # Hybrid score: weighted combination
        base_score = (self.cosine_weight * cosine_score) + (self.xgb_weight * xgb_score)
        
        # Apply domain mismatch penalty
        resume_domain = self._detect_domain(resume_text)
        job_domain = self._detect_domain(job_text)
        
        # If domains are different and both are specific (not 'general'), apply penalty
        if resume_domain != 'general' and job_domain != 'general' and resume_domain != job_domain:
            penalty = 0.25  # 25% penalty for domain mismatch
            adjusted_score = base_score * (1 - penalty)
        else:
            adjusted_score = base_score
        
        return round(float(adjusted_score), 2)
    
    def get_match_category(self, score: float) -> str:
        """
        Categorize match score
        
        Args:
            score: Match score (0-100)
        
        Returns:
            Category string
        """
        if score >= 65:
            return "Shortlisted"
        else:
            return "Not Shortlisted"
