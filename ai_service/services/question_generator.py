QUESTION_BANK = {
    "python": [
        "What is the difference between list and tuple?",
        "Explain decorators in Python."
    ],
    "sql": [
        "What is an INNER JOIN?",
        "Difference between DELETE and TRUNCATE?"
    ],
    "docker": [
        "What is a Docker image?",
        "Difference between Docker and Virtual Machine?"
    ],
    "fastapi": [
        "What is FastAPI?",
        "Why is FastAPI faster than Flask?"
    ]
}

def generate_questions(skills):
    questions = {}

    for skill in skills:
        skill_lower = skill.lower()

        if skill_lower in QUESTION_BANK:
            questions[skill] = QUESTION_BANK[skill_lower]

    return questions