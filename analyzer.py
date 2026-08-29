import re
import json
import os
import streamlit as st
from groq import Groq

# A comprehensive list of ~50 common tech skills
COMMON_TECH_SKILLS = [
    "python", "sql", "docker", "aws", "azure", "fastapi", "react", "pytorch",
    "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby", "php",
    "html", "css", "node.js", "django", "flask", "spring boot", "angular", "vue",
    "kubernetes", "terraform", "jenkins", "git", "github", "gitlab",
    "linux", "bash", "powershell",
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra",
    "gcp", "spark", "hadoop", "kafka", "snowflake", "databricks",
    "machine learning", "deep learning", "nlp", "computer vision",
    "scikit-learn", "tensorflow", "pandas", "numpy"
]

def extract_skills(job_description: str) -> list:
    """
    Finds which common tech skills appear in a pasted job description.
    Uses regex word boundaries to prevent partial word matches (e.g. 'go' in 'good').
    """
    found_skills = set()
    # Convert job description to lowercase for case-insensitive matching
    jd_lower = job_description.lower()
    
    for skill in COMMON_TECH_SKILLS:
        # Escape the skill name to handle special characters like '+' in C++
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, jd_lower):
            found_skills.add(skill)
            
    return sorted(list(found_skills))

def analyze_match(jd_skills: list, user_skills: list) -> dict:
    """
    Compares the job description skills to the user's skillset.
    Returns the match score percentage, skills the user has, and missing skills.
    """
    jd_set = set(s.lower() for s in jd_skills)
    user_set = set(s.lower() for s in user_skills)
    
    if not jd_set:
        return {
            "match_score": 0.0,
            "have_skills": [],
            "missing_skills": []
        }
        
    have_skills = jd_set.intersection(user_set)
    missing_skills = jd_set.difference(user_set)
    
    score = (len(have_skills) / len(jd_set)) * 100
    
    return {
        "match_score": round(score, 1),
        "have_skills": sorted(list(have_skills)),
        "missing_skills": sorted(list(missing_skills))
    }

def fallback_to_keyword(job_description: str, user_skills: list, reason: str) -> dict:
    """Helper to run the keyword analyzer when AI fails."""
    jd_skills = extract_skills(job_description)
    result = analyze_match(jd_skills, user_skills)
    result["required_skills"] = jd_skills
    result["summary"] = f"Fell back to Keyword Analyzer. Reason: {reason}"
    result["mode_used"] = "Keyword"
    return result

def analyze_match_ai(job_description: str, user_skills: list) -> dict:
    """
    Uses the Groq API to analyze the job description against user skills.
    Returns JSON structured data. Falls back to keyword matching if it fails.
    """
    api_key = None
    try:
        # Streamlit st.secrets might throw an error if the secrets file doesn't exist at all
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
        
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY")
        
    if not api_key:
        return fallback_to_keyword(job_description, user_skills, "No GROQ_API_KEY found in st.secrets or env variables.")
        
    try:
        client = Groq(api_key=api_key)
        
        prompt = f"""
You are an expert technical recruiter. Analyze this job description against the user's skillset.

Job Description:
{job_description}

User Skills:
{", ".join(user_skills)}

Reply ONLY with a valid JSON object (no markdown formatting, no code fences) with the exact keys:
{{
    "required_skills": ["skill1", "skill2"],
    "have_skills": ["skill1"],
    "missing_skills": ["skill2"],
    "match_score": 50,
    "summary": "This is a two-sentence summary of the match."
}}
"""
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
            temperature=0.1,
        )
        
        response_text = chat_completion.choices[0].message.content.strip()
        
        # Strip markdown code fences if AI included them
        if response_text.startswith("```"):
            response_text = re.sub(r"^```(?:json)?", "", response_text, flags=re.IGNORECASE).strip()
            response_text = re.sub(r"```$", "", response_text).strip()
            
        result = json.loads(response_text)
        result["mode_used"] = "AI"
        return result
        
    except Exception as e:
        return fallback_to_keyword(job_description, user_skills, f"AI Error: {str(e)}")
