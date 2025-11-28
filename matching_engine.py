"""
Matching Engine for AI Resume Shortlister
Hybrid scoring: Cosine Similarity + XGBoost with Experience Extraction
"""

import numpy as np
import joblib
import re
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from typing import Dict


class SmartDomainDetector:
    def __init__(self):
        # Core keywords + semantic expansions for comprehensive domain coverage
        self.domain_patterns = {
            'technology': {
                'keywords': ['python', 'java', 'javascript', 'software', 'developer', 'engineer', 'cloud', 'aws', 'database', 'programming', 'coding', 'algorithm', 'frontend', 'backend', 'fullstack', 'devops', 'api', 'microservices', 'kubernetes', 'docker'],
                'context': ['development', 'programming', 'coding', 'systems', 'applications', 'technology', 'technical', 'computing', 'digital', 'automation']
            },
            'culinary': {
                'keywords': ['chef', 'cook', 'culinary', 'kitchen', 'food', 'menu', 'recipe', 'cuisine', 'restaurant', 'cooking', 'baking', 'pastry', 'catering'],
                'context': ['culinary', 'food service', 'hospitality', 'dining', 'gastronomy', 'food preparation']
            },
            'healthcare': {
                'keywords': ['patient', 'medical', 'clinical', 'healthcare', 'nurse', 'doctor', 'hospital', 'physician', 'surgery', 'pharmacy', 'diagnosis', 'treatment', 'therapy', 'medication', 'health', 'wellness', 'clinical', 'hospital', 'medical center'],
                'context': ['care', 'treatment', 'medicine', 'health', 'wellness', 'clinical', 'medical', 'patient care', 'health services']
            },
            'finance': {
                'keywords': ['accounting', 'finance', 'financial', 'audit', 'bookkeeping', 'tax', 'cpa', 'budget', 'investment', 'banking', 'portfolio', 'risk management', 'financial analysis', 'wealth management', 'accountant', 'auditor', 'financial planning', 'investment banking'],
                'context': ['financial', 'banking', 'investment', 'money', 'revenue', 'profit', 'financial services', 'wealth management']
            },
            'marketing': {
                'keywords': ['marketing', 'seo', 'sem', 'social media', 'google analytics', 'facebook ads', 'content marketing', 'email marketing', 'brand', 'campaign', 'digital marketing', 'advertising', 'brand management', 'market research', 'customer acquisition', 'conversion rate', 'marketing strategy'],
                'context': ['marketing', 'advertising', 'brand', 'campaign', 'digital', 'social media', 'content', 'engagement']
            },
            'education': {
                'keywords': ['teaching', 'education', 'curriculum', 'classroom', 'student', 'learning', 'lesson planning', 'academic', 'school', 'university', 'college', 'professor', 'instructor', 'tutoring', 'educational technology', 'pedagogy', 'syllabus', 'assessment'],
                'context': ['education', 'teaching', 'learning', 'academic', 'educational', 'student development', 'curriculum']
            },
            'engineering': {
                'keywords': ['mechanical', 'electrical', 'civil', 'engineering', 'design', 'cad', 'prototype', 'manufacturing', 'structural', 'aerospace', 'chemical', 'industrial', 'systems engineering', 'project management', 'technical drawings', 'fea', 'cfd', 'product development'],
                'context': ['engineering', 'design', 'manufacturing', 'technical', 'construction', 'development', 'project management']
            },
            'sales': {
                'keywords': ['sales', 'business development', 'account executive', 'client acquisition', 'negotiation', 'revenue', 'closing', 'prospecting', 'customer relationship', 'account management', 'sales pipeline', 'quotas', 'territory management', 'solution selling', 'sales strategy'],
                'context': ['sales', 'business development', 'client', 'customer', 'revenue', 'negotiation', 'account management']
            },
            'operations': {
                'keywords': ['operations', 'logistics', 'supply chain', 'process improvement', 'efficiency', 'manufacturing', 'production', 'quality control', 'inventory', 'procurement', 'warehouse', 'distribution', 'operational excellence', 'lean manufacturing', 'six sigma', 'process optimization'],
                'context': ['operations', 'logistics', 'supply chain', 'process', 'efficiency', 'manufacturing', 'production']
            },
            'design': {
                'keywords': ['design', 'ux', 'ui', 'user experience', 'graphic design', 'visual design', 'creative', 'adobe', 'photoshop', 'illustrator', 'figma', 'sketch', 'prototyping', 'wireframing', 'brand identity', 'typography', 'layout', 'interaction design'],
                'context': ['design', 'creative', 'visual', 'user experience', 'graphic', 'interface', 'layout']
            },
            'research': {
                'keywords': ['research', 'analysis', 'data collection', 'laboratory', 'experiment', 'scientific', 'methodology', 'hypothesis', 'publication', 'academic research', 'qualitative', 'quantitative', 'data analysis', 'literature review', 'research design', 'statistical analysis'],
                'context': ['research', 'analysis', 'scientific', 'experimental', 'data collection', 'methodology']
            }
        }

    def detect_domain(self, text):
        if len(text) < 20:
            return 'general'

        text_lower = text.lower()
        domain_scores = {}

        for domain, patterns in self.domain_patterns.items():
            keyword_score = sum(2 for keyword in patterns['keywords'] if keyword in text_lower)
            context_score = sum(1 for context in patterns['context'] if context in text_lower)

            total_score = keyword_score + context_score
            if total_score > 0:
                domain_scores[domain] = total_score

        if domain_scores:
            best_domain = max(domain_scores, key=domain_scores.get)
            return best_domain if domain_scores[best_domain] >= 3 else 'general'

        return 'general'


class MatchingEngine:
    """Resume-Job matching engine with experience extraction and ranking"""

    def __init__(self, model_path='xgboost_semantic.pkl', scaler_path='scaler_semantic.pkl',
                 cosine_weight=0.6, xgb_weight=0.4, experience_data_path='experience_data.json'):
        """Initialize matching engine"""
        try:
            # Load models
            self.xgb_model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

            # Set scoring weights
            self.cosine_weight = cosine_weight
            self.xgb_weight = xgb_weight
            assert abs(cosine_weight + xgb_weight - 1.0) < 0.01, "Weights must sum to 1.0"

            # Initialize SmartDomainDetector
            self.domain_detector = SmartDomainDetector()

            # Experience storage
            self.experience_data_path = experience_data_path
            self.experience_data = self._load_experience_data()

            print(f"✅ Matching engine loaded successfully")
            print(f"   Hybrid scoring: {self.cosine_weight*100:.0f}% Cosine + {self.xgb_weight*100:.0f}% XGBoost")
            print(f"   Domain detection: SmartDomainDetector with {len(self.domain_detector.domain_patterns)} domains")
        except Exception as e:
            raise Exception(f"Failed to load matching models: {e}")

    def _load_experience_data(self) -> Dict:
        """Load existing experience data from JSON file"""
        try:
            with open(self.experience_data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_experience_data(self):
        """Save experience data to JSON file"""
        with open(self.experience_data_path, 'w') as f:
            json.dump(self.experience_data, f, indent=2)

    def _extract_experience(self, resume_text: str) -> int:
        """
        Extract years of experience from resume text.
        Simple pattern matching for common formats like "5 years experience"
        """
        text_lower = resume_text.lower()
        
        # Pattern: "X years of experience" or "X+ years experience"
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of)?\s*experience',
            r'experience\s*[:\-]?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*(?:in|of|with|as)',
        ]
        
        years_found = []
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                for match in matches:
                    try:
                        years = int(match)
                        if 0 < years <= 50:  # Sanity check
                            years_found.append(years)
                    except:
                        pass
        
        if years_found:
            return max(years_found)  # Return highest years mentioned
        
        # Fallback: Try to infer from seniority level
        if 'senior' in text_lower and 'junior' not in text_lower:
            return 5
        elif 'mid-level' in text_lower or 'mid level' in text_lower or 'intermediate' in text_lower:
            return 3
        elif 'entry level' in text_lower or 'junior' in text_lower or 'graduate' in text_lower:
            return 1
        elif 'lead' in text_lower or 'principal' in text_lower or 'staff' in text_lower:
            return 8
        elif 'director' in text_lower or 'vp' in text_lower or 'vice president' in text_lower:
            return 10
        
        return 0

    def _detect_domain(self, text: str) -> str:
        """Detect the primary domain using SmartDomainDetector"""
        return self.domain_detector.detect_domain(text)

    def predict_match(self, resume_text: str, job_text: str, resume_id: str = None) -> Dict:
        """Predict match score and extract experience for shortlisted resumes"""
        # Generate embeddings
        resume_emb = self.semantic_model.encode([resume_text])[0]
        job_emb = self.semantic_model.encode([job_text])[0]

        # Calculate similarity metrics
        cos_sim = cosine_similarity([resume_emb], [job_emb])[0][0]
        euc_dist = euclidean_distances([resume_emb], [job_emb])[0][0]
        man_dist = np.sum(np.abs(resume_emb - job_emb))

        # Create feature vector
        X = np.concatenate([resume_emb, job_emb, [cos_sim, euc_dist, man_dist]])
        X_scaled = self.scaler.transform([X])

        # Get scores
        xgb_score = self.xgb_model.predict(X_scaled)[0] * 100
        cosine_score = cos_sim * 100

        # Hybrid score
        base_score = (self.cosine_weight * cosine_score) + (self.xgb_weight * xgb_score)

        # Domain penalty
        resume_domain = self._detect_domain(resume_text)
        job_domain = self._detect_domain(job_text)

        if resume_domain != 'general' and job_domain != 'general' and resume_domain != job_domain:
            adjusted_score = base_score * 0.75
        else:
            adjusted_score = base_score

        final_score = round(float(adjusted_score), 2)
        is_shortlisted = final_score >= 65

        result = {
            'match_score': final_score,
            'category': self.get_match_category(final_score),
            'domain': resume_domain
        }

        # Extract experience ONLY for shortlisted
        if is_shortlisted and resume_id:
            experience_years = self._extract_experience(resume_text)
            result['experience_years'] = experience_years

            # Store in experience data
            self.experience_data[resume_id] = {
                'experience_years': experience_years,
                'match_score': final_score,
                'domain': resume_domain,
                'timestamp': str(np.datetime64('now'))
            }
            self._save_experience_data()

        return result

    def get_experience_stats(self) -> Dict:
        """Get statistics about stored experience data"""
        if not self.experience_data:
            return {}

        experiences = [data['experience_years'] for data in self.experience_data.values()]
        match_scores = [data['match_score'] for data in self.experience_data.values()]

        return {
            'total_shortlisted': len(self.experience_data),
            'avg_experience': round(np.mean(experiences), 2),
            'max_experience': max(experiences),
            'min_experience': min(experiences),
            'avg_match_score': round(np.mean(match_scores), 2)
        }

    def get_match_category(self, score: float) -> str:
        """Categorize match score"""
        if score >= 65:
            return "Shortlisted"
        else:
            return "Not Shortlisted"