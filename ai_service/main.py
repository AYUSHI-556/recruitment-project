from fastapi import FastAPI
from services.text_extraction import extract_text_from_pdf
from services.resume_parser import parse_resume_text
from services.jd_parser import parse_jd_text
from services.matcher import calculate_match_score
from database import create_table, save_candidate, get_all_candidates, get_ranked_candidates
from services.question_generator import generate_questions
from database import create_table, save_candidate, get_all_candidates, get_ranked_candidates, get_dashboard_stats
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import users_db, verify_password, create_token, get_current_user, require_admin
from fastapi import Depends
from auth import get_current_user
from pydantic import BaseModel

app = FastAPI()
create_table()

@app.get("/ai/health")
def health():
    return {"status": "AI service running"}

@app.get("/resume/test")
def resume_test():
    text = extract_text_from_pdf("uploads/resume.pdf")
    return {"text": text}

@app.get("/resume/parse")
def resume_parse():
    text = extract_text_from_pdf("uploads/resume.pdf")
    parsed_data = parse_resume_text(text)

    return parsed_data

@app.get("/jd/parse")
def jd_parse():

    jd_text = """
    Need Backend Developer

    Skills:
    Python
    FastAPI
    Docker
    Kubernetes
    """

    return parse_jd_text(jd_text)

@app.post("/screen")
async def screen_candidate():
    resume_text = extract_text_from_pdf("uploads/resume.pdf")

    jd_text = """
    Need Backend Developer

    Skills:
    Python
    FastAPI
    Docker
    Kubernetes
    """

    resume_data = parse_resume_text(resume_text)
    jd_data = parse_jd_text(jd_text)

    result = calculate_match_score(resume_data, jd_data)

    save_candidate(
        resume_data.get("name", "Unknown"),
        resume_data.get("email", "Unknown"),
        str(resume_data.get("skills", [])),
        result["score"],
        str(result["matched_skills"]),
        str(result["missing_skills"]),
        result["decision"]
    )

    return result



@app.get("/candidates")
def candidates(user=Depends(get_current_user)):
    return get_all_candidates()

@app.get("/leaderboard")
def leaderboard(user=Depends(get_current_user)):
    return get_ranked_candidates()

@app.get("/interview-questions")
def interview_questions():

    resume_text = extract_text_from_pdf("uploads/resume.pdf")

    resume_data = parse_resume_text(resume_text)

    skills = resume_data.get("skills", [])

    return generate_questions(skills)

@app.get("/dashboard")
def dashboard(user=Depends(get_current_user)):
    return get_dashboard_stats()

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"]
    }

@app.get("/admin-only")
def admin_only(user=Depends(require_admin)):
    return {"message": "Welcome Admin"}

@app.get("/dashboard/metrics")
def dashboard_metrics():
    return {
        "total_candidates": 25,
        "shortlisted": 10,
        "interviewed": 8,
        "selected": 3
    }


@app.get("/dashboard/candidates")
def dashboard_candidates():
    return [
        {"name": "Rahul", "score": 92},
        {"name": "Priya", "score": 88}
    ]
@app.get("/dashboard/score-distribution")
def score_distribution():
    return {
        "0-40": 2,
        "41-55": 4,
        "56-70": 8,
        "71-80": 5,
        "81-90": 4,
        "91-100": 2
    }
@app.get("/dashboard/top-candidates")
def top_candidates():
    candidates = [
        {"name": "Rahul", "score": 92, "status": "Hire"},
        {"name": "Priya", "score": 88, "status": "Hire"},
        {"name": "Sneha", "score": 76, "status": "Review"},
        {"name": "Amit", "score": 58, "status": "Reject"}
    ]

    return sorted(candidates, key=lambda x: x["score"], reverse=True)
@app.get("/dashboard/recommendation/{score}")
def get_recommendation(score: int):
    if score >= 80:
        recommendation = "Hire"
    elif score >= 60:
        recommendation = "Review"
    else:
        recommendation = "Reject"

    return {
        "score": score,
        "recommendation": recommendation
    }
@app.get("/dashboard/compare")
def compare_candidates():
    candidate1 = {
        "name": "Rahul",
        "skills": 90,
        "experience": 85,
        "education": 80
    }

    candidate2 = {
        "name": "Priya",
        "skills": 85,
        "experience": 88,
        "education": 90
    }

    return {
        "candidate1": candidate1,
        "candidate2": candidate2
    }
@app.get("/interview/questions")
def interview_questions():
    return {
        "questions": [
            "Tell me about yourself.",
            "What are your strongest technical skills?",
            "Explain one project from your resume.",
            "Why should we hire you?",
            "Where do you see yourself in 2 years?"
        ]
    }


class InterviewAnswer(BaseModel):
    candidate_name: str
    question: str
    answer: str


@app.post("/interview/submit-answer")
def submit_answer(data: InterviewAnswer):
    answer_length = len(data.answer.split())

    if answer_length >= 30:
        score = 90
        feedback = "Good detailed answer"
    elif answer_length >= 15:
        score = 70
        feedback = "Average answer, needs more detail"
    else:
        score = 45
        feedback = "Answer is too short"

    return {
        "candidate_name": data.candidate_name,
        "question": data.question,
        "answer": data.answer,
        "score": score,
        "feedback": feedback
    }
@app.get("/workflow/final-report")
def final_report():
    return {
        "candidate_name": "Rahul",
        "resume_score": 82,
        "interview_score": 70,
        "overall_score": 76,
        "recommendation": "Review",
        "summary": "Candidate has good technical background but needs stronger interview answers."
    }