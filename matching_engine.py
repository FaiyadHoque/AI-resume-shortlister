"""
Matching engine that uses the trained XGBoost model to match candidates with jobs
"""

import pickle
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from database.db_manager import get_db


class MatchingEngine:
    """Match candidates with job posts using trained model"""

    def __init__(self):
        """Load trained model artifacts"""
        self.model = None
        self.vectorizer = None
        self.X_columns = None
        self.load_model()

    def load_model(self):
        """Load model, vectorizer, and feature columns"""
        try:
            with open('xgb_model.pkl', 'rb') as f:
                self.model = pickle.load(f)

            with open('tfidf_vectorizer.pkl', 'rb') as f:
                self.vectorizer = pickle.load(f)

            with open('X_columns.pkl', 'rb') as f:
                self.X_columns = pickle.load(f)

            print("✓ Matching model loaded successfully")
        except Exception as e:
            print(f"⚠ Error loading model: {e}")
            raise

    def prepare_features(self, resume_text: str, job_text: str) -> pd.DataFrame:
        """
        Prepare features for model prediction

        Args:
            resume_text: Full resume text
            job_text: Full job description text

        Returns:
            Feature DataFrame ready for prediction
        """
        # Combine texts for TF-IDF
        combined_text = f"{resume_text} {job_text}"

        # Transform using TF-IDF vectorizer
        tfidf_features = self.vectorizer.transform([combined_text])

        # Convert to DataFrame
        feature_df = pd.DataFrame(
            tfidf_features.toarray(),
            columns=[f'tfidf_{i}' for i in range(tfidf_features.shape[1])]
        )

        # Add any missing columns with zeros
        for col in self.X_columns:
            if col not in feature_df.columns:
                feature_df[col] = 0

        # Ensure columns are in the same order as training
        feature_df = feature_df[self.X_columns]

        return feature_df

    def predict_match(self, resume_text: str, job_text: str) -> float:
        """
        Predict match score between resume and job

        Args:
            resume_text: Resume text
            job_text: Job description text

        Returns:
            Match score (0-1 scale)
        """
        features = self.prepare_features(resume_text, job_text)
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

        # Predict match score
        score = self.predict_match(resume_text, job_text)

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
