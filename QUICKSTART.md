# 🚀 Quick Start Guide

## AI Resume Shortlister - Complete System

### What This System Does

1. **Extract** information from resume PDFs automatically
2. **Store** candidate and job data in a SQL database
3. **Match** candidates with jobs using AI (XGBoost model)
4. **Visualize** matches through a web interface

---

## Installation (5 minutes)

```bash
# 1. Navigate to project directory
cd "AI-resume-shortlister"

# 2. Create virtual environment (if not exists)
python -m venv .venv

# 3. Activate virtual environment
source .venv/bin/activate  # Mac/Linux
# OR
.venv\Scripts\activate  # Windows

# 4. Install dependencies
pip install -r requirements.txt
```

---

## Running the Application

### Start the Web UI

```bash
streamlit run app.py
```

The app will open in your browser at: `http://localhost:8501`

### Test the System

```bash
python test_system.py
```

---

## First-Time Usage

### Step 1: Add a Job Post

1. Click **"💼 Job Posts"** in sidebar
2. Go to **"➕ Add New Job"** tab
3. Fill in:
   - Job Title (e.g., "Senior Software Engineer")
   - Company name
   - Job Description (detailed)
   - Required Skills
   - Experience years
4. Click **"Save Job Post"**

### Step 2: Upload Resume PDFs

1. Click **"📤 Upload Resume"** in sidebar
2. Click **"Browse files"** and select a PDF resume
3. Review extracted information:
   - Name, email, phone
   - Skills, experience, education
4. Edit if needed
5. Click **"Save to Database"**
6. Optionally click **"🔍 Match with All Jobs"** to match immediately

### Step 3: View Matches

1. Click **"🎯 Matches"** in sidebar
2. Select either:
   - **"By Job"**: See all candidates for a specific job
   - **"By Candidate"**: See all jobs for a specific candidate
3. Adjust minimum score slider (default: 60%)
4. Click **"Show Matches"**

Results show:

- **Match Score** (0-100%)
- **Category** (Excellent/Good/Moderate/Poor)
- Contact information
- Relevant details

### Step 4: Dashboard

- Click **"📊 Dashboard"** to see:
  - Total candidates, jobs, matches
  - Average match score
  - Top 10 matches across all data

---

## Match Score Guide

| Score   | Category         | Recommendation     |
| ------- | ---------------- | ------------------ |
| 80-100% | 🟢 **Excellent** | Highly recommended |
| 60-79%  | 🟡 **Good**      | Recommended        |
| 40-59%  | 🟠 **Moderate**  | Consider carefully |
| 0-39%   | 🔴 **Poor**      | Not recommended    |

---

## Project Structure

```
AI-resume-shortlister/
├── app.py                    # 🎨 Main Streamlit web app
├── pdf_extractor.py          # 📄 PDF extraction module
├── matching_engine.py        # 🤖 AI matching engine
├── test_system.py           # 🧪 System test script
├── database/
│   ├── schema.sql           # 📊 Database tables
│   ├── db_manager.py        # 💾 Database operations
│   └── resume_shortlister.db # 🗄️ SQLite database
├── samples/                 # 📁 Sample resumes & jobs
├── xgb_model.pkl           # 🧠 Trained AI model
└── requirements.txt        # 📦 Dependencies
```

---

## Common Commands

```bash
# Start web app
streamlit run app.py

# Test system
python test_system.py

# Test with sample files
python test_model.py

# Install new packages
pip install <package-name>

# Deactivate virtual environment
deactivate
```

---

## Troubleshooting

### "Module not found" error

```bash
pip install -r requirements.txt
```

### Database not creating

- Check `database/` folder exists
- Run `test_system.py` to initialize

### Model loading error

- Ensure these files exist:
  - `xgb_model.pkl`
  - `tfidf_vectorizer.pkl`
  - `X_columns.pkl`

### PDF extraction not working

- Ensure PDFs are text-based (not scanned images)
- Try different PDF or re-save as text-based PDF

---

## Features Overview

### 📤 Upload Resume Page

- Drag & drop PDF upload
- Automatic information extraction
- Preview extracted data
- Edit before saving
- Instant matching option

### 👥 Candidates Page

- View all candidates
- Search by name/email
- Match with jobs
- Delete candidates

### 💼 Job Posts Page

- Add new job postings
- View all jobs
- Update job status (active/closed)
- Match with candidates
- Delete jobs

### 🎯 Matches Page

- View by job or candidate
- Filter by minimum score
- Color-coded results
- Detailed match information

### 📊 Dashboard

- System statistics
- Top 10 matches
- Quick overview

---

## Need Help?

Check the full documentation: `README_PROJECT.md`

---

**Happy Recruiting! 🎉**
