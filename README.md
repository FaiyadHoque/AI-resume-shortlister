# AI Resume-Job Matcher

An AI-powered system to match resumes with job descriptions and predict compatibility scores.

## 🌟 Features

- **Dual Models**: XGBoost (recommended) and Random Forest
- **Advanced NLP**: TF-IDF vectorization with text preprocessing
- **High Accuracy**: Test R² of 0.5231 with only 4.9% overfitting gap
- **Easy Integration**: Simple Python API and CLI

## 📊 Model Performance

| Model | Test R² | Test RMSE | Test MAE | Overfitting Gap |
|-------|---------|-----------|----------|-----------------||
| **XGBoost** | 0.5231 | 0.1158 | 0.0905 | 0.0493 |
| Random Forest | 0.5070 | 0.1177 | 0.0912 | 0.1001 |

**Training Dataset**: 9,542 samples  
**Total Features**: 101  
**Training Date**: 20251110_230129

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-resume-matcher

# Install dependencies
pip install -r requirements.txt
```

### 2. Usage

#### Option A: Command Line

```bash
python predict.py --resume resume.txt --job job_description.txt
```

#### Option B: Python Code

```python
from predict import ResumeJobMatcher

# Initialize the matcher
matcher = ResumeJobMatcher(model_type='xgboost')

# Predict match score
resume_text = "Your resume content here..."
job_text = "Job description here..."

score = matcher.predict(resume_text, job_text)
print(f"Match Score: {score:.2f}/100")
```

#### Option C: Batch Predictions

```python
# Process multiple resume-job pairs
pairs = [
    (resume1, job1),
    (resume2, job2),
    (resume3, job3)
]

scores = matcher.predict_batch(pairs)
for i, score in enumerate(scores):
    print(f"Pair {i+1}: {score:.2f}/100")
```

---

## 📁 Files

- `xgboost_model.pkl` - Trained XGBoost model
- `random_forest_model.pkl` - Trained Random Forest model
- `resume_vectorizer.pkl` - TF-IDF vectorizer for resumes
- `job_vectorizer.pkl` - TF-IDF vectorizer for jobs
- `feature_scaler.pkl` - StandardScaler for features
- `model_metadata.json` - Model configuration and metrics
- `predict.py` - Prediction script
- `requirements.txt` - Python dependencies
- `AI Shortlister.ipynb` - Training notebook

---

## 🎯 Score Interpretation

| Score Range | Recommendation | Meaning |
|-------------|----------------|---------||
| 80-100 | 🟢 Excellent Match | Highly recommended |
| 60-79 | 🟡 Good Match | Recommended |
| 40-59 | 🟠 Moderate Match | Consider with caution |
| 0-39 | 🔴 Poor Match | Not recommended |

---

## 🔧 Technical Details

### Features

**TF-IDF Features** (100 total):
- Resume TF-IDF: 50 features
- Job TF-IDF: 50 features

**Statistical Features**:
- TF-IDF cosine similarity

### Preprocessing

1. Text cleaning and normalization
2. Lowercasing
3. Special character removal
4. Whitespace normalization
5. TF-IDF vectorization (bi-grams)
6. Feature scaling (StandardScaler)

### Model Configuration

**XGBoost** (Recommended):
- `n_estimators=100`
- `max_depth=4` (prevent overfitting)
- `learning_rate=0.05`
- `subsample=0.8`
- L1 and L2 regularization

**Random Forest**:
- `n_estimators=200`
- `max_depth=10`
- `min_samples_split=10`
- `max_features='sqrt'`

---

## 📦 Requirements

- Python 3.7+
- pandas >= 1.3.0
- numpy >= 1.21.0
- scikit-learn >= 1.0.0
- xgboost >= 1.5.0
- joblib >= 1.1.0

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

---

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

## 🙏 Acknowledgments

Built with scikit-learn, XGBoost, and modern NLP techniques.

---

**Made with ❤️ for better recruitment**
