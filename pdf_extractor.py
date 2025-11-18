"""
PDF extraction module for extracting structured information from resume PDFs
"""

import re
from pathlib import Path
from typing import Dict, Optional
import PyPDF2


class ResumeExtractor:
    """Extract structured information from resume PDFs"""

    def __init__(self):
        """Initialize extractor"""
        pass

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract raw text from PDF file with better text extraction

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text content
        """
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception as e:
                        print(f"Warning: Could not extract text from page {page_num + 1}: {e}")
                        continue
                
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""

        # Clean up text
        text = text.strip()
        
        # Remove excessive whitespace and normalize
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        
        return text

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text"""
        # More comprehensive email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        
        # Return first valid email found
        for email in matches:
            # Filter out common false positives
            if not any(word in email.lower() for word in ['example', 'test', 'sample']):
                return email
        
        return matches[0] if matches else None

    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text with better pattern matching"""
        # Match various phone formats
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # +1 (123) 456-7890
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (123) 456-7890
            r'\d{3}[-.\s]?\d{4}[-.\s]?\d{4}',  # 123-4567-8901
            r'\+\d{10,15}',  # +12345678901
        ]

        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                phone = match.group(0)
                # Clean up phone number
                phone = re.sub(r'[^\d+()]', '', phone)
                return match.group(0)  # Return original format
        
        return None

    def extract_name(self, text: str) -> str:
        """
        Extract candidate name with improved logic
        """
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return "Unknown"
            
        # Try first few lines
        for i, line in enumerate(lines[:3]):
            line_lower = line.lower()
            
            # Skip lines with these patterns
            skip_patterns = [
                '@',  # Email
                'http',  # URL
                'linkedin',
                'github',
                r'\d{3}[-.\s]?\d{3}',  # Phone
            ]
            
            if any(re.search(pattern, line_lower) for pattern in skip_patterns):
                continue
            
            # Check if line looks like a name (2-4 words, mostly letters)
            words = line.split()
            if 1 <= len(words) <= 4:
                # Check if words are mostly alphabetic
                alpha_words = sum(1 for w in words if w.replace('.', '').replace(',', '').isalpha())
                if alpha_words >= len(words) * 0.7:  # 70% alphabetic
                    # Clean up common title words
                    cleaned = re.sub(r'\b(resume|cv|curriculum vitae)\b', '', line, flags=re.IGNORECASE)
                    cleaned = cleaned.strip()
                    if cleaned:
                        return cleaned[:50]  # Limit length
        
        # Fallback: look for "Name:" label
        name_pattern = r'(?:Name|Full Name):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        match = re.search(name_pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        
        # Last resort: return first line
        first_line = lines[0]
        first_line = re.sub(r'\b(resume|cv|curriculum vitae)\b', '', first_line, flags=re.IGNORECASE)
        return first_line.strip()[:50] if first_line.strip() else "Unknown"

    def extract_section(self, text: str, section_name: str) -> str:
        """
        Extract content from a specific section

        Args:
            text: Full resume text
            section_name: Section to extract (e.g., 'education', 'experience')

        Returns:
            Section content
        """
        # Common section headers
        section_patterns = {
            'objective': r'(?:objective|summary|profile|about)',
            'education': r'(?:education|academic|qualification)',
            'experience': r'(?:experience|employment|work history|professional experience)',
            'skills': r'(?:skills|technical skills|competencies|expertise)',
            'projects': r'(?:projects|portfolio)',
            'certifications': r'(?:certifications?|certificates?|licenses?)',
        }

        pattern = section_patterns.get(section_name.lower())
        if not pattern:
            return ""

        # Find section start
        section_regex = re.compile(rf'\b{pattern}\b', re.IGNORECASE)
        match = section_regex.search(text)

        if not match:
            return ""

        start_pos = match.start()

        # Find next section or end of text
        next_section_pattern = r'\n(?:' + \
            '|'.join(section_patterns.values()) + r')\b'
        next_match = re.search(
            next_section_pattern, text[start_pos + len(match.group()):], re.IGNORECASE)

        if next_match:
            end_pos = start_pos + len(match.group()) + next_match.start()
            section_content = text[start_pos:end_pos]
        else:
            section_content = text[start_pos:]

        # Clean up the section content
        lines = section_content.split('\n')
        
        # Skip the header line if it's still present
        if lines and re.search(pattern, lines[0], re.IGNORECASE):
            lines = lines[1:]
        
        # Remove empty lines and clean whitespace
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        
        # Remove excessive blank lines but preserve structure
        result = '\n'.join(cleaned_lines)
        result = re.sub(r'\n{3,}', '\n\n', result)  # Max 2 consecutive newlines
        
        return result

    def estimate_experience_years(self, experience_text: str) -> int:
        """
        Estimate years of experience from experience section

        Args:
            experience_text: Experience section text

        Returns:
            Estimated years of experience
        """
        # Look for date ranges like "2020 - 2023" or "2020 - Present"
        year_pattern = r'(19|20)\d{2}'
        years = re.findall(year_pattern, experience_text)

        if len(years) >= 2:
            years = [int(y) for y in years]
            # Calculate from earliest to latest year
            min_year = min(years)
            max_year = max(years)

            # If "present" is mentioned, use current year
            if re.search(r'\bpresent\b', experience_text, re.IGNORECASE):
                from datetime import datetime
                max_year = datetime.now().year

            return max_year - min_year

        # Look for explicit mentions like "5+ years" or "3 years of experience"
        exp_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
        match = re.search(exp_pattern, experience_text, re.IGNORECASE)
        if match:
            return int(match.group(1))

        return 0

    def extract_resume_data(self, pdf_path: str) -> Dict:
        """
        Extract all structured information from resume PDF

        Args:
            pdf_path: Path to resume PDF file

        Returns:
            Dictionary with extracted resume data
        """
        # Extract raw text
        text = self.extract_text_from_pdf(pdf_path)

        if not text:
            return {
                'name': 'Unknown',
                'email': None,
                'phone': None,
                'objective': '',
                'education': '',
                'skills': '',
                'experience_years': 0,
                'experience_details': '',
                'projects': '',
                'certifications': '',
                'resume_text': '',
                'resume_filename': Path(pdf_path).name
            }

        # Extract structured data
        name = self.extract_name(text)
        email = self.extract_email(text)
        phone = self.extract_phone(text)

        objective = self.extract_section(text, 'objective')
        education = self.extract_section(text, 'education')
        skills = self.extract_section(text, 'skills')
        experience = self.extract_section(text, 'experience')
        projects = self.extract_section(text, 'projects')
        certifications = self.extract_section(text, 'certifications')

        experience_years = self.estimate_experience_years(experience)

        return {
            'name': name,
            'email': email,
            'phone': phone,
            'objective': objective[:500] if objective else '',  # Limit length
            'education': education[:1000] if education else '',
            'skills': skills[:1000] if skills else '',
            'experience_years': experience_years,
            'experience_details': experience[:2000] if experience else '',
            'projects': projects[:1000] if projects else '',
            'certifications': certifications[:500] if certifications else '',
            'resume_text': text[:5000],  # Store first 5000 chars for matching
            'resume_filename': Path(pdf_path).name
        }


def extract_resume(pdf_path: str) -> Dict:
    """
    Convenience function to extract resume data

    Args:
        pdf_path: Path to resume PDF

    Returns:
        Extracted resume data dictionary
    """
    extractor = ResumeExtractor()
    return extractor.extract_resume_data(pdf_path)
