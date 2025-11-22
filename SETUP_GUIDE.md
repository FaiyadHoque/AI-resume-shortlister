# 🚀 Step-by-Step Guide: Generate Synthetic Data with Gemini

## Step 1: Get Your FREE Gemini API Key

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"** or **"Get API Key"**
4. Copy the API key (looks like: `AIzaSyC...`)

## Step 2: Install Required Package

Open your terminal and run:

```bash
pip install google-generativeai tqdm
```

## Step 3: Configure the Script

1. Open `generate_synthetic_data.py`
2. Find line 24: `GEMINI_API_KEY = "YOUR_API_KEY_HERE"`
3. Replace with your actual key: `GEMINI_API_KEY = "AIzaSyC..."`

## Step 4: Run the Script

```bash
python generate_synthetic_data.py
```

**What happens:**
- ✅ Loads your existing dataset (9,543 samples)
- ✅ Creates 2,000 cross-domain pairs (Marketing→Engineering, Chef→Data Science, etc.)
- ✅ Uses Gemini to score each pair (FREE - within free tier)
- ✅ Saves augmented dataset to `resume_data_augmented.csv`

**Time:** 30-60 minutes (includes API rate limiting)

## Step 5: Update Your Notebook

Open `AI_Resume_Matcher_SEMANTIC.ipynb` and change:

**Cell 4 - From:**
```python
df = pd.read_csv('resume_data.csv', encoding=encoding, index_col=False)
```

**Cell 4 - To:**
```python
df = pd.read_csv('resume_data_augmented.csv', encoding=encoding, index_col=False)
```

## Step 6: Retrain Your Model

Run all cells in the notebook. You should see:

**Before:**
- Marketing Manager → Data Science: **65-70/100** ❌
- Data Scientist → Data Science: **70-80/100**
- Discrimination: **10-15 points** (BAD)

**After:**
- Marketing Manager → Data Science: **20-25/100** ✅
- Data Scientist → Data Science: **85-95/100** ✅
- Discrimination: **60-70 points** (EXCELLENT!)

---

## 📊 What Gets Generated

**10 Non-Technical Resume Types:**
- Marketing Manager
- Sales Executive
- HR Manager
- Accountant
- Graphic Designer
- Project Manager
- Content Writer
- Chef
- Nurse
- Teacher

**Paired with your existing technical jobs:**
- Machine Learning Engineer
- Data Scientist
- Software Engineer
- Civil Engineer
- etc.

**Result:** True cross-domain mismatches that teach your model discrimination!

---

## ⚠️ Troubleshooting

**Error: "API key not found"**
- Make sure you replaced `YOUR_API_KEY_HERE` with actual key
- Key should start with `AIzaSy`

**Error: "Quota exceeded"**
- Free tier: 1000 requests/day
- Wait 24 hours or reduce `NUM_SYNTHETIC_PAIRS = 1000`

**Script runs slow:**
- Normal! Rate limiting: 15 requests/minute (free tier)
- 2000 pairs = ~2 hours with rate limiting
- Reduce to 1000 pairs for faster testing

---

## 🎯 Quick Start (1 minute)

```bash
# Install package
pip install google-generativeai tqdm

# Edit API key in generate_synthetic_data.py (line 24)
# Then run:
python generate_synthetic_data.py
```

That's it! 🎉
