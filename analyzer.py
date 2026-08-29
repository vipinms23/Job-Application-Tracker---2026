import re

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
