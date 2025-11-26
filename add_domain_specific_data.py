"""
Add domain-specific training data to improve cross-domain discrimination
Creates matched and mismatched pairs for Data Science, Marketing, Chef, and other domains
"""
import pandas as pd
import numpy as np

print("=" * 80)
print("📝 ADDING DOMAIN-SPECIFIC TRAINING DATA")
print("=" * 80)

# Load existing data
print("\n📂 Loading existing data...")
df = pd.read_csv('resume_data_augmented_v3.csv', encoding='utf-8-sig')
print(f"   Current rows: {len(df)}")
print(f"   Current columns: {len(df.columns)}")

# Define domain-specific data
# Format: career_objective, skills, education, degree, year, major, company, related_skills, 
#         position, location, responsibilities, job_position, edu_req, exp_req, job_resp, job_skills, score

domain_data = []

# ============================================================================
# DATA SCIENCE DOMAIN - MATCHED PAIRS (High Scores 0.85-0.95)
# ============================================================================

# Data Scientist Resume 1 - Matched with Data Science Job
domain_data.append({
    'career_objective': 'Experienced Data Scientist specializing in machine learning and predictive analytics. Passionate about building scalable ML solutions.',
    'skills': "['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'SQL', 'Pandas', 'NumPy', 'Data Analysis', 'Statistical Modeling', 'Neural Networks', 'NLP', 'Computer Vision', 'Big Data', 'Spark', 'Hadoop', 'AWS', 'Docker']",
    'educational_institution_name': "['Stanford University', 'MIT']",
    'degree_names': "['Master of Science', 'Bachelor of Science']",
    'passing_years': "['2020', '2018']",
    'major_field_of_studies': "['Data Science', 'Computer Science']",
    'professional_company_names': "['Google', 'Facebook']",
    'related_skils_in_job': "[['Machine Learning', 'Deep Learning', 'Python', 'TensorFlow']]",
    'positions': "['Senior Data Scientist', 'Data Scientist']",
    'locations': "['California', 'New York']",
    'responsibilities': 'Build predictive models\nDeploy ML pipelines\nAnalyze large datasets\nA/B testing\nModel optimization\nCollaborate with engineers',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Senior Data Scientist',
    'educationaL_requirements': "Master's or PhD in Computer Science, Statistics, or related field",
    'experiencere_requirement': '5+ years in data science and machine learning',
    'responsibilities.1': 'Machine Learning model development\nPredictive analytics\nBig Data processing\nStatistical analysis\nModel deployment\nData pipeline optimization',
    'skills_required': 'Python\nMachine Learning\nDeep Learning\nTensorFlow\nPyTorch\nSQL\nSpark\nAWS\nStatistical Analysis\nData Visualization',
    'matched_score': 0.92,
    'is_synthetic': False,
    'job_position_name': 'Senior Data Scientist'
})

# Data Scientist Resume 2 - Matched with ML Engineer Job
domain_data.append({
    'career_objective': 'Machine Learning Engineer with expertise in deploying production ML systems. Strong background in deep learning and NLP.',
    'skills': "['Python', 'Deep Learning', 'Neural Networks', 'TensorFlow', 'Keras', 'PyTorch', 'NLP', 'Computer Vision', 'MLOps', 'Docker', 'Kubernetes', 'AWS SageMaker', 'Model Deployment', 'Data Pipelines']",
    'educational_institution_name': "['Carnegie Mellon University']",
    'degree_names': "['Master of Science']",
    'passing_years': "['2019']",
    'major_field_of_studies': "['Machine Learning']",
    'professional_company_names': "['Amazon', 'Microsoft']",
    'related_skils_in_job': "[['Deep Learning', 'TensorFlow', 'Model Deployment']]",
    'positions': "['ML Engineer', 'Data Scientist']",
    'locations': "['Seattle', 'Washington']",
    'responsibilities': 'Deploy ML models to production\nOptimize model performance\nBuild data pipelines\nImplement MLOps practices\nCollaborate with data scientists',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Machine Learning Engineer',
    'educationaL_requirements': "Master's in Computer Science, ML, or related field",
    'experiencere_requirement': '3+ years in ML engineering',
    'responsibilities.1': 'ML model deployment\nProduction systems\nModel optimization\nData pipeline engineering\nMLOps implementation\nSystem scalability',
    'skills_required': 'Python\nTensorFlow\nPyTorch\nDocker\nKubernetes\nAWS\nML Deployment\nData Engineering\nMLOps',
    'matched_score': 0.90,
    'is_synthetic': False,
    'job_position_name': 'Machine Learning Engineer'
})

# Data Analyst Resume - Matched with Data Analyst Job
domain_data.append({
    'career_objective': 'Data Analyst skilled in SQL, Python, and data visualization. Experience in business intelligence and reporting.',
    'skills': "['SQL', 'Python', 'Pandas', 'Data Analysis', 'Data Visualization', 'Tableau', 'PowerBI', 'Excel', 'Statistics', 'Business Intelligence', 'R', 'ETL']",
    'educational_institution_name': "['University of California Berkeley']",
    'degree_names': "['Bachelor of Science']",
    'passing_years': "['2021']",
    'major_field_of_studies': "['Statistics']",
    'professional_company_names': "['Salesforce', 'Startup Inc']",
    'related_skils_in_job': "[['SQL', 'Data Analysis', 'Tableau']]",
    'positions': "['Data Analyst', 'Junior Analyst']",
    'locations': "['San Francisco']",
    'responsibilities': 'Create reports and dashboards\nAnalyze business metrics\nSQL queries\nData visualization\nStakeholder presentations',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Data Analyst',
    'educationaL_requirements': "Bachelor's in Statistics, Mathematics, or related field",
    'experiencere_requirement': '2-3 years in data analysis',
    'responsibilities.1': 'Data analysis\nSQL reporting\nDashboard creation\nBusiness metrics\nData visualization\nStakeholder communication',
    'skills_required': 'SQL\nPython\nTableau\nPowerBI\nExcel\nData Analysis\nStatistics\nBusiness Intelligence',
    'matched_score': 0.88,
    'is_synthetic': False,
    'job_position_name': 'Data Analyst'
})

# ============================================================================
# MARKETING DOMAIN - MATCHED PAIRS (High Scores 0.85-0.95)
# ============================================================================

# Marketing Manager Resume - Matched with Marketing Manager Job
domain_data.append({
    'career_objective': 'Marketing Manager with 7 years experience in digital marketing, brand strategy, and campaign management.',
    'skills': "['Digital Marketing', 'Social Media Marketing', 'Content Marketing', 'SEO', 'Google Ads', 'Facebook Ads', 'Brand Strategy', 'Campaign Management', 'Marketing Analytics', 'Email Marketing', 'Copywriting', 'Market Research', 'Budget Management']",
    'educational_institution_name': "['Northwestern University']",
    'degree_names': "['MBA', 'Bachelor of Arts']",
    'passing_years': "['2018', '2015']",
    'major_field_of_studies': "['Marketing', 'Business Administration']",
    'professional_company_names': "['Coca-Cola', 'Procter & Gamble']",
    'related_skils_in_job': "[['Digital Marketing', 'Campaign Management', 'Brand Strategy']]",
    'positions': "['Marketing Manager', 'Marketing Specialist']",
    'locations': "['Chicago', 'Atlanta']",
    'responsibilities': 'Plan marketing campaigns\nManage social media\nBrand development\nBudget management\nTeam leadership\nROI analysis\nVendor management',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Marketing Manager',
    'educationaL_requirements': "Bachelor's or Master's in Marketing, Business, or related field",
    'experiencere_requirement': '5+ years in marketing',
    'responsibilities.1': 'Marketing campaign management\nBrand strategy\nSocial media management\nBudget planning\nTeam coordination\nVendor management\nROI tracking',
    'skills_required': 'Digital Marketing\nSocial Media Marketing\nSEO\nGoogle Ads\nCampaign Management\nBrand Strategy\nMarketing Analytics\nContent Creation',
    'matched_score': 0.91,
    'is_synthetic': False,
    'job_position_name': 'Marketing Manager'
})

# Social Media Manager Resume - Matched with Social Media Manager Job
domain_data.append({
    'career_objective': 'Social Media Manager specialized in building brand presence across digital platforms. Expert in content strategy and engagement.',
    'skills': "['Social Media Marketing', 'Content Creation', 'Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'TikTok', 'Content Strategy', 'Community Management', 'Influencer Marketing', 'Analytics', 'Copywriting', 'Graphic Design', 'Canva']",
    'educational_institution_name': "['Boston University']",
    'degree_names': "['Bachelor of Arts']",
    'passing_years': "['2019']",
    'major_field_of_studies': "['Communications']",
    'professional_company_names': "['Nike', 'Adidas']",
    'related_skils_in_job': "[['Social Media Marketing', 'Content Creation', 'Community Management']]",
    'positions': "['Social Media Manager', 'Content Coordinator']",
    'locations': "['Portland', 'New York']",
    'responsibilities': 'Manage social media accounts\nCreate engaging content\nCommunity engagement\nInfluencer partnerships\nAnalyze metrics\nPlan content calendar',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Social Media Manager',
    'educationaL_requirements': "Bachelor's in Marketing, Communications, or related field",
    'experiencere_requirement': '3+ years in social media management',
    'responsibilities.1': 'Social media management\nContent creation\nCommunity engagement\nInfluencer marketing\nAnalytics reporting\nContent calendar planning',
    'skills_required': 'Social Media Marketing\nContent Creation\nFacebook\nInstagram\nTwitter\nLinkedIn\nAnalytics\nCopywriting\nCommunity Management',
    'matched_score': 0.89,
    'is_synthetic': False,
    'job_position_name': 'Social Media Manager'
})

# ============================================================================
# CHEF/CULINARY DOMAIN - MATCHED PAIRS (High Scores 0.85-0.95)
# ============================================================================

# Executive Chef Resume - Matched with Executive Chef Job
domain_data.append({
    'career_objective': 'Executive Chef with 15 years experience in fine dining. Specialized in menu development, kitchen management, and team leadership.',
    'skills': "['Culinary Arts', 'Menu Development', 'Kitchen Management', 'Food Safety', 'Recipe Creation', 'Staff Training', 'Inventory Management', 'Cost Control', 'Food Presentation', 'International Cuisine', 'Knife Skills', 'Baking', 'Pastry']",
    'educational_institution_name': "['Culinary Institute of America']",
    'degree_names': "['Culinary Arts Degree']",
    'passing_years': "['2008']",
    'major_field_of_studies': "['Culinary Arts']",
    'professional_company_names': "['Four Seasons Hotel', 'Michelin Star Restaurant']",
    'related_skils_in_job': "[['Culinary Arts', 'Menu Development', 'Kitchen Management']]",
    'positions': "['Executive Chef', 'Head Chef']",
    'locations': "['New York', 'San Francisco']",
    'responsibilities': 'Menu planning and development\nKitchen staff management\nFood quality control\nInventory management\nCost control\nRecipe creation\nFood safety compliance',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Executive Chef',
    'educationaL_requirements': 'Culinary degree from accredited institution',
    'experiencere_requirement': '10+ years culinary experience, 5+ years as head chef',
    'responsibilities.1': 'Menu development\nKitchen management\nStaff supervision\nFood quality control\nInventory management\nCost control\nRecipe development',
    'skills_required': 'Culinary Arts\nMenu Development\nKitchen Management\nFood Safety\nRecipe Creation\nStaff Training\nCost Control\nFood Presentation',
    'matched_score': 0.93,
    'is_synthetic': False,
    'job_position_name': 'Executive Chef'
})

# ============================================================================
# CROSS-DOMAIN MISMATCHES - LOW SCORES (0.10-0.25)
# ============================================================================

# Data Scientist applying to Marketing Manager - MISMATCH
domain_data.append({
    'career_objective': 'Experienced Data Scientist specializing in machine learning and predictive analytics. Passionate about building scalable ML solutions.',
    'skills': "['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'SQL', 'Pandas', 'NumPy', 'Data Analysis', 'Statistical Modeling', 'Neural Networks', 'NLP', 'Computer Vision', 'Big Data', 'Spark', 'Hadoop', 'AWS', 'Docker']",
    'educational_institution_name': "['Stanford University', 'MIT']",
    'degree_names': "['Master of Science', 'Bachelor of Science']",
    'passing_years': "['2020', '2018']",
    'major_field_of_studies': "['Data Science', 'Computer Science']",
    'professional_company_names': "['Google', 'Facebook']",
    'related_skils_in_job': "[['Machine Learning', 'Deep Learning', 'Python', 'TensorFlow']]",
    'positions': "['Senior Data Scientist', 'Data Scientist']",
    'locations': "['California', 'New York']",
    'responsibilities': 'Build predictive models\nDeploy ML pipelines\nAnalyze large datasets\nA/B testing\nModel optimization\nCollaborate with engineers',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Marketing Manager',
    'educationaL_requirements': "Bachelor's or Master's in Marketing, Business, or related field",
    'experiencere_requirement': '5+ years in marketing',
    'responsibilities.1': 'Marketing campaign management\nBrand strategy\nSocial media management\nBudget planning\nTeam coordination\nVendor management\nROI tracking',
    'skills_required': 'Digital Marketing\nSocial Media Marketing\nSEO\nGoogle Ads\nCampaign Management\nBrand Strategy\nMarketing Analytics\nContent Creation',
    'matched_score': 0.15,
    'is_synthetic': True,
    'job_position_name': 'Marketing Manager'
})

# Marketing Manager applying to Data Scientist - MISMATCH
domain_data.append({
    'career_objective': 'Marketing Manager with 7 years experience in digital marketing, brand strategy, and campaign management.',
    'skills': "['Digital Marketing', 'Social Media Marketing', 'Content Marketing', 'SEO', 'Google Ads', 'Facebook Ads', 'Brand Strategy', 'Campaign Management', 'Marketing Analytics', 'Email Marketing', 'Copywriting', 'Market Research', 'Budget Management']",
    'educational_institution_name': "['Northwestern University']",
    'degree_names': "['MBA', 'Bachelor of Arts']",
    'passing_years': "['2018', '2015']",
    'major_field_of_studies': "['Marketing', 'Business Administration']",
    'professional_company_names': "['Coca-Cola', 'Procter & Gamble']",
    'related_skils_in_job': "[['Digital Marketing', 'Campaign Management', 'Brand Strategy']]",
    'positions': "['Marketing Manager', 'Marketing Specialist']",
    'locations': "['Chicago', 'Atlanta']",
    'responsibilities': 'Plan marketing campaigns\nManage social media\nBrand development\nBudget management\nTeam leadership\nROI analysis\nVendor management',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Senior Data Scientist',
    'educationaL_requirements': "Master's or PhD in Computer Science, Statistics, or related field",
    'experiencere_requirement': '5+ years in data science and machine learning',
    'responsibilities.1': 'Machine Learning model development\nPredictive analytics\nBig Data processing\nStatistical analysis\nModel deployment\nData pipeline optimization',
    'skills_required': 'Python\nMachine Learning\nDeep Learning\nTensorFlow\nPyTorch\nSQL\nSpark\nAWS\nStatistical Analysis\nData Visualization',
    'matched_score': 0.12,
    'is_synthetic': True,
    'job_position_name': 'Senior Data Scientist'
})

# Chef applying to Data Scientist - MISMATCH
domain_data.append({
    'career_objective': 'Executive Chef with 15 years experience in fine dining. Specialized in menu development, kitchen management, and team leadership.',
    'skills': "['Culinary Arts', 'Menu Development', 'Kitchen Management', 'Food Safety', 'Recipe Creation', 'Staff Training', 'Inventory Management', 'Cost Control', 'Food Presentation', 'International Cuisine', 'Knife Skills', 'Baking', 'Pastry']",
    'educational_institution_name': "['Culinary Institute of America']",
    'degree_names': "['Culinary Arts Degree']",
    'passing_years': "['2008']",
    'major_field_of_studies': "['Culinary Arts']",
    'professional_company_names': "['Four Seasons Hotel', 'Michelin Star Restaurant']",
    'related_skils_in_job': "[['Culinary Arts', 'Menu Development', 'Kitchen Management']]",
    'positions': "['Executive Chef', 'Head Chef']",
    'locations': "['New York', 'San Francisco']",
    'responsibilities': 'Menu planning and development\nKitchen staff management\nFood quality control\nInventory management\nCost control\nRecipe creation\nFood safety compliance',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Senior Data Scientist',
    'educationaL_requirements': "Master's or PhD in Computer Science, Statistics, or related field",
    'experiencere_requirement': '5+ years in data science and machine learning',
    'responsibilities.1': 'Machine Learning model development\nPredictive analytics\nBig Data processing\nStatistical analysis\nModel deployment\nData pipeline optimization',
    'skills_required': 'Python\nMachine Learning\nDeep Learning\nTensorFlow\nPyTorch\nSQL\nSpark\nAWS\nStatistical Analysis\nData Visualization',
    'matched_score': 0.08,
    'is_synthetic': True,
    'job_position_name': 'Senior Data Scientist'
})

# Chef applying to Marketing Manager - MISMATCH
domain_data.append({
    'career_objective': 'Executive Chef with 15 years experience in fine dining. Specialized in menu development, kitchen management, and team leadership.',
    'skills': "['Culinary Arts', 'Menu Development', 'Kitchen Management', 'Food Safety', 'Recipe Creation', 'Staff Training', 'Inventory Management', 'Cost Control', 'Food Presentation', 'International Cuisine', 'Knife Skills', 'Baking', 'Pastry']",
    'educational_institution_name': "['Culinary Institute of America']",
    'degree_names': "['Culinary Arts Degree']",
    'passing_years': "['2008']",
    'major_field_of_studies': "['Culinary Arts']",
    'professional_company_names': "['Four Seasons Hotel', 'Michelin Star Restaurant']",
    'related_skils_in_job': "[['Culinary Arts', 'Menu Development', 'Kitchen Management']]",
    'positions': "['Executive Chef', 'Head Chef']",
    'locations': "['New York', 'San Francisco']",
    'responsibilities': 'Menu planning and development\nKitchen staff management\nFood quality control\nInventory management\nCost control\nRecipe creation\nFood safety compliance',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Marketing Manager',
    'educationaL_requirements': "Bachelor's or Master's in Marketing, Business, or related field",
    'experiencere_requirement': '5+ years in marketing',
    'responsibilities.1': 'Marketing campaign management\nBrand strategy\nSocial media management\nBudget planning\nTeam coordination\nVendor management\nROI tracking',
    'skills_required': 'Digital Marketing\nSocial Media Marketing\nSEO\nGoogle Ads\nCampaign Management\nBrand Strategy\nMarketing Analytics\nContent Creation',
    'matched_score': 0.10,
    'is_synthetic': True,
    'job_position_name': 'Marketing Manager'
})

# Data Scientist applying to Chef - MISMATCH
domain_data.append({
    'career_objective': 'Experienced Data Scientist specializing in machine learning and predictive analytics. Passionate about building scalable ML solutions.',
    'skills': "['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'SQL', 'Pandas', 'NumPy', 'Data Analysis', 'Statistical Modeling', 'Neural Networks', 'NLP', 'Computer Vision', 'Big Data', 'Spark', 'Hadoop', 'AWS', 'Docker']",
    'educational_institution_name': "['Stanford University', 'MIT']",
    'degree_names': "['Master of Science', 'Bachelor of Science']",
    'passing_years': "['2020', '2018']",
    'major_field_of_studies': "['Data Science', 'Computer Science']",
    'professional_company_names': "['Google', 'Facebook']",
    'related_skils_in_job': "[['Machine Learning', 'Deep Learning', 'Python', 'TensorFlow']]",
    'positions': "['Senior Data Scientist', 'Data Scientist']",
    'locations': "['California', 'New York']",
    'responsibilities': 'Build predictive models\nDeploy ML pipelines\nAnalyze large datasets\nA/B testing\nModel optimization\nCollaborate with engineers',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Executive Chef',
    'educationaL_requirements': 'Culinary degree from accredited institution',
    'experiencere_requirement': '10+ years culinary experience, 5+ years as head chef',
    'responsibilities.1': 'Menu development\nKitchen management\nStaff supervision\nFood quality control\nInventory management\nCost control\nRecipe development',
    'skills_required': 'Culinary Arts\nMenu Development\nKitchen Management\nFood Safety\nRecipe Creation\nStaff Training\nCost Control\nFood Presentation',
    'matched_score': 0.09,
    'is_synthetic': True,
    'job_position_name': 'Executive Chef'
})

# Marketing Manager applying to Chef - MISMATCH
domain_data.append({
    'career_objective': 'Marketing Manager with 7 years experience in digital marketing, brand strategy, and campaign management.',
    'skills': "['Digital Marketing', 'Social Media Marketing', 'Content Marketing', 'SEO', 'Google Ads', 'Facebook Ads', 'Brand Strategy', 'Campaign Management', 'Marketing Analytics', 'Email Marketing', 'Copywriting', 'Market Research', 'Budget Management']",
    'educational_institution_name': "['Northwestern University']",
    'degree_names': "['MBA', 'Bachelor of Arts']",
    'passing_years': "['2018', '2015']",
    'major_field_of_studies': "['Marketing', 'Business Administration']",
    'professional_company_names': "['Coca-Cola', 'Procter & Gamble']",
    'related_skils_in_job': "[['Digital Marketing', 'Campaign Management', 'Brand Strategy']]",
    'positions': "['Marketing Manager', 'Marketing Specialist']",
    'locations': "['Chicago', 'Atlanta']",
    'responsibilities': 'Plan marketing campaigns\nManage social media\nBrand development\nBudget management\nTeam leadership\nROI analysis\nVendor management',
    'extra_curricular_activity_types': '',
    'online_links': '',
    'issue_dates': '',
    'expiry_dates': '',
    '﻿job_position_name': 'Executive Chef',
    'educationaL_requirements': 'Culinary degree from accredited institution',
    'experiencere_requirement': '10+ years culinary experience, 5+ years as head chef',
    'responsibilities.1': 'Menu development\nKitchen management\nStaff supervision\nFood quality control\nInventory management\nCost control\nRecipe development',
    'skills_required': 'Culinary Arts\nMenu Development\nKitchen Management\nFood Safety\nRecipe Creation\nStaff Training\nCost Control\nFood Presentation',
    'matched_score': 0.11,
    'is_synthetic': True,
    'job_position_name': 'Executive Chef'
})

# Create DataFrame from new data
new_df = pd.DataFrame(domain_data)

# Append to existing data
print(f"\n➕ Adding {len(new_df)} new domain-specific rows...")
print(f"   - Matched pairs (high scores): {len(new_df[new_df['matched_score'] > 0.8])}")
print(f"   - Mismatched pairs (low scores): {len(new_df[new_df['matched_score'] < 0.2])}")

combined_df = pd.concat([df, new_df], ignore_index=True)

# Save the enhanced dataset
output_file = 'resume_data_augmented_v4.csv'
combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n💾 Saved enhanced dataset to: {output_file}")
print(f"   Total rows: {len(combined_df)}")
print(f"   New rows added: {len(new_df)}")

# Show statistics
print(f"\n📊 Score Distribution:")
print(combined_df['matched_score'].describe())

print(f"\n📊 By is_synthetic:")
print(combined_df.groupby('is_synthetic')['matched_score'].agg(['mean', 'count', 'min', 'max']))

print("\n" + "=" * 80)
print("✅ DOMAIN-SPECIFIC DATA ADDED SUCCESSFULLY")
print("=" * 80)
print("\n💡 Next steps:")
print("   1. Review the new data in resume_data_augmented_v4.csv")
print("   2. Retrain the model using this enhanced dataset")
print("   3. Test with the test_resume_job_matching.py script")
