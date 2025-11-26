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
        """Create database connection"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.conn.cursor()
    
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
        self.cursor.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,))
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
        self.cursor.execute("SELECT * FROM resumes ORDER BY created_at DESC LIMIT ?", (limit,))
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
    
    # ============= STATISTICS =============
    
    def get_statistics(self) -> Dict[str, int]:
        """Get database statistics"""
        self.cursor.execute("SELECT COUNT(*) as count FROM jobs")
        job_count = self.cursor.fetchone()['count']
        
        self.cursor.execute("SELECT COUNT(*) as count FROM resumes")
        resume_count = self.cursor.fetchone()['count']
        
        return {
            'total_jobs': job_count,
            'total_resumes': resume_count
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
