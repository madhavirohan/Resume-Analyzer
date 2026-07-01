skill_db = [
    "Python",
    "MySql",
    "Flask",
    "FastApi",
    "Git",
    "Docker",
    "REST API",
    "HTML",
    "CSS",
    "Artificial Intelligence",
    "Machine Learning"
]

def find_skills(text): 
    found_skills = []

    for skill in skill_db:
        if skill.lower() in text.lower():
           found_skills.append(skill)

    return found_skills

def get_missing_skills(found_skills):
     missing_skills = []
     for skills in skill_db:
           if skills not in found_skills:
              missing_skills.append(skills)
     return missing_skills

def calculate_total_score(found_skills):
        total_skills = len(skill_db)

        detected_skills = len(found_skills)

        total_score = (detected_skills / total_skills * 100)
        return round(total_score, 2)


