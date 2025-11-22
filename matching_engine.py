"""
Matching engine that uses the trained XGBoost model to match candidates with jobs
"""

import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sentence_transformers import SentenceTransformer
from database.db_manager import get_db


class MatchingEngine:
    """Match candidates with job posts using trained semantic model"""

    def __init__(self):
        """Load trained model artifacts"""
        self.model = None
        self.scaler = None
        self.embedder = None
        self.load_model()

    def load_model(self):
        """Load semantic model, scaler, and sentence transformer"""
        try:
            # Load XGBoost semantic model
            self.model = joblib.load('xgboost_semantic.pkl')

            # Load feature scaler
            self.scaler = joblib.load('scaler_semantic.pkl')

            # Load sentence transformer for embeddings
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

            print("✓ Semantic matching model loaded successfully")
        except Exception as e:
            print(f"⚠ Error loading semantic model: {e}")
            raise

    def prepare_features(self, resume_text: str, job_text: str, experience_years: float = 0.0) -> np.ndarray:
        """
        Prepare semantic features for model prediction

        Args:
            resume_text: Full resume text
            job_text: Full job description text
            experience_years: Years of experience (default 0 if not provided)

        Returns:
            Scaled feature array ready for prediction
        """
        # Generate embeddings for resume and job
        resume_embedding = self.embedder.encode(resume_text, convert_to_numpy=True)
        job_embedding = self.embedder.encode(job_text, convert_to_numpy=True)

        # Calculate cosine similarity between resume and job
        from sklearn.metrics.pairwise import cosine_similarity
        similarity = cosine_similarity(
            resume_embedding.reshape(1, -1),
            job_embedding.reshape(1, -1)
        )[0][0]

        # Calculate text length ratio
        text_length_ratio = len(resume_text) / (len(job_text) + 1)

        # Combine all features: resume_embedding + job_embedding + numerical features
        combined_features = np.concatenate([
            resume_embedding, 
            job_embedding,
            [experience_years, similarity, text_length_ratio]
        ])

        # Reshape for single sample
        combined_features = combined_features.reshape(1, -1)

        # Scale features using the trained scaler
        scaled_features = self.scaler.transform(combined_features)

        return scaled_features

    def predict_match(self, resume_text: str, job_text: str, experience_years: float = 0.0) -> float:
        """
        Predict match score between resume and job using semantic similarity

        Args:
            resume_text: Resume text
            job_text: Job description text
            experience_years: Years of experience (default 0 if not provided)

        Returns:
            Match score (0-1 scale)
        """
        features = self.prepare_features(resume_text, job_text, experience_years)
        score = self.model.predict(features)[0]

        # Clip to valid range
        score = np.clip(score, 0, 1)

        return float(score)

    def match_candidate_with_job(self, candidate_id: int, job_id: int) -> Dict:
        """
        Match a specific candidate with a specific job and save result

        Args:
            candidate_id: Candidate ID
            job_id: Job post ID

        Returns:
            Match result dictionary
        """
        db = get_db()

        # Get candidate and job data
        candidate = db.get_candidate(candidate_id)
        job = db.get_job_post(job_id)

        if not candidate or not job:
            raise ValueError("Candidate or job not found")

        # Prepare texts for matching
        resume_text = self._build_resume_text(candidate)
        job_text = self._build_job_text(job)

        # Extract experience years (default to 0 if not available)
        experience_years = float(candidate.get('experience_years', 0) or 0)

        # Predict match score
        score = self.predict_match(resume_text, job_text, experience_years)

        # Save to database
        db.save_match_result(candidate_id, job_id, score)

        # Determine category
        score_percentage = score * 100
        if score_percentage >= 80:
            category = "Excellent"
        elif score_percentage >= 60:
            category = "Good"
        elif score_percentage >= 40:
            category = "Moderate"
        else:
            category = "Poor"

        return {
            'candidate_id': candidate_id,
            'candidate_name': candidate.get('name'),
            'job_id': job_id,
            'job_title': job.get('title'),
            'match_score': score,
            'match_category': category,
            'score_percentage': score_percentage
        }

    def match_candidate_with_all_jobs(self, candidate_id: int) -> List[Dict]:
        """
        Match a candidate with all active jobs

        Args:
            candidate_id: Candidate ID

        Returns:
            List of match results sorted by score
        """
        db = get_db()

        # Get all active jobs
        jobs = db.get_all_job_posts(status='active')

        results = []
        for job in jobs:
            try:
                result = self.match_candidate_with_job(candidate_id, job['id'])
                results.append(result)
            except Exception as e:
                print(
                    f"Error matching candidate {candidate_id} with job {job['id']}: {e}")

        # Sort by score descending
        results.sort(key=lambda x: x['match_score'], reverse=True)

        return results

    def match_job_with_all_candidates(self, job_id: int) -> List[Dict]:
        """
        Match a job with all candidates

        Args:
            job_id: Job post ID

        Returns:
            List of match results sorted by score
        """
        db = get_db()

        # Get all candidates
        candidates = db.get_all_candidates()

        results = []
        for candidate in candidates:
            try:
                result = self.match_candidate_with_job(candidate['id'], job_id)
                results.append(result)
            except Exception as e:
                print(
                    f"Error matching job {job_id} with candidate {candidate['id']}: {e}")

        # Sort by score descending
        results.sort(key=lambda x: x['match_score'], reverse=True)

        return results

    def match_all(self, min_score: float = 0.0) -> List[Dict]:
        """
        Match all candidates with all jobs

        Args:
            min_score: Minimum score threshold

        Returns:
            List of all match results
        """
        db = get_db()

        candidates = db.get_all_candidates()
        jobs = db.get_all_job_posts(status='active')

        results = []
        total = len(candidates) * len(jobs)
        count = 0

        for candidate in candidates:
            for job in jobs:
                count += 1
                try:
                    result = self.match_candidate_with_job(
                        candidate['id'], job['id'])
                    if result['match_score'] >= min_score:
                        results.append(result)

                    if count % 10 == 0:
                        print(f"Progress: {count}/{total} matches completed")

                except Exception as e:
                    print(f"Error in matching: {e}")

        # Sort by score descending
        results.sort(key=lambda x: x['match_score'], reverse=True)

        return results

    def _build_resume_text(self, candidate: Dict) -> str:
        """Build comprehensive text from candidate data"""
        parts = [
            candidate.get('objective', ''),
            candidate.get('education', ''),
            candidate.get('skills', ''),
            candidate.get('experience_details', ''),
            candidate.get('projects', ''),
            candidate.get('certifications', ''),
            candidate.get('resume_text', '')
        ]
        return ' '.join(p for p in parts if p)

    def _build_job_text(self, job: Dict) -> str:
        """Build comprehensive text from job data"""
        parts = [
            job.get('title', ''),
            job.get('description', ''),
            job.get('required_skills', ''),
            job.get('required_education', '')
        ]
        return ' '.join(p for p in parts if p)


# Singleton instance
_engine_instance = None


def get_matching_engine() -> MatchingEngine:
    """Get matching engine singleton instance"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = MatchingEngine()
    return _engine_instance
