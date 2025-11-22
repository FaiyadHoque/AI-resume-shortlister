"""
Create test resume files in the SAME FORMAT as training data
This ensures fair comparison with the model
"""

# Data Scientist resume - keyword format like training data
data_scientist_keywords = """
Data Scientist seeking opportunities
Python R SQL Java Machine Learning Deep Learning TensorFlow PyTorch Keras Scikit-learn XGBoost 
LightGBM NLP Computer Vision Statistical Analysis A/B Testing Hypothesis Testing 
Data Visualization Tableau Power BI Apache Spark Big Data Hadoop AWS Azure Cloud Docker 
Kubernetes ETL Pipelines Feature Engineering Model Deployment Predictive Modeling 
Time Series Analysis Recommendation Systems Neural Networks CNN RNN LSTM Transformer 
Data Mining Data Cleaning Exploratory Data Analysis Regression Classification Clustering 
Random Forest Gradient Boosting SVM Decision Trees K-Means PCA Dimensionality Reduction
Jupyter Notebook Git GitHub Agile Scrum Master's Degree Computer Science Stanford University
Tech Corp DataTech Solutions
Senior Data Scientist Machine Learning Engineer Data Analyst
Built predictive models Deployed deep learning models Designed ETL pipelines 
Created interactive dashboards Led A/B testing Statistical analysis Product optimization
Developed NLP models Sentiment analysis Text classification Recommendation systems
Collaborative filtering Feature engineering Hyperparameter tuning
"""

# Marketing Manager resume - keyword format like training data  
marketing_keywords = """
Marketing Manager seeking opportunities
Digital Marketing Brand Strategy Social Media Marketing SEO SEM Google Analytics 
Content Marketing Email Marketing Marketing Automation HubSpot Salesforce CRM
Campaign Management Lead Generation Customer Acquisition Social Media Campaigns
Facebook Ads Google Ads Instagram Marketing LinkedIn Marketing Twitter Marketing
Market Research Competitive Analysis Customer Segmentation Target Audience
Brand Development Brand Positioning Marketing Strategy Growth Hacking Conversion Optimization
A/B Testing Landing Pages Marketing Metrics KPIs ROI Marketing Budget
Content Creation Copywriting Blogging Video Marketing Influencer Marketing
Public Relations Media Relations Press Releases Event Marketing Trade Shows
Team Management Project Management Stakeholder Communication Cross-functional Collaboration
Bachelor's Degree Marketing State University Marketing Agency Tech Startup
Marketing Manager Social Media Manager Content Marketing Manager Brand Manager
Managed social media campaigns Developed marketing strategies Increased brand awareness
Generated qualified leads Optimized conversion rates Analyzed marketing metrics
Created compelling content Coordinated with design teams Managed marketing budget
"""

# Data Science Job - keyword format like training data
job_keywords = """
Data Scientist Machine Learning Engineer
Bachelor's Master's PhD Computer Science Data Science Statistics Mathematics
3+ years 5+ years experience
Machine Learning Deep Learning Python R SQL TensorFlow PyTorch Statistical Analysis
Predictive Modeling Data Analysis Big Data Apache Spark Cloud AWS Azure
ETL Pipelines Data Visualization Model Deployment Feature Engineering
A/B Testing Experimentation Statistical Modeling Time Series Analysis NLP
Scikit-learn XGBoost Pandas NumPy Matplotlib Seaborn Jupyter Docker Kubernetes
Hadoop Hive Spark Kafka Database SQL NoSQL MongoDB PostgreSQL
Regression Classification Clustering Neural Networks CNN RNN Decision Trees
Random Forest Gradient Boosting Ensemble Methods Cross-validation Hyperparameter Tuning
Data Cleaning Data Preprocessing Exploratory Data Analysis Feature Selection
Git Version Control Agile Development CI/CD Problem Solving Communication
Collaborate with engineers product teams stakeholders
Build scalable machine learning systems production environment
Analyze large datasets extract insights business decisions
Develop predictive models improve business outcomes
Deploy models production monitor performance
"""

# Save files
with open('data_scientist_resume.txt', 'w', encoding='utf-8') as f:
    f.write(data_scientist_keywords.strip())

with open('marketing_manager_resume.txt', 'w', encoding='utf-8') as f:
    f.write(marketing_keywords.strip())

with open('data_science_job.txt', 'w', encoding='utf-8') as f:
    f.write(job_keywords.strip())

print("✅ Created test files in training data format:")
print("   - data_scientist_resume.txt")
print("   - marketing_manager_resume.txt")
print("   - data_science_job.txt")
print("\nThese files now match the space-separated keyword format used in training!")
