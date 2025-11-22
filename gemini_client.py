"""Simple Gemini integration and resume text parser fallback.

This module provides:
- extract_resume_via_gemini(file_path=None, text=None): try to call Gemini if API key present, else fallback
- parse_resume_text(text): lightweight parsing to extract required fields

The Gemini call path is optional; if you plan to use Gemini, set GEMINI_API_KEY and GEMINI_ENDPOINT env vars.
"""
from typing import Dict, Optional
import os
import re
from pathlib import Path

try:
    import requests
except Exception:
    requests = None


def _extract_text_from_pdf_path(pdf_path: str) -> str:
    """Minimal PDF text extraction fallback using PyPDF2 if available."""
    try:
        import PyPDF2
    except Exception:
        return ""

    text_parts = []
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                try:
                    page_text = page.extract_text() or ""
                except Exception:
                    page_text = ""
                text_parts.append(page_text)
    except Exception:
        return ""

    return "\n".join(text_parts)


def extract_resume_via_gemini(file_path: Optional[str] = None, text: Optional[str] = None) -> Dict:
    """Try to extract resume fields using Gemini API if configured, otherwise fallback to local parsing.

    Returns a dictionary of fields: name, email, phone, objective, education, skills,
    experience_years, experience_details, projects, certifications, resume_text
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    endpoint = os.environ.get('GEMINI_ENDPOINT')

    # If user provided plain text, we prefer that
    if text is None and file_path:
        text = _extract_text_from_pdf_path(file_path)

    # If Gemini env is available and requests is installed, attempt remote call
    if api_key and endpoint and requests:
        try:
            headers = {'Authorization': f'Bearer {api_key}',
                       'Content-Type': 'application/json'}
            payload = {'text': text} if text else {'upload': True}
            # NOTE: This is a placeholder call. Replace with your actual Gemini REST call format.
            resp = requests.post(endpoint, json=payload,
                                 headers=headers, timeout=30)
            resp.raise_for_status()
            resp_json = resp.json()
            # Expecting resp_json to contain 'extracted_text' or full fields
            extracted_text = resp_json.get(
                'extracted_text') or resp_json.get('text') or ''
            # If API already returns parsed fields, pass them through
            fields = {k: resp_json.get(k) for k in ['name', 'email', 'phone', 'objective', 'education',
                                                    'skills', 'experience_years', 'experience_details', 'projects', 'certifications']}
            fields = {k: v for k, v in fields.items() if v}
            if not fields:
                return parse_resume_text(extracted_text)
            fields['resume_text'] = extracted_text
            return fields
        except Exception:
            # If API fails, fall back to local parsing
            pass

    # Fallback local parsing
    if not text and file_path:
        text = _extract_text_from_pdf_path(file_path)

    return parse_resume_text(text or "")


def parse_resume_text(text: str) -> Dict:
    """Lightweight résumé parser that extracts requested fields from raw text.

    This is not perfect — it's a pragmatic fallback that looks for common patterns.
    """
    out = {
        'name': None,
        'email': None,
        'phone': None,
        'objective': None,
        'education': None,
        'skills': None,
        'experience_years': 0,
        'experience_details': None,
        'projects': None,
        'certifications': None,
        'resume_text': text,
    }

    if not text:
        return out

    # Normalize whitespace
    text_norm = re.sub(r'\r', '\n', text)
    text_norm = re.sub(r'\n{2,}', '\n\n', text_norm)

    # Email
    m = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text_norm)
    if m:
        out['email'] = m.group(0)

    # Phone
    m = re.search(r"\+?\d[\d\s().-]{6,}\d", text_norm)
    if m:
        out['phone'] = m.group(0).strip()

    # Name: look at the first non-empty line that doesn't contain email/phone/link
    lines = [l.strip() for l in text_norm.split('\n') if l.strip()]
    for line in lines[:6]:
        low = line.lower()
        if 'resume' in low or 'curriculum' in low or '@' in low or 'linkedin' in low or 'github' in low or re.search(r'\d{3}[-.\s]?\d{3}', line):
            continue
        # Heuristic: 1-4 words, mostly alphabetic
        words = [w.strip('.,') for w in line.split()]
        alpha = sum(1 for w in words if w.isalpha())
        if 1 <= len(words) <= 4 and alpha >= max(1, int(len(words) * 0.6)):
            out['name'] = line[:80]
            break

    # Sections helper
    def _extract_section(section_names):
        pattern = r'(?:' + '|'.join(section_names) + r')\b'  # header
        rx = re.compile(
            rf'(?:^|\n)\s*(?:{"|".join(section_names)})\s*[:\-]?\s*\n', re.IGNORECASE)
        # Simpler: search for keywords and take following lines
        for name in section_names:
            idx = text_norm.lower().find(name.lower())
            if idx != -1:
                # grab up to next double newline or 600 chars
                tail = text_norm[idx:idx+800]
                # split by double newline or header-like pattern
                parts = re.split(r'\n\s*\n', tail)
                if len(parts) > 1:
                    return parts[1].strip()
                else:
                    return tail[len(name):].strip()
        return None

    # Objective / Summary
    out['objective'] = _extract_section(
        ['objective', 'summary', 'profile', 'about'])

    # Education
    out['education'] = _extract_section(
        ['education', 'academic', 'qualification'])

    # Skills
    skills_text = _extract_section(
        ['skills', 'technical skills', 'key skills', 'competencies'])
    if skills_text:
        # Try to compress inline skills
        out['skills'] = re.sub(r'\s+', ' ', skills_text).strip()

    # Experience years: explicit numbers first
    m = re.search(r'(\d+)\+?\s+years?\s+of\s+experience',
                  text_norm, re.IGNORECASE)
    if m:
        out['experience_years'] = int(m.group(1))
    else:
        # try year ranges
        yrs = re.findall(r'(19|20)\d{2}', text_norm)
        if yrs and len(yrs) >= 2:
            yrs_int = [int(y) for y in yrs]
            out['experience_years'] = max(0, max(yrs_int) - min(yrs_int))

    out['experience_details'] = _extract_section(
        ['experience', 'work experience', 'employment', 'professional experience'])
    out['projects'] = _extract_section(['projects', 'project', 'portfolio'])
    out['certifications'] = _extract_section(
        ['certifications', 'certificates', 'licenses'])

    return out
