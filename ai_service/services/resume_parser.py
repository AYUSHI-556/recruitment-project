import re

SKILLS_DB = [
    "Python", "Java", "C", "C++", "SQL", "HTML", "CSS",
    "JavaScript", "Bootstrap", "Django", "FastAPI",
    "Docker", "Kubernetes", "Git", "Linux",
    "Azure", "Prometheus", "Grafana"
]

def parse_resume_text(text):
    email = None
    phone = None
    skills = []

    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        email = email_match.group()

    phone_match = re.search(r'(\+91[-\s]?)?[6-9]\d{9}', text)
    if phone_match:
        phone = phone_match.group()

    lines = text.split("\n")
    name = lines[0] if lines else None

    for skill in SKILLS_DB:
        if skill.lower() in text.lower():
            skills.append(skill)

    education = None
    for line in lines:
        if "B.Tech" in line or "Bachelor" in line or "Computer Science" in line:
            education = line
            break

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education
    }