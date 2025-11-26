"""
Generate 1000+ domain-specific training examples with clear matched and mismatched pairs
Creates diverse examples across Data Science, Marketing, Chef, Software Engineering, and other domains
"""
import pandas as pd
import numpy as np
import random

print("=" * 80)
print("📝 GENERATING 1000+ DOMAIN-SPECIFIC TRAINING EXAMPLES")
print("=" * 80)

# Load existing data
print("\n📂 Loading existing data...")
df = pd.read_csv('resume_data_augmented_v4.csv', encoding='utf-8-sig')
print(f"   Current rows: {len(df)}")

# ============================================================================
# DEFINE DOMAIN TEMPLATES
# ============================================================================

# Data Science Domain
data_science_resumes = [
    {
        'objective': 'Data Scientist with {years} years in machine learning and predictive analytics',
        'skills': ['Python', 'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'SQL', 'Pandas', 'NumPy', 'Statistical Analysis', 'Neural Networks', 'NLP', 'Computer Vision', 'Spark', 'Hadoop', 'AWS', 'Azure', 'Data Visualization', 'Tableau', 'PowerBI'],
        'education': ['Stanford University', 'MIT', 'Carnegie Mellon', 'UC Berkeley', 'Georgia Tech'],
        'degree': ['Master of Science', 'PhD', 'Bachelor of Science'],
        'major': ['Data Science', 'Computer Science', 'Statistics', 'Mathematics'],
        'companies': ['Google', 'Facebook', 'Amazon', 'Microsoft', 'Netflix', 'Uber'],
        'positions': ['Senior Data Scientist', 'Data Scientist', 'ML Engineer', 'Research Scientist'],
        'responsibilities': 'Build ML models\nDeploy pipelines\nStatistical analysis\nData preprocessing\nModel optimization\nA/B testing\nFeature engineering'
    },
    {
        'objective': 'Machine Learning Engineer specializing in deep learning and production ML systems',
        'skills': ['Python', 'Deep Learning', 'TensorFlow', 'Keras', 'PyTorch', 'MLOps', 'Docker', 'Kubernetes', 'Model Deployment', 'Data Pipelines', 'AWS SageMaker', 'Neural Networks', 'Computer Vision', 'NLP'],
        'education': ['MIT', 'Stanford', 'CMU', 'Berkeley'],
        'degree': ['Master of Science', 'Bachelor of Science'],
        'major': ['Machine Learning', 'Computer Science', 'AI'],
        'companies': ['Apple', 'Google', 'Tesla', 'Amazon', 'Microsoft'],
        'positions': ['ML Engineer', 'Senior ML Engineer', 'AI Engineer'],
        'responsibilities': 'Deploy ML models\nOptimize performance\nBuild pipelines\nMLOps implementation\nModel monitoring\nScalability solutions'
    },
    {
        'objective': 'Data Analyst skilled in business intelligence and data visualization',
        'skills': ['SQL', 'Python', 'Pandas', 'Data Analysis', 'Tableau', 'PowerBI', 'Excel', 'Statistics', 'R', 'Data Visualization', 'Business Intelligence', 'ETL', 'Reporting'],
        'education': ['UC Berkeley', 'University of Michigan', 'NYU', 'Columbia'],
        'degree': ['Bachelor of Science', 'Master of Science'],
        'major': ['Statistics', 'Mathematics', 'Data Analytics', 'Business Analytics'],
        'companies': ['Salesforce', 'LinkedIn', 'Adobe', 'Oracle', 'SAP'],
        'positions': ['Data Analyst', 'Senior Data Analyst', 'Business Analyst'],
        'responsibilities': 'Create dashboards\nSQL reporting\nData analysis\nBusiness metrics\nStakeholder presentations\nETL processes'
    }
]

data_science_jobs = [
    {
        'position': 'Senior Data Scientist',
        'education_req': "Master's or PhD in Computer Science, Statistics, or related field",
        'experience_req': '{years}+ years in data science and machine learning',
        'responsibilities': 'ML model development\nPredictive analytics\nBig Data processing\nStatistical analysis\nModel deployment\nData pipeline optimization\nTeam collaboration',
        'skills': 'Python\nMachine Learning\nDeep Learning\nTensorFlow\nPyTorch\nSQL\nSpark\nAWS\nStatistical Analysis\nData Visualization'
    },
    {
        'position': 'Machine Learning Engineer',
        'education_req': "Master's in Computer Science, ML, or related field",
        'experience_req': '{years}+ years in ML engineering',
        'responsibilities': 'ML model deployment\nProduction systems\nModel optimization\nData pipeline engineering\nMLOps implementation\nSystem scalability',
        'skills': 'Python\nTensorFlow\nPyTorch\nDocker\nKubernetes\nAWS\nML Deployment\nData Engineering\nMLOps'
    },
    {
        'position': 'Data Analyst',
        'education_req': "Bachelor's in Statistics, Mathematics, or related field",
        'experience_req': '{years} years in data analysis',
        'responsibilities': 'Data analysis\nSQL reporting\nDashboard creation\nBusiness metrics\nData visualization\nStakeholder communication',
        'skills': 'SQL\nPython\nTableau\nPowerBI\nExcel\nData Analysis\nStatistics\nBusiness Intelligence'
    }
]

# Marketing Domain
marketing_resumes = [
    {
        'objective': 'Marketing Manager with {years} years in digital marketing and brand strategy',
        'skills': ['Digital Marketing', 'Social Media Marketing', 'SEO', 'Google Ads', 'Facebook Ads', 'Brand Strategy', 'Campaign Management', 'Content Marketing', 'Email Marketing', 'Marketing Analytics', 'Copywriting', 'Market Research', 'Budget Management'],
        'education': ['Northwestern University', 'NYU', 'USC', 'Boston University'],
        'degree': ['MBA', 'Bachelor of Arts', 'Master of Arts'],
        'major': ['Marketing', 'Business Administration', 'Communications'],
        'companies': ['Coca-Cola', 'Procter & Gamble', 'Unilever', 'Nike', 'Apple'],
        'positions': ['Marketing Manager', 'Brand Manager', 'Marketing Director'],
        'responsibilities': 'Campaign management\nBrand strategy\nSocial media management\nBudget planning\nTeam coordination\nROI tracking\nVendor management'
    },
    {
        'objective': 'Social Media Manager specialized in content creation and engagement',
        'skills': ['Social Media Marketing', 'Content Creation', 'Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'TikTok', 'Content Strategy', 'Community Management', 'Influencer Marketing', 'Analytics', 'Copywriting', 'Canva', 'Video Editing'],
        'education': ['Boston University', 'USC', 'Syracuse', 'Columbia'],
        'degree': ['Bachelor of Arts'],
        'major': ['Communications', 'Marketing', 'Media Studies'],
        'companies': ['Nike', 'Adidas', 'Spotify', 'Netflix', 'Airbnb'],
        'positions': ['Social Media Manager', 'Content Manager', 'Digital Marketing Specialist'],
        'responsibilities': 'Social media management\nContent creation\nCommunity engagement\nInfluencer partnerships\nAnalytics reporting\nContent calendar'
    },
    {
        'objective': 'SEO Specialist focused on search engine optimization and organic growth',
        'skills': ['SEO', 'Google Analytics', 'Keyword Research', 'Link Building', 'Content Optimization', 'Technical SEO', 'Google Search Console', 'SEMrush', 'Ahrefs', 'Backlink Analysis'],
        'education': ['University of Texas', 'Florida State', 'Arizona State'],
        'degree': ['Bachelor of Science'],
        'major': ['Marketing', 'Digital Marketing', 'Business'],
        'companies': ['HubSpot', 'Moz', 'SEMrush', 'Shopify'],
        'positions': ['SEO Specialist', 'SEO Manager', 'Digital Marketing Analyst'],
        'responsibilities': 'SEO optimization\nKeyword research\nContent strategy\nLink building\nTechnical audits\nRanking improvement'
    }
]

marketing_jobs = [
    {
        'position': 'Marketing Manager',
        'education_req': "Bachelor's or Master's in Marketing, Business, or related field",
        'experience_req': '{years}+ years in marketing',
        'responsibilities': 'Marketing campaign management\nBrand strategy\nSocial media management\nBudget planning\nTeam coordination\nVendor management\nROI tracking',
        'skills': 'Digital Marketing\nSocial Media Marketing\nSEO\nGoogle Ads\nCampaign Management\nBrand Strategy\nMarketing Analytics\nContent Creation'
    },
    {
        'position': 'Social Media Manager',
        'education_req': "Bachelor's in Marketing, Communications, or related field",
        'experience_req': '{years}+ years in social media management',
        'responsibilities': 'Social media management\nContent creation\nCommunity engagement\nInfluencer marketing\nAnalytics reporting\nContent calendar planning',
        'skills': 'Social Media Marketing\nContent Creation\nFacebook\nInstagram\nTwitter\nLinkedIn\nAnalytics\nCopywriting\nCommunity Management'
    },
    {
        'position': 'SEO Manager',
        'education_req': "Bachelor's in Marketing or related field",
        'experience_req': '{years} years in SEO',
        'responsibilities': 'SEO strategy\nKeyword optimization\nLink building\nContent optimization\nTechnical SEO\nAnalytics tracking',
        'skills': 'SEO\nGoogle Analytics\nKeyword Research\nLink Building\nContent Strategy\nTechnical SEO\nSEMrush\nAhrefs'
    }
]

# Chef/Culinary Domain
chef_resumes = [
    {
        'objective': 'Executive Chef with {years} years in fine dining and menu development',
        'skills': ['Culinary Arts', 'Menu Development', 'Kitchen Management', 'Food Safety', 'Recipe Creation', 'Staff Training', 'Inventory Management', 'Cost Control', 'Food Presentation', 'International Cuisine', 'Knife Skills', 'Baking', 'Pastry'],
        'education': ['Culinary Institute of America', 'Le Cordon Bleu', 'Johnson & Wales'],
        'degree': ['Culinary Arts Degree', 'Certificate'],
        'major': ['Culinary Arts', 'Pastry Arts', 'Hospitality'],
        'companies': ['Four Seasons', 'Ritz-Carlton', 'Hilton', 'Marriott', 'Michelin Restaurant'],
        'positions': ['Executive Chef', 'Head Chef', 'Sous Chef'],
        'responsibilities': 'Menu development\nKitchen management\nStaff supervision\nFood quality control\nInventory management\nCost control\nRecipe development'
    },
    {
        'objective': 'Pastry Chef specialized in desserts and baking',
        'skills': ['Pastry Arts', 'Baking', 'Dessert Creation', 'Chocolate Work', 'Cake Decoration', 'Recipe Development', 'Food Safety', 'Kitchen Management'],
        'education': ['Le Cordon Bleu', 'Culinary Institute of America'],
        'degree': ['Pastry Arts Degree'],
        'major': ['Pastry Arts', 'Baking'],
        'companies': ['Waldorf Astoria', 'French Laundry', 'Bouchon Bakery'],
        'positions': ['Pastry Chef', 'Executive Pastry Chef', 'Sous Chef'],
        'responsibilities': 'Dessert creation\nBaking operations\nRecipe development\nTeam management\nInventory control\nQuality assurance'
    }
]

chef_jobs = [
    {
        'position': 'Executive Chef',
        'education_req': 'Culinary degree from accredited institution',
        'experience_req': '{years}+ years culinary experience',
        'responsibilities': 'Menu development\nKitchen management\nStaff supervision\nFood quality control\nInventory management\nCost control\nRecipe development',
        'skills': 'Culinary Arts\nMenu Development\nKitchen Management\nFood Safety\nRecipe Creation\nStaff Training\nCost Control\nFood Presentation'
    },
    {
        'position': 'Pastry Chef',
        'education_req': 'Culinary or Pastry Arts degree',
        'experience_req': '{years} years pastry experience',
        'responsibilities': 'Dessert creation\nBaking operations\nRecipe development\nTeam management\nInventory control\nQuality standards',
        'skills': 'Pastry Arts\nBaking\nDessert Creation\nRecipe Development\nFood Safety\nKitchen Management\nCake Decoration'
    }
]

# Software Engineering Domain
software_resumes = [
    {
        'objective': 'Software Engineer with {years} years in full-stack development',
        'skills': ['JavaScript', 'Python', 'React', 'Node.js', 'Java', 'SQL', 'Git', 'AWS', 'Docker', 'REST APIs', 'Agile', 'TypeScript', 'MongoDB', 'PostgreSQL'],
        'education': ['MIT', 'Stanford', 'CMU', 'UC Berkeley'],
        'degree': ['Bachelor of Science', 'Master of Science'],
        'major': ['Computer Science', 'Software Engineering'],
        'companies': ['Google', 'Amazon', 'Facebook', 'Microsoft', 'Apple'],
        'positions': ['Senior Software Engineer', 'Software Engineer', 'Full Stack Developer'],
        'responsibilities': 'Software development\nCode review\nSystem design\nAPI development\nDatabase optimization\nDeployment\nBug fixing'
    },
    {
        'objective': 'Frontend Developer specializing in React and modern web technologies',
        'skills': ['JavaScript', 'React', 'TypeScript', 'HTML', 'CSS', 'Redux', 'Next.js', 'Webpack', 'Git', 'Responsive Design', 'UI/UX'],
        'education': ['UC Berkeley', 'University of Washington', 'Georgia Tech'],
        'degree': ['Bachelor of Science'],
        'major': ['Computer Science', 'Web Development'],
        'companies': ['Airbnb', 'Netflix', 'Spotify', 'Twitter'],
        'positions': ['Frontend Developer', 'UI Engineer', 'Web Developer'],
        'responsibilities': 'Frontend development\nUI implementation\nResponsive design\nCode optimization\nCross-browser compatibility\nComponent development'
    }
]

software_jobs = [
    {
        'position': 'Senior Software Engineer',
        'education_req': "Bachelor's or Master's in Computer Science",
        'experience_req': '{years}+ years software development',
        'responsibilities': 'Software development\nSystem design\nCode review\nAPI development\nDatabase design\nDeployment automation\nMentoring',
        'skills': 'JavaScript\nPython\nJava\nReact\nNode.js\nSQL\nAWS\nDocker\nGit\nREST APIs\nAgile'
    },
    {
        'position': 'Frontend Developer',
        'education_req': "Bachelor's in Computer Science or related field",
        'experience_req': '{years} years frontend development',
        'responsibilities': 'Frontend development\nUI implementation\nResponsive design\nPerformance optimization\nCode quality\nCollaboration',
        'skills': 'JavaScript\nReact\nTypeScript\nHTML\nCSS\nRedux\nWebpack\nGit\nUI/UX\nResponsive Design'
    }
]

# ============================================================================
# GENERATE TRAINING DATA
# ============================================================================

def generate_skill_string(skills_list):
    """Convert skills list to string format matching CSV"""
    # Take random subset of skills
    num_skills = random.randint(8, min(15, len(skills_list)))
    selected_skills = random.sample(skills_list, num_skills)
    return str(selected_skills)

def generate_matched_pair(resume_template, job_template, domain_name):
    """Generate a matched resume-job pair with high score"""
    years = random.randint(3, 10)
    
    resume = {
        'career_objective': resume_template['objective'].format(years=years),
        'skills': generate_skill_string(resume_template['skills']),
        'educational_institution_name': str([random.choice(resume_template['education'])]),
        'degree_names': str([random.choice(resume_template['degree'])]),
        'passing_years': str([str(random.randint(2015, 2022))]),
        'major_field_of_studies': str([random.choice(resume_template['major'])]),
        'professional_company_names': str([random.choice(resume_template['companies'])]),
        'related_skils_in_job': str([[random.choice(resume_template['skills'][:5])]]),
        'positions': str([random.choice(resume_template['positions'])]),
        'locations': str([random.choice(['New York', 'California', 'Seattle', 'Boston', 'Chicago'])]),
        'responsibilities': resume_template['responsibilities'],
        'extra_curricular_activity_types': '',
        'online_links': '',
        'issue_dates': '',
        'expiry_dates': '',
        '﻿job_position_name': job_template['position'],
        'educationaL_requirements': job_template['education_req'],
        'experiencere_requirement': job_template['experience_req'].format(years=random.randint(3, 7)),
        'responsibilities.1': job_template['responsibilities'],
        'skills_required': job_template['skills'],
        'matched_score': round(random.uniform(0.85, 0.95), 2),
        'is_synthetic': False,
        'job_position_name': job_template['position']
    }
    return resume

def generate_mismatched_pair(resume_template, job_template, resume_domain, job_domain):
    """Generate a mismatched resume-job pair with low score"""
    years = random.randint(3, 10)
    
    resume = {
        'career_objective': resume_template['objective'].format(years=years),
        'skills': generate_skill_string(resume_template['skills']),
        'educational_institution_name': str([random.choice(resume_template['education'])]),
        'degree_names': str([random.choice(resume_template['degree'])]),
        'passing_years': str([str(random.randint(2015, 2022))]),
        'major_field_of_studies': str([random.choice(resume_template['major'])]),
        'professional_company_names': str([random.choice(resume_template['companies'])]),
        'related_skils_in_job': str([[random.choice(resume_template['skills'][:5])]]),
        'positions': str([random.choice(resume_template['positions'])]),
        'locations': str([random.choice(['New York', 'California', 'Seattle', 'Boston', 'Chicago'])]),
        'responsibilities': resume_template['responsibilities'],
        'extra_curricular_activity_types': '',
        'online_links': '',
        'issue_dates': '',
        'expiry_dates': '',
        '﻿job_position_name': job_template['position'],
        'educationaL_requirements': job_template['education_req'],
        'experiencere_requirement': job_template['experience_req'].format(years=random.randint(3, 7)),
        'responsibilities.1': job_template['responsibilities'],
        'skills_required': job_template['skills'],
        'matched_score': round(random.uniform(0.05, 0.20), 2),
        'is_synthetic': True,
        'job_position_name': job_template['position']
    }
    return resume

# Generate data
new_data = []
target_count = 1000

print(f"\n🔄 Generating {target_count} training examples...")

# Calculate distribution
matched_count = int(target_count * 0.5)  # 50% matched
mismatched_count = target_count - matched_count  # 50% mismatched

# Generate matched pairs
print(f"   Generating {matched_count} matched pairs...")
for i in range(matched_count):
    domain = random.choice(['data_science', 'marketing', 'chef', 'software'])
    
    if domain == 'data_science':
        resume_template = random.choice(data_science_resumes)
        job_template = random.choice(data_science_jobs)
        new_data.append(generate_matched_pair(resume_template, job_template, 'Data Science'))
    elif domain == 'marketing':
        resume_template = random.choice(marketing_resumes)
        job_template = random.choice(marketing_jobs)
        new_data.append(generate_matched_pair(resume_template, job_template, 'Marketing'))
    elif domain == 'chef':
        resume_template = random.choice(chef_resumes)
        job_template = random.choice(chef_jobs)
        new_data.append(generate_matched_pair(resume_template, job_template, 'Chef'))
    else:  # software
        resume_template = random.choice(software_resumes)
        job_template = random.choice(software_jobs)
        new_data.append(generate_matched_pair(resume_template, job_template, 'Software'))
    
    if (i + 1) % 100 == 0:
        print(f"      Generated {i + 1}/{matched_count} matched pairs...")

# Generate mismatched pairs
print(f"   Generating {mismatched_count} mismatched pairs...")
domains = ['data_science', 'marketing', 'chef', 'software']
for i in range(mismatched_count):
    # Pick two different domains
    resume_domain, job_domain = random.sample(domains, 2)
    
    # Get templates
    if resume_domain == 'data_science':
        resume_template = random.choice(data_science_resumes)
    elif resume_domain == 'marketing':
        resume_template = random.choice(marketing_resumes)
    elif resume_domain == 'chef':
        resume_template = random.choice(chef_resumes)
    else:
        resume_template = random.choice(software_resumes)
    
    if job_domain == 'data_science':
        job_template = random.choice(data_science_jobs)
    elif job_domain == 'marketing':
        job_template = random.choice(marketing_jobs)
    elif job_domain == 'chef':
        job_template = random.choice(chef_jobs)
    else:
        job_template = random.choice(software_jobs)
    
    new_data.append(generate_mismatched_pair(resume_template, job_template, resume_domain, job_domain))
    
    if (i + 1) % 100 == 0:
        print(f"      Generated {i + 1}/{mismatched_count} mismatched pairs...")

# Create DataFrame and combine
new_df = pd.DataFrame(new_data)
combined_df = pd.concat([df, new_df], ignore_index=True)

# Save
output_file = 'resume_data_augmented_v4.csv'
combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n💾 Saved enhanced dataset to: {output_file}")
print(f"   Previous rows: {len(df)}")
print(f"   New rows added: {len(new_df)}")
print(f"   Total rows: {len(combined_df)}")

# Statistics
print(f"\n📊 New Data Statistics:")
print(f"   Matched pairs (score > 0.8): {len(new_df[new_df['matched_score'] > 0.8])}")
print(f"   Mismatched pairs (score < 0.2): {len(new_df[new_df['matched_score'] < 0.2])}")

print(f"\n📊 Overall Score Distribution:")
print(combined_df['matched_score'].describe())

print(f"\n📊 By is_synthetic:")
print(combined_df.groupby('is_synthetic')['matched_score'].agg(['mean', 'count', 'min', 'max']))

print("\n" + "=" * 80)
print("✅ 1000 DOMAIN-SPECIFIC EXAMPLES GENERATED SUCCESSFULLY")
print("=" * 80)
print("\n💡 Next steps:")
print("   1. Retrain the model using: AI_Resume_Matcher_SEMANTIC.ipynb")
print("   2. Test with: python test_resume_job_matching.py")
