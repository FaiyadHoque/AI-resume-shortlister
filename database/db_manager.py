"""
Database module for AI Resume Shortlister
Handles all database operations for candidates, jobs, and match results
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Database:
    """SQLite database manager for resume shortlister"""

    def __init__(self, db_path: str = "database/resume_shortlister.db"):
        """Initialize database connection"""
        self.db_path = db_path
        # Create database directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_database()

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn

    def init_database(self):
        """Initialize database with schema"""
        schema_path = Path(__file__).parent / "schema.sql"

        with self.get_connection() as conn:
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
            conn.commit()

    # ==================== CANDIDATE OPERATIONS ====================

    def add_candidate(self, candidate_data: Dict) -> int:
        """
        Add a new candidate to database

        Args:
            candidate_data: Dictionary with candidate information

        Returns:
            ID of inserted candidate
        """
        query = """
            INSERT INTO candidates 
            (name, email, phone, objective, education, skills, 
             experience_years, experience_details, projects, certifications, 
             resume_text, resume_filename)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                candidate_data.get('name', ''),
                candidate_data.get('email', ''),
                candidate_data.get('phone', ''),
                candidate_data.get('objective', ''),
                candidate_data.get('education', ''),
                candidate_data.get('skills', ''),
                candidate_data.get('experience_years', 0),
                candidate_data.get('experience_details', ''),
                candidate_data.get('projects', ''),
                candidate_data.get('certifications', ''),
                candidate_data.get('resume_text', ''),
                candidate_data.get('resume_filename', '')
            ))
            conn.commit()
            return cursor.lastrowid

    def get_candidate(self, candidate_id: int) -> Optional[Dict]:
        """Get candidate by ID"""
        query = "SELECT * FROM candidates WHERE id = ?"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (candidate_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_candidates(self, limit: int = 100) -> List[Dict]:
        """Get all candidates"""
        query = "SELECT * FROM candidates ORDER BY created_at DESC LIMIT ?"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def search_candidates(self, search_term: str) -> List[Dict]:
        """Search candidates by name or email"""
        query = """
            SELECT * FROM candidates 
            WHERE name LIKE ? OR email LIKE ?
            ORDER BY created_at DESC
        """
        search_pattern = f"%{search_term}%"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (search_pattern, search_pattern))
            return [dict(row) for row in cursor.fetchall()]

    def delete_candidate(self, candidate_id: int):
        """Delete candidate and associated match results"""
        query = "DELETE FROM candidates WHERE id = ?"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (candidate_id,))
            conn.commit()

    # ==================== JOB POST OPERATIONS ====================

    def add_job_post(self, job_data: Dict) -> int:
        """
        Add a new job post to database

        Args:
            job_data: Dictionary with job information

        Returns:
            ID of inserted job post
        """
        query = """
            INSERT INTO job_posts 
            (title, company, location, job_type, description, 
             required_skills, required_education, required_experience_years, 
             salary_range, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                job_data.get('title', ''),
                job_data.get('company', ''),
                job_data.get('location', ''),
                job_data.get('job_type', ''),
                job_data.get('description', ''),
                job_data.get('required_skills', ''),
                job_data.get('required_education', ''),
                job_data.get('required_experience_years', 0),
                job_data.get('salary_range', ''),
                job_data.get('status', 'active')
            ))
            conn.commit()
            return cursor.lastrowid

    def get_job_post(self, job_id: int) -> Optional[Dict]:
        """Get job post by ID"""
        query = "SELECT * FROM job_posts WHERE id = ?"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_job_posts(self, status: str = 'active', limit: int = 100) -> List[Dict]:
        """Get all job posts"""
        if status == 'all':
            query = "SELECT * FROM job_posts ORDER BY created_at DESC LIMIT ?"
            params = (limit,)
        else:
            query = "SELECT * FROM job_posts WHERE status = ? ORDER BY created_at DESC LIMIT ?"
            params = (status, limit)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def update_job_status(self, job_id: int, status: str):
        """Update job post status"""
        query = "UPDATE job_posts SET status = ?, updated_at = ? WHERE id = ?"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (status, datetime.now(), job_id))
            conn.commit()

    def delete_job_post(self, job_id: int):
        """Delete job post and associated match results"""
        query = "DELETE FROM job_posts WHERE id = ?"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (job_id,))
            conn.commit()

    # ==================== MATCH RESULTS OPERATIONS ====================

    def save_match_result(self, candidate_id: int, job_id: int, match_score: float):
        """
        Save or update match result

        Args:
            candidate_id: Candidate ID
            job_id: Job ID
            match_score: Match score (0-1 scale)
        """
        # Determine match category
        score_percentage = match_score * 100
        if score_percentage >= 80:
            category = "Excellent"
        elif score_percentage >= 60:
            category = "Good"
        elif score_percentage >= 40:
            category = "Moderate"
        else:
            category = "Poor"

        query = """
            INSERT INTO match_results (candidate_id, job_id, match_score, match_category)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(candidate_id, job_id) 
            DO UPDATE SET 
                match_score = excluded.match_score,
                match_category = excluded.match_category,
                matched_at = CURRENT_TIMESTAMP
        """

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query, (candidate_id, job_id, match_score, category))
            conn.commit()

    def get_matches_for_job(self, job_id: int, min_score: float = 0.0) -> List[Dict]:
        """
        Get all candidate matches for a job, sorted by score

        Args:
            job_id: Job post ID
            min_score: Minimum match score filter

        Returns:
            List of matches with candidate details
        """
        query = """
            SELECT 
                m.id as match_id,
                m.match_score,
                m.match_category,
                m.matched_at,
                c.*
            FROM match_results m
            JOIN candidates c ON m.candidate_id = c.id
            WHERE m.job_id = ? AND m.match_score >= ?
            ORDER BY m.match_score DESC
        """

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (job_id, min_score))
            return [dict(row) for row in cursor.fetchall()]

    def get_matches_for_candidate(self, candidate_id: int, min_score: float = 0.0) -> List[Dict]:
        """
        Get all job matches for a candidate, sorted by score

        Args:
            candidate_id: Candidate ID
            min_score: Minimum match score filter

        Returns:
            List of matches with job details
        """
        query = """
            SELECT 
                m.id as match_id,
                m.match_score,
                m.match_category,
                m.matched_at,
                j.*
            FROM match_results m
            JOIN job_posts j ON m.job_id = j.id
            WHERE m.candidate_id = ? AND m.match_score >= ?
            ORDER BY m.match_score DESC
        """

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (candidate_id, min_score))
            return [dict(row) for row in cursor.fetchall()]

    def get_top_matches(self, limit: int = 10) -> List[Dict]:
        """Get top matches across all candidates and jobs"""
        query = """
            SELECT 
                m.match_score,
                m.match_category,
                m.matched_at,
                c.name as candidate_name,
                c.email as candidate_email,
                j.title as job_title,
                j.company as job_company
            FROM match_results m
            JOIN candidates c ON m.candidate_id = c.id
            JOIN job_posts j ON m.job_id = j.id
            ORDER BY m.match_score DESC
            LIMIT ?
        """

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    # ==================== STATISTICS ====================

    def get_statistics(self) -> Dict:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Count candidates
            cursor.execute("SELECT COUNT(*) FROM candidates")
            total_candidates = cursor.fetchone()[0]

            # Count jobs
            cursor.execute(
                "SELECT COUNT(*) FROM job_posts WHERE status = 'active'")
            active_jobs = cursor.fetchone()[0]

            # Count matches
            cursor.execute("SELECT COUNT(*) FROM match_results")
            total_matches = cursor.fetchone()[0]

            # Average match score
            cursor.execute("SELECT AVG(match_score) FROM match_results")
            avg_score = cursor.fetchone()[0] or 0

            return {
                'total_candidates': total_candidates,
                'active_jobs': active_jobs,
                'total_matches': total_matches,
                'average_match_score': avg_score
            }


# Singleton instance
_db_instance = None


def get_db() -> Database:
    """Get database singleton instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
