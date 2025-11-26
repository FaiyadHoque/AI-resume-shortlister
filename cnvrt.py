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
    1. Extract ONLY: technical skills, qualifications, requirements, tools, technologies, job responsibilities
    2. Remove: company names, company descriptions, "about us", motivational text, benefits, salary info
    3. Format as comma-separated phrases (e.g., "Python, Machine Learning, 5 years experience, Bachelor's degree")
    4. Use commas between different skills/requirements
    5. Keep it concise - focus on keywords and essential qualifications
    6. NO bullet points, NO line breaks, NO full sentences
    7. Group related items together naturally
    
    Example output format:
    "Marketing Manager, digital marketing strategy, 5+ years experience, SEO, SEM, Google Analytics, HubSpot, social media campaigns, content marketing, Bachelor's degree Marketing, team leadership, budget management, data analysis, campaign optimization"
    
    JOB POSTING:
    {job_text}
    
    CONDENSED OUTPUT (comma-separated keywords only):
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
    1. Extract ONLY: job titles, skills, technologies, tools, years of experience, education, certifications
    2. Remove: company names, addresses, phone numbers, emails, objective statements, personal info
    3. Format as comma-separated phrases (e.g., "Executive Chef, 10 years experience, menu development, kitchen management")
    4. Use commas between different skills/qualifications
    5. Keep it concise - focus on keywords and essential qualifications
    6. NO bullet points, NO line breaks, NO full sentences
    7. Group related items together naturally
    
    Example output format:
    "Executive Chef, 10 years culinary arts, menu development, kitchen management, food safety, recipe creation, Bachelor's Degree Culinary Arts, ServSafe certified, team leadership, inventory management"
    
    RESUME:
    {resume_text}
    
    CONDENSED OUTPUT (comma-separated keywords only):
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