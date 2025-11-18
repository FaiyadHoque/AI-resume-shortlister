-- AI Resume Shortlister Database Schema
-- SQLite compatible schema

-- Table: candidates
-- Stores candidate information extracted from resume PDFs
CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    objective TEXT,
    education TEXT,
    skills TEXT,
    experience_years INTEGER,
    experience_details TEXT,
    projects TEXT,
    certifications TEXT,
    resume_text TEXT,
    resume_filename TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: job_posts
-- Stores job posting requirements
CREATE TABLE IF NOT EXISTS job_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT,
    location TEXT,
    job_type TEXT,
    description TEXT NOT NULL,
    required_skills TEXT,
    required_education TEXT,
    required_experience_years INTEGER,
    salary_range TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: match_results
-- Stores matching scores between candidates and jobs
CREATE TABLE IF NOT EXISTS match_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    match_score REAL NOT NULL,
    match_category TEXT,
    matched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES job_posts(id) ON DELETE CASCADE,
    UNIQUE(candidate_id, job_id)
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_candidates_name ON candidates(name);
CREATE INDEX IF NOT EXISTS idx_candidates_email ON candidates(email);
CREATE INDEX IF NOT EXISTS idx_job_posts_status ON job_posts(status);
CREATE INDEX IF NOT EXISTS idx_match_results_score ON match_results(match_score DESC);
CREATE INDEX IF NOT EXISTS idx_match_results_candidate ON match_results(candidate_id);
CREATE INDEX IF NOT EXISTS idx_match_results_job ON match_results(job_id);
