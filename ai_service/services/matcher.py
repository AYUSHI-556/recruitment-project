def calculate_match_score(resume_data, jd_data):
    resume_skills = set(resume_data.get("skills", []))
    jd_skills = set(jd_data.get("skills", []))

    matched = resume_skills.intersection(jd_skills)

    score = 0
    if len(jd_skills) > 0:
        score = round((len(matched) / len(jd_skills)) * 100, 2)

    return {
        "score": score,
        "matched_skills": list(matched),
        "missing_skills": list(jd_skills - resume_skills),
        "decision": "SHORTLIST" if score >= 60 else "REJECT"
    }