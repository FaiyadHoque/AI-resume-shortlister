# AI Resume Shortlister - Complete System

An intelligent resume matching system that extracts information from PDF resumes, stores them in a database, and uses machine learning to match candidates with job postings.

## 🌟 Features

- **PDF Resume Extraction**: Automatically extract structured information from resume PDFs
- **Database Storage**: Store candidates, job posts, and match results in SQLite database
- **AI-Powered Matching**: Use trained XGBoost model to match candidates with jobs
- **Web Interface**: User-friendly Streamlit UI for all operations
- **Match Scoring**: Get percentage-based match scores with categories (Excellent/Good/Moderate/Poor)

## 📋 System Components

### 1. Database (`database/`)

- `schema.sql`: Database schema with tables for candidates, job_posts, and match_results
- `db_manager.py`: Database operations (CRUD for all entities)

### 2. PDF Extraction (`pdf_extractor.py`)

- Extracts text from PDF resumes
- Parses structured information (name, email, phone, skills, experience, etc.)
- Estimates years of experience

### 3. Matching Engine (`matching_engine.py`)

- Uses trained XGBoost model for predictions
- Matches candidates with jobs based on resume and job description text
- Stores match results in database

### 4. Web Application (`app.py`)

- Streamlit-based UI with 5 main pages:
  - **Dashboard**: Statistics and top matches
  - **Upload Resume**: Extract and save resume PDFs
  - **Candidates**: View and manage candidates
  - **Job Posts**: Add and manage job postings
  - **Matches**: View match results by job or candidate

## 🚀 Installation

```bash
# Clone repository
git clone <your-repo-url>
cd AI-resume-shortlister

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📊 Database Schema

### Tables

**candidates**

- Stores candidate information extracted from resumes
- Fields: name, email, phone, objective, education, skills, experience_years, etc.

**job_posts**

- Stores job posting requirements
- Fields: title, company, location, description, required_skills, required_experience_years, etc.

**match_results**

- Stores matching scores between candidates and jobs
- Fields: candidate_id, job_id, match_score, match_category, matched_at

## 🎯 Usage

### Start the Web Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Workflow

1. **Add Job Posts**

   - Go to "💼 Job Posts" → "Add New Job"
   - Fill in job details (title, description, requirements)
   - Click "Save Job Post"

2. **Upload Resumes**

   - Go to "📤 Upload Resume"
   - Upload PDF resume file
   - Review extracted information
   - Click "Save to Database"
   - Optionally match with all jobs immediately

3. **View Matches**

   - Go to "🎯 Matches"
   - Select a job to see ranked candidates
   - Or select a candidate to see suitable jobs
   - Filter by minimum match score

4. **Dashboard**
   - View statistics (total candidates, jobs, matches)
   - See top 10 matches across the system

### Command-Line Testing

You can also test the model using the command-line script:

```bash
python test_model.py
```

This will test all resumes in the `samples/` directory against `samples/sample_job.txt`.

## 📁 Project Structure

```
AI-resume-shortlister/
├── app.py                      # Streamlit web application
├── pdf_extractor.py            # PDF extraction module
├── matching_engine.py          # Matching engine with XGBoost
├── test_model.py              # Command-line testing script
├── retrain_model.py           # Model retraining script
├── requirements.txt           # Python dependencies
├── database/
│   ├── schema.sql             # Database schema
│   ├── db_manager.py          # Database operations
│   └── resume_shortlister.db  # SQLite database (created automatically)
├── samples/
│   ├── sample_resume.txt      # Sample resume 1
│   ├── sample_resume2.txt     # Sample resume 2
│   ├── sample_resume3.txt     # Sample resume 3
│   └── sample_job.txt         # Sample job description
├── xgb_model.pkl             # Trained XGBoost model
├── tfidf_vectorizer.pkl      # TF-IDF vectorizer
└── X_columns.pkl             # Feature columns
```

## 🎨 Match Score Categories

| Score Range | Category     | Meaning                  |
| ----------- | ------------ | ------------------------ |
| 80-100%     | 🟢 Excellent | Highly recommended match |
| 60-79%      | 🟡 Good      | Recommended match        |
| 40-59%      | 🟠 Moderate  | Consider with caution    |
| 0-39%       | 🔴 Poor      | Not recommended          |

## 🔧 Technical Details

### PDF Extraction

- Uses PyPDF2 to extract text from PDFs
- Regex patterns to identify email, phone, sections (education, skills, etc.)
- Estimates experience years from date ranges or explicit mentions

### Machine Learning

- **Model**: XGBoost Regressor
- **Features**: TF-IDF vectorization of resume and job description text
- **Score**: Outputs match score on 0-1 scale (converted to percentage)
- **Training Data**: Historical resume-job matches with scores

### Database

- **Engine**: SQLite (easy to use, no server required)
- **Relationships**: Foreign keys between match_results and candidates/jobs
- **Indexes**: Optimized for common queries

## 🛠️ API Usage (Python)

```python
from database.db_manager import get_db
from pdf_extractor import extract_resume
from matching_engine import get_matching_engine

# Initialize
db = get_db()
engine = get_matching_engine()

# Extract resume from PDF
resume_data = extract_resume('path/to/resume.pdf')
candidate_id = db.add_candidate(resume_data)

# Add job post
job_data = {
    'title': 'Software Engineer',
    'description': 'We are looking for...',
    'required_skills': 'Python, Django, AWS',
    'required_experience_years': 3
}
job_id = db.add_job_post(job_data)

# Match candidate with job
result = engine.match_candidate_with_job(candidate_id, job_id)
print(f"Match Score: {result['score_percentage']:.1f}%")
print(f"Category: {result['match_category']}")

# Get all matches for a job
matches = db.get_matches_for_job(job_id, min_score=0.6)
for match in matches:
    print(f"{match['name']}: {match['match_score']*100:.1f}%")
```

## 🔄 Retraining the Model

If you have new training data (CSV with columns: `resume_text`, `job_text`, `score`):

```bash
python retrain_model.py
```

This will create new model artifacts:

- `xgb_model.pkl`
- `tfidf_vectorizer.pkl`
- `X_columns.pkl`

## 📝 Notes

- **PDF Quality**: Extraction works best with text-based PDFs (not scanned images)
- **Match Scores**: Scores are relative and depend on training data quality
- **Database**: SQLite database is created automatically in `database/` folder
- **Model**: Pre-trained XGBoost model is required for matching to work

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the system!

## 📄 License

MIT License - free to use for personal or commercial purposes.

---

**Made with ❤️ for better recruitment**
