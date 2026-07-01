COURSE = {
            "MySql": "Beginner Friendly MySQL",
            "Flask": "Flask For Beginners",
            "FastApi": "FastAPI Crash Course",
            "Artificial Intelligence": "Introduction to AI",
            "Machine Learning": "Introduction to ML",
            "Python": "Python Fundamentals",
            "Git" : "Git:The Complete Course",
            "Docker": "Learn Docker With Me",
            "HTML": "HTML:HyperText Markup Language",
            "CSS" : "CSS:Style Your WebPage",
            "Pandas" : "Learn Pandas in 10 minutes"
         }

def get_recommended_courses(missing_skills):
  recommended_course = []

  for skill in missing_skills:
    if skill in COURSE:
     recommended_course.append(COURSE[skill])

  return recommended_course
