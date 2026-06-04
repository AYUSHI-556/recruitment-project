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