"""
AI Resume Shortlister - Streamlit UI
Web application for uploading resumes, managing jobs, and viewing matches
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import tempfile
from datetime import datetime

from database.db_manager import get_db
from gemini_client import extract_resume_via_gemini, parse_resume_text
from matching_engine import get_matching_engine


# Page configuration
st.set_page_config(
    page_title="AI RESUME SHORTLISTER",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Theme-adaptive styling that works in both light and dark modes
st.markdown("""
    <style>
    /* Full-width rectangular sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        padding: 14px 20px !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        margin-bottom: 8px !important;
        transition: all 0.2s ease !important;
        border: 2px solid rgba(128, 128, 128, 0.3) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateX(4px) !important;
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateX(2px) !important;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Match category colors - work in both light and dark modes */
    .match-excellent { 
        background: linear-gradient(90deg, rgba(40, 167, 69, 0.15) 0%, rgba(40, 167, 69, 0.05) 100%);
        padding: 0.75rem; 
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
    }
    .match-good { 
        background: linear-gradient(90deg, rgba(255, 193, 7, 0.15) 0%, rgba(255, 193, 7, 0.05) 100%);
        padding: 0.75rem; 
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    .match-moderate { 
        background: linear-gradient(90deg, rgba(255, 152, 0, 0.15) 0%, rgba(255, 152, 0, 0.05) 100%);
        padding: 0.75rem; 
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 0.5rem 0;
    }
    .match-poor { 
        background: linear-gradient(90deg, rgba(220, 53, 69, 0.15) 0%, rgba(220, 53, 69, 0.05) 100%);
        padding: 0.75rem; 
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Card-like containers */
    .stExpander {
        border-radius: 8px !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        margin-bottom: 1rem !important;
    }
    
    /* Text input focus */
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25) !important;
    }
    
    /* Improve spacing */
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'db' not in st.session_state:
        st.session_state.db = get_db()
    if 'matching_engine' not in st.session_state:
        try:
            st.session_state.matching_engine = get_matching_engine()
        except Exception as e:
            st.error(f"⚠️ Error loading matching model: {e}")
            st.session_state.matching_engine = None


def dashboard_page():
    """Dashboard page with statistics"""
    st.markdown('<div class="main-header">📊 Dashboard</div>',
                unsafe_allow_html=True)

    # Get statistics
    stats = st.session_state.db.get_statistics()

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Candidates", stats['total_candidates'])

    with col2:
        st.metric("Active Jobs", stats['active_jobs'])

    with col3:
        st.metric("Total Matches", stats['total_matches'])

    with col4:
        avg_score = stats['average_match_score'] * 100
        st.metric("Avg Match Score", f"{avg_score:.1f}%")

    st.markdown("---")

    # Recent top matches
    st.subheader("🏆 Top 10 Matches")
    top_matches = st.session_state.db.get_top_matches(limit=10)

    if top_matches:
        df = pd.DataFrame(top_matches)
        df['match_score'] = (df['match_score'] * 100).round(2)
        df = df.rename(columns={
            'candidate_name': 'Candidate',
            'candidate_email': 'Email',
            'job_title': 'Job Title',
            'job_company': 'Company',
            'match_score': 'Score (%)',
            'match_category': 'Category',
            'matched_at': 'Date'
        })
        st.dataframe(df, width='stretch')
    else:
        st.info("No matches yet. Upload resumes and add jobs to get started!")


def upload_resume_page():
    """Page for uploading resume PDFs"""
    # Centered app title
    st.markdown('<div class="main-header">📤 Upload Resume</div>',
                unsafe_allow_html=True)

    # Initialize session state for extracted data
    if 'extracted_resume' not in st.session_state:
        st.session_state.extracted_resume = None
    if 'resume_saved' not in st.session_state:
        st.session_state.resume_saved = False

    uploaded_file = st.file_uploader(
        "Choose a PDF resume file (optional)",
        type=['pdf'],
        help="Upload a candidate's resume in PDF format"
    )

    pasted_text = st.text_area(
        "Or paste resume text here (optional)", height=200)

    if uploaded_file:
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size / 1024:.2f} KB")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("🛰️ Use Gemini (file)") and uploaded_file:
            with st.spinner("Calling Gemini to extract resume..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                try:
                    resume_data = extract_resume_via_gemini(file_path=tmp_path)
                    resume_data['resume_filename'] = uploaded_file.name
                    st.session_state.extracted_resume = resume_data
                    st.session_state.resume_saved = False
                    st.success("✅ Information extracted (Gemini)!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Gemini extraction failed: {e}")
                    st.session_state.extracted_resume = None

    with col2:
        if st.button("🔎 Parse Pasted Text") and pasted_text:
            with st.spinner("Parsing pasted text..."):
                try:
                    resume_data = parse_resume_text(pasted_text)
                    resume_data['resume_filename'] = 'pasted_text'
                    st.session_state.extracted_resume = resume_data
                    st.session_state.resume_saved = False
                    st.success("✅ Text parsed successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Parsing failed: {e}")
                    st.session_state.extracted_resume = None

    with col3:
        # Alternative: use Gemini on pasted text if available
        if st.button("🛰️ Use Gemini (text)") and (pasted_text or uploaded_file):
            with st.spinner("Calling Gemini to extract from text..."):
                try:
                    if pasted_text:
                        resume_data = extract_resume_via_gemini(
                            text=pasted_text)
                        resume_data['resume_filename'] = 'pasted_text'
                    else:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        resume_data = extract_resume_via_gemini(
                            file_path=tmp_path)
                        resume_data['resume_filename'] = uploaded_file.name

                    st.session_state.extracted_resume = resume_data
                    st.session_state.resume_saved = False
                    st.success("✅ Gemini extraction complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Gemini extraction failed: {e}")
                    st.session_state.extracted_resume = None

    # Display extracted information if available
    if st.session_state.extracted_resume:
        resume_data = st.session_state.extracted_resume

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📋 Extracted Information")
            st.write(f"**Name:** {resume_data.get('name', 'Unknown')}")
            st.write(f"**Email:** {resume_data.get('email') or 'Not found'}")
            st.write(f"**Phone:** {resume_data.get('phone') or 'Not found'}")
            st.write(
                f"**Experience:** {resume_data.get('experience_years', 0)} years")

        with col2:
            st.subheader("💼 Skills")
            if resume_data.get('skills'):
                skills_text = str(
                    resume_data['skills']) if resume_data['skills'] else ""
                st.text_area(
                    "Skills", skills_text[:300], height=150, disabled=True, label_visibility="collapsed")
            else:
                st.info("No skills section found")

        # Allow editing before saving
        with st.expander("✏️ Edit Information Before Saving"):
            edited_name = st.text_input("Name", resume_data.get('name', ''))
            edited_email = st.text_input(
                "Email", resume_data.get('email') or '')
            edited_phone = st.text_input(
                "Phone", resume_data.get('phone') or '')
            edited_experience = st.number_input("Experience (years)",
                                                value=resume_data.get(
                                                    'experience_years', 0),
                                                min_value=0, max_value=50)

            # Update resume data with edits
            if edited_name:
                resume_data['name'] = edited_name
            if edited_email:
                resume_data['email'] = edited_email
            if edited_phone:
                resume_data['phone'] = edited_phone
            resume_data['experience_years'] = edited_experience

        # Save to database button
        if not st.session_state.resume_saved:
            if st.button("💾 Save to Database", type="primary"):
                try:
                    candidate_id = st.session_state.db.add_candidate(
                        resume_data)
                    st.session_state.resume_saved = True
                    st.success(
                        f"✅ Candidate saved successfully with ID: {candidate_id}")

                    # Ask if user wants to match immediately
                    if st.session_state.matching_engine:
                        st.info(
                            "💡 Go to 'View Matches' page to see this candidate's job matches!")

                except Exception as e:
                    st.error(f"❌ Error saving to database: {str(e)}")
        else:
            st.success("✅ Resume already saved to database!")
            if st.button("Upload Another Resume"):
                st.session_state.extracted_resume = None
                st.session_state.resume_saved = False
                st.rerun()

    # Show recent candidates
    st.divider()
    st.subheader("📋 Recent Candidates")

    try:
        candidates = st.session_state.db.get_all_candidates(limit=5)
        if candidates:
            df = pd.DataFrame(candidates)
            display_df = df[['id', 'name', 'email',
                             'experience_years', 'created_at']].copy()
            display_df.columns = ['ID', 'Name', 'Email',
                                  'Experience (Years)', 'Added On']
            st.dataframe(display_df, width='stretch')
        else:
            st.info("No candidates yet. Upload a resume to get started!")
    except Exception as e:
        st.error(f"Error loading candidates: {str(e)}")


def manage_candidates_page():
    """Page for viewing and managing candidates"""
    st.markdown('<div class="main-header">👥 Manage Candidates</div>',
                unsafe_allow_html=True)

    # Search bar
    search_term = st.text_input("🔍 Search by name or email", "")

    # Get candidates
    if search_term:
        candidates = st.session_state.db.search_candidates(search_term)
    else:
        candidates = st.session_state.db.get_all_candidates(limit=100)

    st.write(f"**Total Candidates:** {len(candidates)}")

    if candidates:
        # Display candidates in a table
        for candidate in candidates:
            with st.expander(f"📄 {candidate['name']} - {candidate['email'] or 'No email'}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**ID:** {candidate['id']}")
                    st.write(f"**Phone:** {candidate['phone'] or 'N/A'}")
                    st.write(
                        f"**Experience:** {candidate['experience_years']} years")
                    st.write(f"**Resume:** {candidate['resume_filename']}")
                    st.write(f"**Added:** {candidate['created_at']}")

                    if candidate['skills']:
                        skills_text = str(
                            candidate['skills']) if candidate['skills'] else ""
                        st.text_area(
                            "Skills", skills_text[:300], height=100, disabled=True, key=f"skills_{candidate['id']}")

                with col2:
                    if st.button("🔍 Match Jobs", key=f"match_{candidate['id']}"):
                        if st.session_state.matching_engine:
                            with st.spinner("Matching..."):
                                matches = st.session_state.matching_engine.match_candidate_with_all_jobs(
                                    candidate['id'])
                                st.success(
                                    f"Matched with {len(matches)} jobs!")

                    if st.button("🗑️ Delete", key=f"delete_{candidate['id']}"):
                        st.session_state.db.delete_candidate(candidate['id'])
                        st.success("Deleted!")
                        st.rerun()
    else:
        st.info("No candidates found. Upload resumes to get started!")


def manage_jobs_page():
    """Page for adding and managing job posts"""
    st.markdown('<div class="main-header">💼 Manage Job Posts</div>',
                unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["➕ Add New Job", "📋 View Jobs"])

    with tab1:
        st.subheader("Add New Job Post")

        with st.form("add_job_form"):
            title = st.text_input(
                "Job Title*", placeholder="e.g., Senior Software Engineer")
            company = st.text_input("Company", placeholder="e.g., Tech Corp")

            col1, col2 = st.columns(2)
            with col1:
                location = st.text_input(
                    "Location", placeholder="e.g., Remote / New York")
                job_type = st.selectbox(
                    "Job Type", ["Full-time", "Part-time", "Contract", "Internship"])

            with col2:
                salary_range = st.text_input(
                    "Salary Range", placeholder="e.g., $100k - $150k")
                req_experience = st.number_input(
                    "Required Experience (years)", min_value=0, max_value=50, value=3)

            description = st.text_area(
                "Job Description*", height=200, placeholder="Detailed job description...")
            required_skills = st.text_area(
                "Required Skills", height=100, placeholder="Python, Machine Learning, AWS, etc.")
            required_education = st.text_area(
                "Required Education", height=80, placeholder="Bachelor's in Computer Science or related field")

            submitted = st.form_submit_button("Save Job Post", type="primary")

            if submitted:
                if not title or not description:
                    st.error(
                        "Please fill in required fields (Title and Description)")
                else:
                    job_data = {
                        'title': title,
                        'company': company,
                        'location': location,
                        'job_type': job_type,
                        'description': description,
                        'required_skills': required_skills,
                        'required_education': required_education,
                        'required_experience_years': req_experience,
                        'salary_range': salary_range,
                        'status': 'active'
                    }

                    job_id = st.session_state.db.add_job_post(job_data)
                    st.success(f"✅ Job post saved with ID: {job_id}")

                    if st.session_state.matching_engine:
                        if st.button("🔍 Match with All Candidates"):
                            with st.spinner("Matching..."):
                                matches = st.session_state.matching_engine.match_job_with_all_candidates(
                                    job_id)
                                st.success(
                                    f"✅ Matched with {len(matches)} candidates!")

    with tab2:
        st.subheader("All Job Posts")

        jobs = st.session_state.db.get_all_job_posts(status='all')

        if jobs:
            for job in jobs:
                status_emoji = "🟢" if job['status'] == 'active' else "🔴"
                with st.expander(f"{status_emoji} {job['title']} at {job['company'] or 'Unknown'}"):
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.write(f"**ID:** {job['id']}")
                        st.write(f"**Location:** {job['location']}")
                        st.write(f"**Type:** {job['job_type']}")
                        st.write(
                            f"**Experience:** {job['required_experience_years']} years")
                        st.write(f"**Status:** {job['status']}")
                        st.write(f"**Posted:** {job['created_at']}")
                        desc_text = str(job['description']
                                        ) if job['description'] else ""
                        st.text_area(
                            "Description", desc_text[:500], height=150, disabled=True, key=f"desc_{job['id']}")

                    with col2:
                        if st.button("🔍 Match", key=f"match_job_{job['id']}"):
                            if st.session_state.matching_engine:
                                with st.spinner("Matching..."):
                                    matches = st.session_state.matching_engine.match_job_with_all_candidates(
                                        job['id'])
                                    st.success(
                                        f"Matched with {len(matches)} candidates!")

                        new_status = st.selectbox("Status", ["active", "closed"],
                                                  index=0 if job['status'] == 'active' else 1,
                                                  key=f"status_{job['id']}")

                        if st.button("Update", key=f"update_{job['id']}"):
                            st.session_state.db.update_job_status(
                                job['id'], new_status)
                            st.success("Updated!")
                            st.rerun()

                        if st.button("🗑️ Delete", key=f"delete_job_{job['id']}"):
                            st.session_state.db.delete_job_post(job['id'])
                            st.success("Deleted!")
                            st.rerun()
        else:
            st.info("No jobs added yet. Create your first job post!")


def view_matches_page():
    """Page for viewing match results"""
    # Centered app title
    st.markdown('<div class="main-header">🎯 Match Results</div>',
                unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["By Job", "By Candidate"])

    with tab1:
        st.subheader("View Candidates for Job")

        jobs = st.session_state.db.get_all_job_posts(status='active')

        if jobs:
            job_options = {
                f"{job['title']} (ID: {job['id']})": job['id'] for job in jobs}
            selected_job = st.selectbox("Select Job", list(job_options.keys()))

            min_score = st.slider("Minimum Match Score (%)", 0, 100, 60) / 100

            if st.button("Show Matches"):
                job_id = job_options[selected_job]
                matches = st.session_state.db.get_matches_for_job(
                    job_id, min_score)

                if matches:
                    st.write(f"**Found {len(matches)} matches**")

                    for i, match in enumerate(matches, 1):
                        score_pct = match['match_score'] * 100
                        category = match['match_category']

                        # Color code based on category
                        if category == "Excellent":
                            st.markdown(
                                f'<div class="match-excellent">', unsafe_allow_html=True)
                        elif category == "Good":
                            st.markdown(f'<div class="match-good">',
                                        unsafe_allow_html=True)
                        elif category == "Moderate":
                            st.markdown(
                                f'<div class="match-moderate">', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="match-poor">',
                                        unsafe_allow_html=True)

                        st.write(
                            f"**{i}. {match['name']}** - {score_pct:.1f}% ({category})")
                        st.write(
                            f"📧 {match['email']} | 📞 {match['phone'] or 'N/A'} | 💼 {match['experience_years']} years exp")
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.write("")
                else:
                    st.info("No matches found for this job.")
        else:
            st.info("No active jobs. Add job posts first!")

    with tab2:
        st.subheader("View Jobs for Candidate")

        candidates = st.session_state.db.get_all_candidates(limit=100)

        if candidates:
            candidate_options = {
                f"{c['name']} (ID: {c['id']})": c['id'] for c in candidates}
            selected_candidate = st.selectbox(
                "Select Candidate", list(candidate_options.keys()))

            min_score = st.slider("Minimum Match Score (%)",
                                  0, 100, 60, key="candidate_min_score") / 100

            if st.button("Show Matches", key="show_candidate_matches"):
                candidate_id = candidate_options[selected_candidate]
                matches = st.session_state.db.get_matches_for_candidate(
                    candidate_id, min_score)

                if matches:
                    st.write(f"**Found {len(matches)} matches**")

                    for i, match in enumerate(matches, 1):
                        score_pct = match['match_score'] * 100
                        category = match['match_category']

                        # Color code based on category
                        if category == "Excellent":
                            st.markdown(
                                f'<div class="match-excellent">', unsafe_allow_html=True)
                        elif category == "Good":
                            st.markdown(f'<div class="match-good">',
                                        unsafe_allow_html=True)
                        elif category == "Moderate":
                            st.markdown(
                                f'<div class="match-moderate">', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="match-poor">',
                                        unsafe_allow_html=True)

                        st.write(
                            f"**{i}. {match['title']}** - {score_pct:.1f}% ({category})")
                        st.write(
                            f"🏢 {match['company']} | 📍 {match['location']} | 💰 {match['salary_range'] or 'N/A'}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.write("")
                else:
                    st.info("No matches found for this candidate.")
        else:
            st.info("No candidates. Upload resumes first!")


def main():
    """Main application"""
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.title("📄 AI Resume Shortlister")
        st.markdown("---")

        # Navigation as full-width buttons
        if 'page' not in st.session_state:
            st.session_state.page = "📊 Dashboard"

        nav_pages = ["📊 Dashboard", "📤 Upload Resume",
                     "👥 Candidates", "💼 Job Posts", "🎯 Matches"]

        for p in nav_pages:
            # Key ensures each button is unique
            if st.button(p, key=f"nav_{p}"):
                st.session_state.page = p

        st.markdown("---")
        st.caption("Built with Streamlit & XGBoost")

    # Route to appropriate page (based on session state)
    page = st.session_state.get('page', "📊 Dashboard")
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "📤 Upload Resume":
        upload_resume_page()
    elif page == "👥 Candidates":
        manage_candidates_page()
    elif page == "💼 Job Posts":
        manage_jobs_page()
    elif page == "🎯 Matches":
        view_matches_page()


if __name__ == "__main__":
    main()
