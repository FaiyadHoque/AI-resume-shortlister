"""
AI Resume Shortlister - Streamlit UI
Simplified application with two-table database structure
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import tempfile
from datetime import datetime

# Import local modules
from database import get_db
from cnvrt import condense_job_posting, condense_resume
from matching_engine import MatchingEngine

# Page configuration
st.set_page_config(
    page_title="AI RESUME SHORTLISTER",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Sidebar navigation buttons - remove boxes */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        padding: 12px 16px !important;
        border-radius: 0px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        margin-bottom: 4px !important;
        transition: all 0.3s ease !important;
        border: none !important;
        background-color: transparent !important;
        color: inherit !important;
        box-shadow: none !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(102, 126, 234, 0.1) !important;
        transform: translateX(8px) !important;
        padding-left: 24px !important;
        border-left: 3px solid rgba(102, 126, 234, 0.8) !important;
        color: #667eea !important;
    }
    
    /* Active/clicked state */
    [data-testid="stSidebar"] .stButton > button:active,
    [data-testid="stSidebar"] .stButton > button:focus {
        background-color: rgba(102, 126, 234, 0.15) !important;
        border-left: 3px solid #667eea !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
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
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'db' not in st.session_state:
        st.session_state.db = get_db()
    if 'matching_engine' not in st.session_state:
        try:
            # Initialize with hybrid scoring (60% Cosine + 40% XGBoost)
            st.session_state.matching_engine = MatchingEngine(
                cosine_weight=0.6,
                xgb_weight=0.4
            )
        except Exception as e:
            st.error(f"Error loading matching model: {e}")
            st.session_state.matching_engine = None


def dashboard_page():
    """Dashboard with statistics"""
    st.markdown('<div class="main-header">Dashboard</div>',
                unsafe_allow_html=True)

    stats = st.session_state.db.get_statistics()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Resumes", stats['total_resumes'])
    with col2:
        st.metric("Total Jobs", stats['total_jobs'])

    st.markdown("---")
    st.info("Upload resumes and add jobs to start matching!")


def upload_resume_page():
    """Upload and process resume"""
    st.markdown('<div class="main-header">Upload Resume</div>',
                unsafe_allow_html=True)

    # Initialize session state
    if 'resume_saved' not in st.session_state:
        st.session_state.resume_saved = False

    # Input methods
    tab1, tab2 = st.tabs(["Upload File", "Paste Text"])

    resume_text = None
    applicant_name = None

    with tab1:
        uploaded_file = st.file_uploader(
            "Upload resume (TXT or PDF)", type=['txt', 'pdf'])
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                resume_text = uploaded_file.read().decode('utf-8')
            elif uploaded_file.type == "application/pdf":
                st.warning(
                    "PDF parsing not implemented yet. Please paste text instead.")

    with tab2:
        pasted_text = st.text_area("Paste resume text here", height=300)
        if pasted_text:
            resume_text = pasted_text

    # Name input
    if resume_text:
        st.markdown("---")
        applicant_name = st.text_input(
            "Applicant Name*", placeholder="Enter applicant's full name")

        # Show preview
        with st.expander("Resume Preview"):
            st.text_area("", resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
                         height=200, disabled=True)

        # Process button
        if st.button("Process & Save Resume", type="primary", disabled=not applicant_name):
            if not applicant_name:
                st.error("Please enter applicant name!")
            else:
                with st.spinner("Processing resume with Gemini AI..."):
                    try:
                        # Convert using cnvrt.py
                        resume_model = condense_resume(resume_text)

                        # Save to database
                        resume_id = st.session_state.db.add_resume(
                            applicant_name=applicant_name,
                            resume_description=resume_text,
                            resume_description_model=resume_model
                        )

                        st.success(
                            f"Resume saved successfully! (ID: {resume_id})")
                        st.session_state.resume_saved = True

                        # Show processed output
                        with st.expander("Model-Ready Format"):
                            st.code(resume_model, language="text")

                    except Exception as e:
                        st.error(f"Error processing resume: {e}")

    # Show recent resumes
    st.markdown("---")
    st.subheader("Recent Resumes")
    resumes = st.session_state.db.get_all_resumes(limit=5)
    if resumes:
        df = pd.DataFrame(resumes)
        display_df = df[['id', 'applicant_name', 'created_at']].copy()
        display_df.columns = ['ID', 'Applicant Name', 'Added On']
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No resumes yet. Upload one to get started!")


def manage_resumes_page():
    """View and manage all resumes"""
    st.markdown('<div class="main-header">Manage Resumes</div>',
                unsafe_allow_html=True)

    # Search
    search_term = st.text_input("Search by name", "")

    if search_term:
        resumes = st.session_state.db.search_resumes(search_term)
    else:
        resumes = st.session_state.db.get_all_resumes(limit=100)

    st.write(f"**Total Resumes:** {len(resumes)}")

    if resumes:
        for resume in resumes:
            with st.expander(f"{resume['applicant_name']} (ID: {resume['id']})"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**Added:** {resume['created_at']}")
                    st.text_area("Resume Description", resume['resume_description'][:300] + "...",
                                 height=150, disabled=True, key=f"desc_{resume['id']}")

                    with st.expander("Model Format"):
                        st.code(
                            resume['resume_description_model'], language="text")

                with col2:
                    if st.button("Delete", key=f"del_resume_{resume['id']}"):
                        st.session_state.db.delete_resume(resume['id'])
                        st.success("Deleted!")
                        st.rerun()
    else:
        st.info("No resumes found.")


def add_job_page():
    """Add new job posting"""
    st.markdown('<div class="main-header">Add Job</div>',
                unsafe_allow_html=True)

    with st.form("add_job_form"):
        job_name = st.text_input(
            "Job Title*", placeholder="e.g., Senior Machine Learning Engineer")

        job_description = st.text_area("Job Description*", height=300,
                                       placeholder="Paste full job description here...")

        submitted = st.form_submit_button("Save Job", type="primary")

    if submitted:
        if not job_name or not job_description:
            st.error("Please fill in both job title and description!")
        else:
            with st.spinner("Processing job description with Gemini AI..."):
                try:
                    # Convert using cnvrt.py
                    job_model = condense_job_posting(job_description)

                    # Save to database
                    job_id = st.session_state.db.add_job(
                        job_name=job_name,
                        job_description=job_description,
                        job_description_model=job_model
                    )

                    st.success(f"Job saved successfully! (ID: {job_id})")

                    # Show processed output
                    with st.expander("Model-Ready Format"):
                        st.code(job_model, language="text")

                except Exception as e:
                    st.error(f"Error processing job: {e}")

    # Show recent jobs
    st.markdown("---")
    st.subheader("Recent Jobs")
    jobs = st.session_state.db.get_all_jobs(limit=5)
    if jobs:
        df = pd.DataFrame(jobs)
        display_df = df[['id', 'job_name', 'created_at']].copy()
        display_df.columns = ['ID', 'Job Title', 'Added On']
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No jobs yet. Add one to get started!")


def manage_jobs_page():
    """View and manage all jobs"""
    st.markdown('<div class="main-header">Manage Jobs</div>',
                unsafe_allow_html=True)

    # Search
    search_term = st.text_input("Search by title", "")

    if search_term:
        jobs = st.session_state.db.search_jobs(search_term)
    else:
        jobs = st.session_state.db.get_all_jobs(limit=100)

    st.write(f"**Total Jobs:** {len(jobs)}")

    if jobs:
        for job in jobs:
            with st.expander(f"{job['job_name']} (ID: {job['id']})"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**Added:** {job['created_at']}")
                    st.text_area("Job Description", job['job_description'][:300] + "...",
                                 height=150, disabled=True, key=f"desc_{job['id']}")

                    with st.expander("Model Format"):
                        st.code(job['job_description_model'], language="text")

                with col2:
                    if st.button("Delete", key=f"del_job_{job['id']}"):
                        st.session_state.db.delete_job(job['id'])
                        st.success("Deleted!")
                        st.rerun()
    else:
        st.info("No jobs found.")


def display_ranking_results(job_id: int):
    """Display ranking results for ONLY shortlisted candidates for THIS specific job"""
    db = st.session_state.db
    engine = st.session_state.matching_engine

    # Get job details
    job = db.get_job(job_id)
    if not job:
        st.error("Job not found!")
        return

    # Get all resumes and re-match them to get shortlisted ones for THIS job
    resumes = db.get_all_resumes()

    if not resumes:
        st.warning("No resumes available.")
        return

    # Collect ONLY shortlisted resumes for THIS specific job
    shortlisted_resumes = []

    with st.spinner("Ranking shortlisted candidates..."):
        for resume in resumes:
            # Re-run matching for this specific job
            result = engine.predict_match(
                resume['resume_description_model'],
                job['job_description_model'],
                resume_id=str(resume['id'])
            )

            score = result['match_score'] if isinstance(
                result, dict) else result
            category = result.get('category', 'Not Shortlisted') if isinstance(
                result, dict) else 'Not Shortlisted'

            # Save match to database
            db.save_match(
                resume_id=resume['id'],
                job_id=job['id'],
                match_score=score / 100.0,  # Convert to 0-1 scale
                match_category=category
            )

            # ONLY include if shortlisted (score >= 65)
            if score >= 65:
                experience_years = result.get(
                    'experience_years', 0) if isinstance(result, dict) else 0

                shortlisted_resumes.append({
                    'resume_id': resume['id'],
                    'applicant_name': resume['applicant_name'],
                    'match_score': score,
                    'experience_years': experience_years
                })

    if not shortlisted_resumes:
        st.warning("No shortlisted resumes found for this job.")
        return

    # Sort by experience (DESCENDING), then by match score (DESCENDING)
    shortlisted_resumes.sort(
        key=lambda x: (x['experience_years'], x['match_score']),
        reverse=True
    )

    # Display header
    st.success(
        f"✅ Ranked {len(shortlisted_resumes)} shortlisted candidates for **{job['job_name']}** by experience")

    # Statistics
    if shortlisted_resumes:
        experiences = [r['experience_years'] for r in shortlisted_resumes]
        scores = [r['match_score'] for r in shortlisted_resumes]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Shortlisted", len(shortlisted_resumes))
        with col2:
            st.metric("Avg Experience",
                      f"{sum(experiences)/len(experiences):.1f} yrs")
        with col3:
            st.metric("Max Experience", f"{max(experiences)} yrs")
        with col4:
            st.metric("Avg Match Score", f"{sum(scores)/len(scores):.1f}%")

    st.markdown("---")

    # Display ranked candidates in card format
    st.markdown("### 🏆 Ranked by Experience (Most Experienced First)")

    for rank, candidate in enumerate(shortlisted_resumes, 1):
        st.markdown('<div class="match-excellent">', unsafe_allow_html=True)
        st.write(
            f"**{rank}. {candidate['applicant_name']}** - {candidate['match_score']:.1f}%")
        st.write(f"Experience: {candidate['experience_years']} years")
        st.write(f"Resume ID: {candidate['resume_id']}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Download option
    st.markdown("### 📥 Download Rankings")

    # Create simple CSV data
    csv_data = []
    for rank, candidate in enumerate(shortlisted_resumes, 1):
        csv_data.append({
            'Rank': rank,
            'Applicant Name': candidate['applicant_name'],
            'Experience (Years)': candidate['experience_years'],
            'Match Score (%)': candidate['match_score'],
            'Resume ID': candidate['resume_id']
        })

    df = pd.DataFrame(csv_data)
    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Download Ranked Results (CSV)",
        data=csv,
        file_name=f"ranked_{job['job_name'].replace(' ', '_')}.csv",
        mime="text/csv",
        use_container_width=True
    )


def matching_page():
    """Match resumes with jobs"""
    st.markdown('<div class="main-header">Matching</div>',
                unsafe_allow_html=True)

    if not st.session_state.matching_engine:
        st.error("Matching engine not initialized. Check if model files exist.")
        return

    tab1, tab2 = st.tabs(["Match Resume to Jobs", "Match Job to Resumes"])

    with tab1:
        st.subheader("Find Jobs for a Resume")

        resumes = st.session_state.db.get_all_resumes()
        if not resumes:
            st.info("No resumes available. Upload resumes first!")
        else:
            resume_options = {
                f"{r['applicant_name']} (ID: {r['id']})": r for r in resumes}
            selected_resume = st.selectbox(
                "Select Resume", list(resume_options.keys()))

            if st.button("Find Matching Jobs", type="primary"):
                resume = resume_options[selected_resume]
                jobs = st.session_state.db.get_all_jobs()

                if not jobs:
                    st.warning("No jobs available. Add jobs first!")
                else:
                    with st.spinner("Matching..."):
                        matches = []
                        for job in jobs:
                            result = st.session_state.matching_engine.predict_match(
                                resume['resume_description_model'],
                                job['job_description_model'],
                                resume_id=str(resume['id'])
                            )
                            score = result['match_score'] if isinstance(
                                result, dict) else result
                            category = result.get('category', 'Not Shortlisted') if isinstance(
                                result, dict) else 'Not Shortlisted'

                            # Save match to database
                            st.session_state.db.save_match(
                                resume_id=resume['id'],
                                job_id=job['id'],
                                match_score=score / 100.0,  # Convert to 0-1 scale
                                match_category=category
                            )

                            matches.append({
                                'job_name': job['job_name'],
                                'job_id': job['id'],
                                'score': score
                            })

                        # Sort by score
                        matches.sort(key=lambda x: x['score'], reverse=True)

                        st.markdown("### Match Results")

                        # Separate shortlisted and rejected
                        shortlisted = [m for m in matches if m['score'] >= 65]
                        rejected = [m for m in matches if m['score'] < 65]

                        if shortlisted:
                            st.markdown("#### ✅ Shortlisted")
                            for i, match in enumerate(shortlisted, 1):
                                st.markdown(
                                    '<div class="match-excellent">', unsafe_allow_html=True)
                                st.write(
                                    f"**{i}. {match['job_name']}** - {match['score']:.1f}%")
                                st.write(f"Job ID: {match['job_id']}")
                                st.markdown('</div>', unsafe_allow_html=True)

                        if rejected:
                            st.markdown("#### ❌ Not Shortlisted")
                            for i, match in enumerate(rejected, 1):
                                st.markdown('<div class="match-poor">',
                                            unsafe_allow_html=True)
                                st.write(
                                    f"**{i}. {match['job_name']}** - {match['score']:.1f}%")
                                st.write(f"Job ID: {match['job_id']}")
                                st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.subheader("Find Resumes for a Job")

        jobs = st.session_state.db.get_all_jobs()
        if not jobs:
            st.info("No jobs available. Add jobs first!")
        else:
            job_options = {
                f"{j['job_name']} (ID: {j['id']})": j['id'] for j in jobs}
            selected_job = st.selectbox("Select Job", list(job_options.keys()))

            col1, col2 = st.columns([3, 1])

            with col1:
                match_button = st.button(
                    "Find Matching Resumes", type="primary", key="match_job", use_container_width=True)

            with col2:
                rank_button = st.button(
                    "🏆 Rank by Experience", key="rank_exp", use_container_width=True)

            if match_button:
                job_id = job_options[selected_job]
                job = st.session_state.db.get_job(job_id)
                resumes = st.session_state.db.get_all_resumes()

                if not resumes:
                    st.warning("No resumes available. Upload resumes first!")
                else:
                    with st.spinner("Matching..."):
                        matches = []
                        for resume in resumes:
                            result = st.session_state.matching_engine.predict_match(
                                resume['resume_description_model'],
                                job['job_description_model'],
                                resume_id=str(resume['id'])
                            )
                            score = result['match_score'] if isinstance(
                                result, dict) else result
                            category = result.get('category', 'Not Shortlisted') if isinstance(
                                result, dict) else 'Not Shortlisted'

                            # Save match to database
                            st.session_state.db.save_match(
                                resume_id=resume['id'],
                                job_id=job['id'],
                                match_score=score / 100.0,  # Convert to 0-1 scale
                                match_category=category
                            )

                            matches.append({
                                'applicant_name': resume['applicant_name'],
                                'resume_id': resume['id'],
                                'score': score
                            })

                        # Sort by score
                        matches.sort(key=lambda x: x['score'], reverse=True)

                        st.markdown("### Match Results")

                        # Separate shortlisted and rejected
                        shortlisted = [m for m in matches if m['score'] >= 65]
                        rejected = [m for m in matches if m['score'] < 65]

                        if shortlisted:
                            st.markdown("#### ✅ Shortlisted")
                            for i, match in enumerate(shortlisted, 1):
                                st.markdown(
                                    '<div class="match-excellent">', unsafe_allow_html=True)
                                st.write(
                                    f"**{i}. {match['applicant_name']}** - {match['score']:.1f}%")
                                st.write(f"Resume ID: {match['resume_id']}")
                                st.markdown('</div>', unsafe_allow_html=True)

                        if rejected:
                            st.markdown("#### ❌ Not Shortlisted")
                            for i, match in enumerate(rejected, 1):
                                st.markdown('<div class="match-poor">',
                                            unsafe_allow_html=True)
                                st.write(
                                    f"**{i}. {match['applicant_name']}** - {match['score']:.1f}%")
                                st.write(f"Resume ID: {match['resume_id']}")
                                st.markdown('</div>', unsafe_allow_html=True)

            if rank_button:
                job_id = job_options[selected_job]  # Get the job ID (integer)

                st.markdown("---")
                st.markdown("### 🏆 Experience-Based Ranking")

                # Call the ranking function with integer ID
                display_ranking_results(job_id)


def main():
    """Main application"""
    init_session_state()

    # Sidebar navigation
    with st.sidebar:
        st.title("AI Resume Shortlister")
        st.markdown("---")

        if 'page' not in st.session_state:
            st.session_state.page = "Dashboard"

        nav_pages = [
            "Dashboard",
            "Upload Resume",
            "Manage Resumes",
            "Add Job",
            "Manage Jobs",
            "Matching"
        ]

        for p in nav_pages:
            if st.button(p, key=f"nav_{p}"):
                st.session_state.page = p

        st.markdown("---")
        st.caption("Built with Streamlit & XGBoost")

    # Route to pages
    page = st.session_state.get('page', "Dashboard")

    if page == "Dashboard":
        dashboard_page()
    elif page == "Upload Resume":
        upload_resume_page()
    elif page == "Manage Resumes":
        manage_resumes_page()
    elif page == "Add Job":
        add_job_page()
    elif page == "Manage Jobs":
        manage_jobs_page()
    elif page == "Matching":
        matching_page()


if __name__ == "__main__":
    main()
