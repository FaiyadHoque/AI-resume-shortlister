"""
General Resume Matching Test Script

This script:
1. Loads trained model artifacts (model, vectorizer, column names)
2. Reads job description from samples/sample_job.txt
3. Reads all resume files from samples/ directory
4. Predicts match scores for each resume against the job
5. Outputs ranked results

Usage:
    python test_model.py
"""

import pickle
import pandas as pd
from pathlib import Path
import re


def load_artifacts():
    """Load the trained model, vectorizer, and feature columns."""
    print("Loading model artifacts...")

    with open('xgb_model.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    with open('X_columns.pkl', 'rb') as f:
        X_columns = pickle.load(f)

    print("✓ Model artifacts loaded successfully!\n")
    return model, vectorizer, X_columns


def parse_job_file(filepath):
    """
    Parse a job description text file and extract structured information.
    Returns a dictionary with job details.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract job position (first line, usually the title)
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    job_position = lines[0] if lines else "Unknown Position"

    # Try to extract education requirements
    education = "Unknown"
    education_patterns = [
        r"Education:?\s*[•\n]*(.*?)(?=\n\n|\nExperience:|\nTechnical Skills:|\nRESPONSIBILITIES:|$)",
        r"(Bachelor|Master|PhD|degree).*?(?=\n\n|\n[A-Z]|$)",
    ]
    for pattern in education_patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            education = match.group(0).strip()
            # Clean up - take first meaningful line
            education_lines = [l.strip('• ').strip() for l in education.split(
                '\n') if l.strip() and l.strip() != 'Education:']
            if education_lines:
                education = education_lines[0][:100]  # Limit length
            break

    # Try to extract experience requirements
    experience = "Unknown"
    experience_patterns = [
        r"Experience:?\s*[•\n]*(.*?)(?=\n\n|\nTechnical Skills:|\nRESPONSIBILITIES:|$)",
        r"(\d+[\+\-]?\s*years?).*?experience",
    ]
    for pattern in experience_patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            experience = match.group(0).strip()
            # Clean up - take first meaningful line
            experience_lines = [l.strip('• ').strip() for l in experience.split(
                '\n') if l.strip() and l.strip() != 'Experience:']
            if experience_lines:
                experience = experience_lines[0][:100]  # Limit length
            break

    job_data = {
        'job_position_name': job_position,
        'educational_requirements': education,
        'experience_requirement': experience,
        'full_text': content
    }

    return job_data


def parse_resume_file(filepath):
    """
    Parse a resume text file and extract structured information.
    Returns a dictionary with resume details.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract career objective
    objective = ""
    objective_patterns = [
        r"OBJECTIVE:?\s*(.*?)(?=\n\n|\nEDUCATION:|\nTECHNICAL SKILLS:|\nPROFESSIONAL EXPERIENCE:|$)",
        r"SUMMARY:?\s*(.*?)(?=\n\n|\nEDUCATION:|\nTECHNICAL SKILLS:|\nPROFESSIONAL EXPERIENCE:|$)",
    ]
    for pattern in objective_patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            objective = match.group(1).strip()
            break

    # Extract skills section
    skills = ""
    skills_patterns = [
        r"TECHNICAL SKILLS:?\s*(.*?)(?=\n\n[A-Z]|\nPROFESSIONAL EXPERIENCE:|\nPROJECTS:|\nCERTIFICATIONS:|$)",
        r"SKILLS:?\s*(.*?)(?=\n\n[A-Z]|\nPROFESSIONAL EXPERIENCE:|\nPROJECTS:|\nCERTIFICATIONS:|$)",
    ]
    for pattern in skills_patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            skills = match.group(1).strip()
            break

    # Extract experience/responsibilities
    responsibilities = ""
    exp_patterns = [
        r"PROFESSIONAL EXPERIENCE:?\s*(.*?)(?=\n\nPROJECTS:|\nCERTIFICATIONS:|\nEDUCATION:|\nPUBLICATIONS:|$)",
        r"EXPERIENCE:?\s*(.*?)(?=\n\nPROJECTS:|\nCERTIFICATIONS:|\nEDUCATION:|\nPUBLICATIONS:|$)",
    ]
    for pattern in exp_patterns:
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            responsibilities = match.group(1).strip()
            break

    resume_data = {
        'career_objective': objective,
        'skills': skills,
        'responsibilities': responsibilities,
        'full_text': content
    }

    return resume_data


def preprocess_for_prediction(job_data, resume_data, vectorizer, X_columns):
    """
    Preprocess job and resume data to match the training format.
    Returns a DataFrame ready for prediction.
    """
    # Combine text fields from resume (same as training)
    combined_text = f"{resume_data['career_objective']} {resume_data['skills']} {resume_data['responsibilities']}"

    # DEBUG: Print what we're sending to TF-IDF
    # print(f"    [DEBUG] Combined text for TF-IDF: {combined_text[:200]}...")

    # Create input dataframe matching training structure
    input_df = pd.DataFrame([{
        '﻿job_position_name': job_data['job_position_name'],
        'educationaL_requirements': job_data['educational_requirements'],
        'experiencere_requirement': job_data['experience_requirement'],
        'combined_text': combined_text
    }])

    # Apply TF-IDF transformation
    tfidf_matrix = vectorizer.transform(input_df['combined_text'].fillna(''))

    # DEBUG: Check TF-IDF output
    # print(f"    [DEBUG] TF-IDF matrix shape: {tfidf_matrix.shape}, non-zero: {tfidf_matrix.nnz}")

    # Get categorical columns (excluding combined_text)
    categorical_cols = input_df.select_dtypes(
        include='object').columns.tolist()
    if 'combined_text' in categorical_cols:
        categorical_cols.remove('combined_text')

    # One-hot encode categorical features
    if len(categorical_cols) > 0:
        X_categorical = pd.get_dummies(
            input_df[categorical_cols], dummy_na=False)
    else:
        X_categorical = pd.DataFrame(index=input_df.index)

    # Convert TF-IDF to DataFrame
    X_tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=input_df.index)

    # CRITICAL: Convert column names to strings to match training data
    X_tfidf_df.columns = [str(c) for c in X_tfidf_df.columns]

    # Concatenate features
    X_processed = pd.concat([X_categorical, X_tfidf_df], axis=1)

    # DEBUG: Check combined features before reindex
    # print(f"    [DEBUG] Before reindex - shape: {X_processed.shape}, non-zero: {(X_processed != 0).sum().sum()}")

    # Align columns with training data (use reindex for efficiency)
    X_processed = X_processed.reindex(columns=X_columns, fill_value=0)

    # DEBUG: Check after reindex
    # print(f"    [DEBUG] After reindex - shape: {X_processed.shape}, non-zero: {(X_processed != 0).sum().sum()}")

    return X_processed


def predict_match_score(job_data, resume_data, model, vectorizer, X_columns, debug=False):
    """
    Predict match score for a resume against a job posting.
    Returns: float (predicted match score)
    """
    X = preprocess_for_prediction(job_data, resume_data, vectorizer, X_columns)
    score = model.predict(X)[0]

    if debug:
        print(
            f"  DEBUG - Combined text length: {len(resume_data['career_objective']) + len(resume_data['skills']) + len(resume_data['responsibilities'])}")
        print(
            f"  DEBUG - Objective snippet: {resume_data['career_objective'][:100]}...")
        print(f"  DEBUG - Skills snippet: {resume_data['skills'][:100]}...")
        print(f"  DEBUG - Feature vector shape: {X.shape}")

        # Count non-zero features by type
        non_zero_mask = (X != 0).values[0]
        non_zero_count = non_zero_mask.sum()

        # Categorical features are the first ~66, rest are TF-IDF
        cat_feature_count = sum(1 for col in X.columns if col.startswith(
            ('job_position_name_', 'educationaL_requirements_', 'experiencere_requirement_')))
        non_zero_cat = non_zero_mask[:cat_feature_count].sum()
        non_zero_tfidf = non_zero_mask[cat_feature_count:].sum()

        print(f"  DEBUG - Non-zero features: {non_zero_count} total")
        print(f"           - Categorical: {non_zero_cat}/{cat_feature_count}")
        print(
            f"           - TF-IDF: {non_zero_tfidf}/{len(X.columns) - cat_feature_count}")

        if non_zero_tfidf > 0:
            # Show some matching TF-IDF terms
            tfidf_features = X.columns[cat_feature_count:]
            tfidf_vals = X.values[0][cat_feature_count:]
            top_tfidf_idx = tfidf_vals.argsort()[-5:][::-1]
            print(f"  DEBUG - Top TF-IDF features:")
            for idx in top_tfidf_idx:
                if tfidf_vals[idx] > 0:
                    print(f"           - Feature {idx}: {tfidf_vals[idx]:.4f}")

    return score


def main():
    print("=" * 80)
    print("RESUME MATCHING TEST - GENERAL IMPLEMENTATION")
    print("=" * 80)
    print()

    # Load model artifacts
    model, vectorizer, X_columns = load_artifacts()

    # Define paths
    samples_dir = Path('samples')
    job_file = samples_dir / 'sample_job.txt'

    # Check if samples directory exists
    if not samples_dir.exists():
        print(f"❌ Error: 'samples' directory not found!")
        print(f"   Expected location: {samples_dir.resolve()}")
        return

    # Read job description
    if not job_file.exists():
        print(f"❌ Error: Job file not found!")
        print(f"   Expected location: {job_file.resolve()}")
        return

    print(f"📋 Reading job description from: {job_file.name}")
    job_data = parse_job_file(job_file)
    print(f"   Position: {job_data['job_position_name']}")
    print(f"   Education: {job_data['educational_requirements'][:80]}...")
    print(f"   Experience: {job_data['experience_requirement'][:80]}...")
    print()

    # Find all resume files
    resume_files = sorted(samples_dir.glob('sample_resume*.txt'))

    if not resume_files:
        print(f"❌ Error: No resume files found in {samples_dir}")
        print("   Expected files: sample_resume.txt, sample_resume2.txt, etc.")
        return

    print(f"📄 Found {len(resume_files)} resume(s) to test")
    print()

    # Test each resume
    results = []

    for resume_file in resume_files:
        print(f"Testing: {resume_file.name}...")

        # Parse resume
        resume_data = parse_resume_file(resume_file)

        # Predict match score (with debug for first resume)
        score = predict_match_score(
            job_data, resume_data, model, vectorizer, X_columns, debug=True)

        # Extract candidate name (first line of resume)
        with open(resume_file, 'r') as f:
            first_line = f.readline().strip()
        candidate_name = first_line if first_line else resume_file.stem

        results.append({
            'file': resume_file.name,
            'candidate': candidate_name,
            'score': score
        })

        print(f"  Candidate: {candidate_name}")
        print(f"  Match Score: {score:.2f}")
        print()

    # Sort results by score (descending)
    results.sort(key=lambda x: x['score'], reverse=True)

    # Display ranked results
    print("=" * 80)
    print("RANKED RESULTS")
    print("=" * 80)
    print()

    for i, result in enumerate(results, 1):
        rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        print(f"{rank_icon} {result['candidate']}")
        print(f"   Score: {result['score']:.2f}")
        print(f"   File: {result['file']}")

        # Interpretation (scores are on 0-1 scale, multiply by 100 for percentage)
        score_percentage = result['score'] * 100
        if score_percentage >= 80:
            interpretation = "Excellent match! ⭐⭐⭐"
        elif score_percentage >= 60:
            interpretation = "Good match ✓"
        elif score_percentage >= 40:
            interpretation = "Moderate match"
        else:
            interpretation = "Poor match"

        print(f"   Assessment: {interpretation}")
        print()

    # Save results to CSV
    results_df = pd.DataFrame(results)
    output_file = 'test_results.csv'
    results_df.to_csv(output_file, index=False)
    print(f"✓ Results saved to: {output_file}")
    print()


if __name__ == "__main__":
    main()
