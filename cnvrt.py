"""
Text Converter for AI Resume Shortlister
Converts job descriptions and resumes into model-ready format using Gemini AI
"""

import google.generativeai as genai
import os
import re

# Setup Gemini
genai.configure(api_key="AIzaSyCc-3z0OrRIBE3iUAO3TYmiOZ7RfXTZv88")
model = genai.GenerativeModel('gemini-2.5-flash')


def condense_job_posting(job_text: str) -> str:
    """
    Convert job description to model-ready format
    
    Args:
        job_text: Raw job description text
    
    Returns:
        Condensed text suitable for model input
    """
    prompt = f"""
    Extract and condense the following job posting into a clean, comma-separated format.
    
    RULES:
    1. PRIORITIZE: Technical skills, software/tools, domain-specific technologies, industry-specific knowledge
    2. INCLUDE: Job title, years of experience, specific certifications, education requirements, technical qualifications
    3. MINIMIZE: Generic soft skills (leadership, communication, teamwork) - only include if specifically required
    4. Remove: company names, company descriptions, "about us", motivational text, benefits, salary info
    5. Format as comma-separated phrases emphasizing TECHNICAL and DOMAIN-SPECIFIC terms
    6. NO bullet points, NO line breaks, NO full sentences
    
    Example output format:
    "Marketing Manager, digital marketing, 5+ years marketing experience, SEO specialist, SEM campaigns, Google Analytics expert, HubSpot CRM, social media advertising, Facebook Ads, LinkedIn Ads, content marketing automation, email marketing platforms, web analytics tools, marketing automation software, Bachelor's degree Marketing, Google Analytics certified, paid advertising campaigns"
    
    JOB POSTING:
    {job_text}
    
    CONDENSED OUTPUT (comma-separated keywords, emphasize technical/domain-specific terms):
    """
    
    response = model.generate_content(prompt)
    
    # Additional cleanup to ensure no bullets or line breaks
    condensed = response.text.strip()
    
    # Remove any remaining bullet points, asterisks, or special characters
    condensed = re.sub(r'[•\-\*▪➢⦿]', ' ', condensed)  # Remove bullet symbols
    condensed = re.sub(r'\s+', ' ', condensed)  # Replace multiple spaces with single space
    condensed = condensed.replace('\n', ' ')  # Remove line breaks
    
    return condensed.strip()


def condense_resume(resume_text: str) -> str:
    """
    Convert resume to model-ready format
    
    Args:
        resume_text: Raw resume text
    
    Returns:
        Condensed text suitable for model input
    """
    prompt = f"""
    Extract and condense the following resume into a clean, comma-separated format.
    
    RULES:
    1. PRIORITIZE: Job titles, technical skills, domain-specific expertise, specialized tools/software, industry-specific techniques
    2. INCLUDE: Years of experience in specific roles, technical certifications, specialized education, technical competencies
    3. MINIMIZE: Generic soft skills (leadership, communication, teamwork) - only include if it's a key qualification
    4. Remove: company names, addresses, phone numbers, emails, objective statements, personal info
    5. Format as comma-separated phrases emphasizing TECHNICAL and DOMAIN-SPECIFIC terms
    6. NO bullet points, NO line breaks, NO full sentences
    
    Example output format:
    "Executive Chef, 10 years culinary experience, French cuisine specialist, Italian cooking techniques, menu engineering, culinary arts degree, ServSafe certified, HACCP certified, sous vide cooking, molecular gastronomy, pastry techniques, butchery skills, wine pairing expertise"
    
    RESUME:
    {resume_text}
    
    CONDENSED OUTPUT (comma-separated keywords, emphasize technical/domain-specific terms):
    """
    
    response = model.generate_content(prompt)
    
    # Additional cleanup
    condensed = response.text.strip()
    condensed = re.sub(r'[•\-\*▪➢⦿]', ' ', condensed)  # Remove bullet symbols
    condensed = re.sub(r'\s+', ' ', condensed)  # Replace multiple spaces with single space
    condensed = condensed.replace('\n', ' ')  # Remove line breaks
    
    return condensed.strip()


def convert_from_file(input_file: str, output_file: str, conversion_type: str = 'job'):
    """
    Convert text from file
    
    Args:
        input_file: Path to input file
        output_file: Path to output file
        conversion_type: 'job' or 'resume'
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Process based on type
        if conversion_type == 'job':
            result = condense_job_posting(text)
        elif conversion_type == 'resume':
            result = condense_resume(text)
        else:
            raise ValueError("conversion_type must be 'job' or 'resume'")
        
        # Save output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"✅ Processing complete! Output saved to '{output_file}'")
        return result
        
    except FileNotFoundError:
        print(f"❌ Error: {input_file} file not found")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


# Command-line usage (optional)
if __name__ == "__main__":
    # Example: convert job description from b.txt to bb.txt
    try:
        with open('b.txt', 'r', encoding='utf-8') as file:
            job_text = file.read()
        
        result = condense_job_posting(job_text)
        
        with open('bb.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(result)
        
        print("✅ Processing complete! Output saved to 'bb.txt'")
        print(f"Output: {result[:200]}...")
        
    except FileNotFoundError:
        print("❌ Error: b.txt file not found")
    except Exception as e:
        print(f"❌ Error: {e}")