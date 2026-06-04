import sqlite3

def create_table():
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        skills TEXT,
        score REAL,
        matched_skills TEXT,
        missing_skills TEXT,
        decision TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_candidate(name, email, skills, score, matched_skills, missing_skills, decision):
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates (name, email, skills, score, matched_skills, missing_skills, decision)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, skills, score, matched_skills, missing_skills, decision))

    conn.commit()
    conn.close()


def get_all_candidates():
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates")
    data = cursor.fetchall()

    conn.close()
    return data

def get_ranked_candidates():
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM candidates
    ORDER BY score DESC
    """)

    data = cursor.fetchall()

    conn.close()
    return data

def get_dashboard_stats():
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM candidates")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM candidates WHERE decision = 'SHORTLIST'")
    shortlisted = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM candidates WHERE decision = 'REJECT'")
    rejected = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM candidates")
    average_score = cursor.fetchone()[0]

    cursor.execute("SELECT name FROM candidates ORDER BY score DESC LIMIT 1")
    top = cursor.fetchone()

    conn.close()

    return {
        "total_candidates": total,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "average_score": round(average_score, 2) if average_score else 0,
        "top_candidate": top[0] if top else "None"
    }