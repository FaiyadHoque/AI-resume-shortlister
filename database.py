"""
SQLite Database Manager for AI Resume Shortlister
Simplified database structure with two tables: jobs and resumes
"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Dict, Any


class Database:
    """Simple SQLite database manager"""

    def __init__(self, db_path: str = "resume_shortlister.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()

    def _connect(self):
        """Create database connection with lock prevention"""
        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            timeout=30.0,  # Wait up to 30 seconds for locks
            isolation_level=None  # Autocommit mode
        )
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.conn.cursor()

        # Enable Write-Ahead Logging for better concurrency
        self.cursor.execute('PRAGMA journal_mode=WAL')
        self.cursor.execute('PRAGMA busy_timeout=30000')
        self.cursor.execute('PRAGMA synchronous=NORMAL')

    def _create_tables(self):
        """Create tables if they don't exist"""

        # Jobs table: job_name, job_description, job_description_model
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT NOT NULL,
                job_description TEXT NOT NULL,
                job_description_model TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Resumes table: applicant_name, resume_description, resume_description_model
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                applicant_name TEXT NOT NULL,
                resume_description TEXT NOT NULL,
                resume_description_model TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Matches table: stores matching results between resumes and jobs
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                match_score REAL NOT NULL,
                match_category TEXT NOT NULL,
                matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
                UNIQUE(resume_id, job_id)
            )
        """)

        self.conn.commit()

    # ============= JOB OPERATIONS =============

    def add_job(self, job_name: str, job_description: str, job_description_model: str) -> int:
        """
        Add a new job to the database

        Args:
            job_name: Name/title of the job
            job_description: Raw job description text
            job_description_model: Processed text for model use (from cnvrt.py)

        Returns:
            job_id: ID of the inserted job
        """
        self.cursor.execute("""
            INSERT INTO jobs (job_name, job_description, job_description_model)
            VALUES (?, ?, ?)
        """, (job_name, job_description, job_description_model))

        self.conn.commit()
        return self.cursor.lastrowid

    def get_job(self, job_id: int) -> Optional[Dict[str, Any]]:
        """Get a single job by ID"""
        self.cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_all_jobs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all jobs"""
        self.cursor.execute(
            "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict(row) for row in self.cursor.fetchall()]

    def update_job(self, job_id: int, job_name: str = None,
                   job_description: str = None,
                   job_description_model: str = None):
        """Update an existing job"""
        updates = []
        params = []

        if job_name:
            updates.append("job_name = ?")
            params.append(job_name)
        if job_description:
            updates.append("job_description = ?")
            params.append(job_description)
        if job_description_model:
            updates.append("job_description_model = ?")
            params.append(job_description_model)

        if updates:
            params.append(job_id)
            query = f"UPDATE jobs SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, params)
            self.conn.commit()

    def delete_job(self, job_id: int):
        """Delete a job"""
        self.cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        self.conn.commit()

    def search_jobs(self, search_term: str) -> List[Dict[str, Any]]:
        """Search jobs by name or description"""
        query = """
            SELECT * FROM jobs 
            WHERE job_name LIKE ? OR job_description LIKE ?
            ORDER BY created_at DESC
        """
        search_pattern = f"%{search_term}%"
        self.cursor.execute(query, (search_pattern, search_pattern))
        return [dict(row) for row in self.cursor.fetchall()]

    # ============= RESUME OPERATIONS =============

    def add_resume(self, applicant_name: str, resume_description: str,
                   resume_description_model: str) -> int:
        """
        Add a new resume to the database

        Args:
            applicant_name: Name of the applicant
            resume_description: Raw resume text
            resume_description_model: Processed text for model use (from cnvrt.py)

        Returns:
            resume_id: ID of the inserted resume
        """
        self.cursor.execute("""
            INSERT INTO resumes (applicant_name, resume_description, resume_description_model)
            VALUES (?, ?, ?)
        """, (applicant_name, resume_description, resume_description_model))

        self.conn.commit()
        return self.cursor.lastrowid

    def get_resume(self, resume_id: int) -> Optional[Dict[str, Any]]:
        """Get a single resume by ID"""
        self.cursor.execute("SELECT * FROM resumes WHERE id = ?", (resume_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_all_resumes(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all resumes"""
        self.cursor.execute(
            "SELECT * FROM resumes ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict(row) for row in self.cursor.fetchall()]

    def update_resume(self, resume_id: int, applicant_name: str = None,
                      resume_description: str = None,
                      resume_description_model: str = None):
        """Update an existing resume"""
        updates = []
        params = []

        if applicant_name:
            updates.append("applicant_name = ?")
            params.append(applicant_name)
        if resume_description:
            updates.append("resume_description = ?")
            params.append(resume_description)
        if resume_description_model:
            updates.append("resume_description_model = ?")
            params.append(resume_description_model)

        if updates:
            params.append(resume_id)
            query = f"UPDATE resumes SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, params)
            self.conn.commit()

    def delete_resume(self, resume_id: int):
        """Delete a resume"""
        self.cursor.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
        self.conn.commit()

    def search_resumes(self, search_term: str) -> List[Dict[str, Any]]:
        """Search resumes by name or description"""
        query = """
            SELECT * FROM resumes 
            WHERE applicant_name LIKE ? OR resume_description LIKE ?
            ORDER BY created_at DESC
        """
        search_pattern = f"%{search_term}%"
        self.cursor.execute(query, (search_pattern, search_pattern))
        return [dict(row) for row in self.cursor.fetchall()]

    # ============= MATCH OPERATIONS =============

    def save_match(self, resume_id: int, job_id: int, match_score: float,
                   match_category: str) -> int:
        """
        Save or update a match result between a resume and job

        Args:
            resume_id: ID of the resume
            job_id: ID of the job
            match_score: Match score (0-1)
            match_category: Category (Excellent, Good, Moderate, Poor)

        Returns:
            match_id: ID of the inserted/updated match
        """
        # Use INSERT OR REPLACE to handle duplicates
        self.cursor.execute("""
            INSERT INTO matches (resume_id, job_id, match_score, match_category, matched_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(resume_id, job_id) 
            DO UPDATE SET 
                match_score = excluded.match_score,
                match_category = excluded.match_category,
                matched_at = CURRENT_TIMESTAMP
        """, (resume_id, job_id, match_score, match_category))

        self.conn.commit()
        return self.cursor.lastrowid

    def get_match(self, resume_id: int, job_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific match between resume and job"""
        self.cursor.execute("""
            SELECT m.*, r.applicant_name, j.job_name
            FROM matches m
            JOIN resumes r ON m.resume_id = r.id
            JOIN jobs j ON m.job_id = j.id
            WHERE m.resume_id = ? AND m.job_id = ?
        """, (resume_id, job_id))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_matches_for_job(self, job_id: int, min_score: float = 0.0) -> List[Dict[str, Any]]:
        """
        Get all candidate matches for a specific job, sorted by score

        Args:
            job_id: ID of the job
            min_score: Minimum match score filter (default 0.0)

        Returns:
            List of matches with candidate details
        """
        self.cursor.execute("""
            SELECT m.*, r.applicant_name, r.resume_description
            FROM matches m
            JOIN resumes r ON m.resume_id = r.id
            WHERE m.job_id = ? AND m.match_score >= ?
            ORDER BY m.match_score DESC
        """, (job_id, min_score))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_matches_for_resume(self, resume_id: int, min_score: float = 0.0) -> List[Dict[str, Any]]:
        """
        Get all job matches for a specific resume, sorted by score

        Args:
            resume_id: ID of the resume
            min_score: Minimum match score filter (default 0.0)

        Returns:
            List of matches with job details
        """
        self.cursor.execute("""
            SELECT m.*, j.job_name, j.job_description
            FROM matches m
            JOIN jobs j ON m.job_id = j.id
            WHERE m.resume_id = ? AND m.match_score >= ?
            ORDER BY m.match_score DESC
        """, (resume_id, min_score))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_all_matches(self, min_score: float = 0.0) -> List[Dict[str, Any]]:
        """
        Get all matches in the database

        Args:
            min_score: Minimum match score filter (default 0.0)

        Returns:
            List of all matches with resume and job details
        """
        self.cursor.execute("""
            SELECT m.*, r.applicant_name, j.job_name
            FROM matches m
            JOIN resumes r ON m.resume_id = r.id
            JOIN jobs j ON m.job_id = j.id
            WHERE m.match_score >= ?
            ORDER BY m.match_score DESC
        """, (min_score,))
        return [dict(row) for row in self.cursor.fetchall()]

    def get_top_matches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top N matches across all resumes and jobs"""
        self.cursor.execute("""
            SELECT m.*, r.applicant_name, j.job_name
            FROM matches m
            JOIN resumes r ON m.resume_id = r.id
            JOIN jobs j ON m.job_id = j.id
            ORDER BY m.match_score DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in self.cursor.fetchall()]

    def delete_match(self, match_id: int):
        """Delete a specific match"""
        self.cursor.execute("DELETE FROM matches WHERE id = ?", (match_id,))
        self.conn.commit()

    def delete_matches_for_job(self, job_id: int):
        """Delete all matches for a specific job"""
        self.cursor.execute("DELETE FROM matches WHERE job_id = ?", (job_id,))
        self.conn.commit()

    def delete_matches_for_resume(self, resume_id: int):
        """Delete all matches for a specific resume"""
        self.cursor.execute(
            "DELETE FROM matches WHERE resume_id = ?", (resume_id,))
        self.conn.commit()

    # ============= STATISTICS =============

    def get_statistics(self) -> Dict[str, int]:
        """Get database statistics"""
        self.cursor.execute("SELECT COUNT(*) as count FROM jobs")
        job_count = self.cursor.fetchone()['count']

        self.cursor.execute("SELECT COUNT(*) as count FROM resumes")
        resume_count = self.cursor.fetchone()['count']

        self.cursor.execute("SELECT COUNT(*) as count FROM matches")
        match_count = self.cursor.fetchone()['count']

        return {
            'total_jobs': job_count,
            'total_resumes': resume_count,
            'total_matches': match_count
        }

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Cleanup"""
        self.close()


# Singleton instance
_db_instance = None


def get_db() -> Database:
    """Get or create database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
