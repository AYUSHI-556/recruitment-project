SKILLS_DB = [
    "Python", "Java", "C++", "SQL",
    "Django", "FastAPI", "Docker",
    "Kubernetes", "Git", "Azure"
]

def parse_jd_text(text):
    skills = []

    for skill in SKILLS_DB:
        if skill.lower() in text.lower():
            skills.append(skill)

    return {
        "skills": skills
    }