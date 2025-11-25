
import google.generativeai as genai
import os
import re

# Setup Gemini
genai.configure(api_key="AIzaSyCc-3z0OrRIBE3iUAO3TYmiOZ7RfXTZv88")
model = genai.GenerativeModel('gemini-2.5-flash')

def condense_job_posting(job_text):
    prompt = f"""
    Extract and condense the following job posting into a highly compressed skills-focused format.
    
    RULES:
    1. Remove ALL bullet points, symbols, and formatting
    2. Remove all stopwords, emotive language, and descriptive phrases
    3. Extract ONLY technical skills, qualifications, responsibilities, and key requirements
    4. Format as continuous plain text with no line breaks or bullets
    5. Combine everything into a single paragraph with spaces between keywords
    6. Include: technologies, frameworks, methodologies, job functions, education requirements
    7. Exclude: company descriptions, "about us", motivational language, full sentences
    
    JOB POSTING:
    {job_text}
    
    CONDENSED OUTPUT (continuous text only):
    """
    
    response = model.generate_content(prompt)
    
    # Additional cleanup to ensure no bullets or line breaks
    condensed = response.text.strip()
    
    # Remove any remaining bullet points, asterisks, or special characters
    condensed = re.sub(r'[•\-\*▪➢⦿]', ' ', condensed)  # Remove bullet symbols
    condensed = re.sub(r'\s+', ' ', condensed)  # Replace multiple spaces with single space
    condensed = condensed.replace('\n', ' ')  # Remove line breaks
    
    return condensed.strip()

# Read input from file
try:
    with open('b.txt', 'r', encoding='utf-8') as file:
        job_text = file.read()
    
    # Process the text
    result = condense_job_posting(job_text)
    
    # Save output to file
    with open('bb.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(result)
    
    print(" Processing complete! Output saved to 'sr5.txt'")
    print(f"Output: {result}")
    
except FileNotFoundError:
    print(" Error: sample_resume5.txt file not found")
except Exception as e:
    print(f" Error: {e}")