"""
Database module for AI Resume Shortlister
Handles all database operations for candidates, jobs, and match results
"""

import sqlite3
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import wraps


def retry_on_lock(max_retries=10, delay=0.1):
    """Decorator to retry database operations on lock"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    if 'locked' in str(e).lower() and attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))
                        continue
                    raise
            return func(*args, **kwargs)
        return wrapper
    return decorator


class Database:
    """SQLite database manager for resume shortlister with connection pooling"""

    _instance = None
    _lock = threading.Lock()
    _connection = None

    def __new__(cls, db_path: str = "database/resume_shortlister.db"):
        """Singleton pattern to ensure only one database instance"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path: str = "database/resume_shortlister.db"):
        """Initialize database connection"""
        # Only initialize once
        if not hasattr(self, '_initialized'):
            self.db_path = db_path
            # Create database directory if it doesn't exist
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            self._connection_lock = threading.RLock()
            self._initialize_connection()
            self.init_database()
            self._initialized = True

    def _initialize_connection(self):
        """Initialize persistent database connection"""
        if self._connection is None:
            self._connection = sqlite3.connect(
                self.db_path,
                timeout=120.0,  # 2 minutes timeout
                check_same_thread=False,
                isolation_level=None  # Autocommit mode
            )
            self._connection.row_factory = sqlite3.Row
            # Disable WAL mode - use DELETE journal mode for better compatibility
            self._connection.execute('PRAGMA journal_mode=DELETE')
            self._connection.execute('PRAGMA busy_timeout=120000')
            self._connection.execute('PRAGMA synchronous=FULL')  # Safer writes
            self._connection.execute('PRAGMA cache_size=10000')
            self._connection.execute('PRAGMA temp_store=MEMORY')
            self._connection.execute('PRAGMA locking_mode=NORMAL')

    def get_connection(self) -> sqlite3.Connection:
        """Get the persistent database connection"""
        with self._connection_lock:
            if self._connection is None:
                self._initialize_connection()
            return self._connection

    def execute_query(self, query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False):
        """Execute query with proper locking"""
        with self._connection_lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if fetch_one:
                result = cursor.fetchone()
                return dict(result) if result else None
            elif fetch_all:
                return [dict(row) for row in cursor.fetchall()]
            else:
                return cursor.lastrowid

    def init_database(self):
        """Initialize database with schema"""
        schema_path = Path(__file__).parent / "schema.sql"

        with self._connection_lock:
            conn = self.get_connection()
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())

    # ==================== CANDIDATE OPERATIONS ====================

    @retry_on_lock(max_retries=10, delay=0.1)
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

        return self.execute_query(query, (
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

    @retry_on_lock(max_retries=10, delay=0.1)
    def get_candidate(self, candidate_id: int) -> Optional[Dict]:
        """Get candidate by ID"""
        query = "SELECT * FROM candidates WHERE id = ?"
        return self.execute_query(query, (candidate_id,), fetch_one=True)

    @retry_on_lock(max_retries=10, delay=0.1)
    def get_all_candidates(self, limit: int = 100) -> List[Dict]:
        """Get all candidates"""
        query = "SELECT * FROM candidates ORDER BY created_at DESC LIMIT ?"
        return self.execute_query(query, (limit,), fetch_all=True)

    @retry_on_lock(max_retries=10, delay=0.1)
    def search_candidates(self, search_term: str) -> List[Dict]:
        """Search candidates by name or email"""
        query = """
            SELECT * FROM candidates 
            WHERE name LIKE ? OR email LIKE ?
            ORDER BY created_at DESC
        """
        search_pattern = f"%{search_term}%"
        return self.execute_query(query, (search_pattern, search_pattern), fetch_all=True)

    @retry_on_lock(max_retries=10, delay=0.1)
    def delete_candidate(self, candidate_id: int):
        """Delete candidate and associated match results"""
        query = "DELETE FROM candidates WHERE id = ?"
        self.execute_query(query, (candidate_id,))

    # ==================== JOB POST OPERATIONS ====================

    @retry_on_lock(max_retries=10, delay=0.1)
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

        return self.execute_query(query, (
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

    @retry_on_lock(max_retries=10, delay=0.1)
    def get_job_post(self, job_id: int) -> Optional[Dict]:
        """Get job post by ID"""
        query = "SELECT * FROM job_posts WHERE id = ?"
        return self.execute_query(query, (job_id,), fetch_one=True)

    @retry_on_lock(max_retries=10, delay=0.1)
    def get_all_job_posts(self, status: str = 'active', limit: int = 100) -> List[Dict]:
        """Get all job posts"""
        if status == 'all':
            query = "SELECT * FROM job_posts ORDER BY created_at DESC LIMIT ?"
            params = (limit,)
        else:
            query = "SELECT * FROM job_posts WHERE status = ? ORDER BY created_at DESC LIMIT ?"
            params = (status, limit)

        return self.execute_query(query, params, fetch_all=True)

    @retry_on_lock(max_retries=10, delay=0.1)
    def update_job_status(self, job_id: int, status: str):
        """Update job post status"""
        query = "UPDATE job_posts SET status = ?, updated_at = ? WHERE id = ?"
        self.execute_query(query, (status, datetime.now(), job_id))

    @retry_on_lock(max_retries=10, delay=0.1)
    def delete_job_post(self, job_id: int):
        """Delete job post and associated match results"""
        query = "DELETE FROM job_posts WHERE id = ?"
        self.execute_query(query, (job_id,))

    # ==================== MATCH RESULTS OPERATIONS ====================

    @retry_on_lock(max_retries=10, delay=0.1)
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
        self.execute_query(query, (candidate_id, job_id, match_score, category))

    @retry_on_lock(max_retries=10, delay=0.1)
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
        return self.execute_query(query, (job_id, min_score), fetch_all=True)

    @retry_on_lock(max_retries=10, delay=0.1)
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
        return self.execute_query(query, (candidate_id, min_score), fetch_all=True)

    @retry_on_lock(max_retries=10, delay=0.1)
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
        return self.execute_query(query, (limit,), fetch_all=True)

    # ==================== STATISTICS ====================

    @retry_on_lock(max_retries=10, delay=0.1)
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        with self._connection_lock:
            conn = self.get_connection()
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
