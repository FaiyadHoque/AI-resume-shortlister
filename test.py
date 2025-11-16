import pickle
import os
import re
import numpy as np

# Load models
def load_models():
    """Load your trained models"""
    models = {}
    try:
        with open('tfidf_vectorizer.pkl', 'rb') as f:
            models['vectorizer'] = pickle.load(f)
        print(" Loaded: tfidf_vectorizer.pkl")
    except Exception as e:
        print(f" Error loading vectorizer: {e}")
        return None
    
    try:
        with open('random_forest_model.pkl', 'rb') as f:
            models['rf_model'] = pickle.load(f)
        print(" Loaded: random_forest_model.pkl")
    except Exception as e:
        print(f" Error loading Random Forest: {e}")
    
    try:
        with open('xgboost_model.pkl', 'rb') as f:
            models['xgb_model'] = pickle.load(f)
        print(" Loaded: xgboost_model.pkl")
    except Exception as e:
        print(f" Error loading XGBoost: {e}")
    
    return models

def read_text_file(file_path):
    """Read a single text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        print(f" Loaded: {file_path}")
        return content
    except Exception as e:
        print(f" Error reading {file_path}: {e}")
        return None

# MATCH THIS EXACTLY TO data_preprocessing.py
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", 
    "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 
    'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 
    'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 
    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 
    'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 
    'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 
    'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', 
    "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 
    'wouldn', "wouldn't"
}

def clean_text(text):
    """IDENTICAL to data_preprocessing.py clean_text function"""
    if not isinstance(text, str):
        return ""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and extra spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove stopwords
    words = text.split()
    filtered_words = [word for word in words if word not in STOPWORDS]
    text = ' '.join(filtered_words)
    
    return text.strip()

def predict_match_score(models, job_text, resume_text):
    """Predict match score — preprocess SAME WAY as training"""
    
    # Combine BEFORE cleaning (same order as training)
    combined_text = job_text + " " + resume_text
    
    # Clean combined text (same function as training)
    cleaned_text = clean_text(combined_text)
    
    # Vectorize using trained TF-IDF
    text_vectorized = models['vectorizer'].transform([cleaned_text])
    
    predictions = {}
    
    # Get prediction from Random Forest
    if 'rf_model' in models:
        rf_score = models['rf_model'].predict(text_vectorized)[0]
        predictions['random_forest'] = max(0.0, min(1.0, float(rf_score)))
    
    # Get prediction from XGBoost
    if 'xgb_model' in models:
        xgb_score = models['xgb_model'].predict(text_vectorized)[0]
        predictions['xgboost'] = max(0.0, min(1.0, float(xgb_score)))
    
    # Ensemble average
    if len(predictions) > 0:
        predictions['ensemble'] = float(np.mean(list(predictions.values())))
    
    return predictions, cleaned_text

def display_single_match(job_file, resume_file, job_text, resume_text, predictions, cleaned_text):
    """Display results for single job-resume match"""
    print("\n" + "="*80)
    print(" SINGLE JOB-RESUME MATCHING RESULT")
    print("="*80)
    
    print(f"\n JOB DESCRIPTION:")
    print(f"   File: {job_file}")
    print(f"   Original preview: {job_text[:200]}{'...' if len(job_text) > 200 else ''}")
    
    print(f"\n RESUME:")
    print(f"   File: {resume_file}")
    print(f"   Original preview: {resume_text[:200]}{'...' if len(resume_text) > 200 else ''}")
    
    print(f"\n CLEANED & COMBINED TEXT (as trained):")
    print(f"   {cleaned_text[:300]}{'...' if len(cleaned_text) > 300 else ''}")
    
    print(f"\n MATCH SCORES:")
    if 'random_forest' in predictions:
        print(f"    Random Forest Score: {predictions['random_forest']:.4f}")
    
    if 'xgboost' in predictions:
        print(f"    XGBoost Score: {predictions['xgboost']:.4f}")
    
    if 'ensemble' in predictions:
        print(f"    Ensemble Score: {predictions['ensemble']:.4f}")
        score = predictions['ensemble']
        if score >= 0.8:
            print(f"    → EXCELLENT MATCH")
        elif score >= 0.6:
            print(f"    → GOOD MATCH")
        elif score >= 0.4:
            print(f"    → MODERATE MATCH")
        else:
            print(f"    → WEAK MATCH")

def main():
    print(" SINGLE JOB-RESUME MATCHING ANALYSIS")
    print("=" * 50)
    
    print("\n LOADING TRAINED MODELS...")
    models = load_models()
    
    if not models or 'vectorizer' not in models:
        print(" Critical error: Could not load models.")
        return
    
    job_file = "sample_job.txt"    
    resume_file = "sample_resume2.txt"          
    
    print(f"\n LOADING YOUR FILES...")
    job_text = read_text_file(job_file)
    resume_text = read_text_file(resume_file)
    
    if job_text is None or resume_text is None:
        print(" Could not load one or both files.")
        return
    
    print(f"\n ANALYZING MATCH...")
    predictions, cleaned_text = predict_match_score(models, job_text, resume_text)
    
    display_single_match(job_file, resume_file, job_text, resume_text, predictions, cleaned_text)
    
    print(f"\n ANALYSIS COMPLETE!")

if __name__ == "__main__":
    main()