from flask import Flask, config,render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash  
from config import Config
from services.skills import find_skills, get_missing_skills, calculate_total_score
from services.pdf_reader import extract_text
from services.roles import recommend_job_role
from services.ats import calculate_ats_score
from services.courses import get_recommended_courses
from services.similarity import calculate_nlp_score
from database.db import save_analysis
from database.db import get_analysis_history
from database.db import create_user
from database.db import get_user_by_email 

app =  Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

@app.route("/", methods=["GET","POST"])
def home():
    
    if "user_id" not in session:
        return redirect("/login")

    found_skills = []
    total_score = 0
    missing_skills = []

    job_role = ""
    recommended_course = []

    ats_score = 0
    final_score = 0
    
    job_skills = []
    matched_skills = []
    missing_job_skills = []
    job_match_score = 0

    nlp_score = 0
    final_match_score = 0

    if request.method == "POST":
       resume = request.files["resume"]

       if resume.filename == "":
        return "Please select a PDF file."
       
       if not resume.filename.lower().endswith(".pdf"):
        return "Please upload a PDF file."

       file_path = "uploads/" + resume.filename

       resume.save(file_path)


       text = extract_text(file_path)
       found_skills = find_skills(text)
       job_role = recommend_job_role(found_skills)
       missing_skills = get_missing_skills(found_skills)
       recommended_course = get_recommended_courses(missing_skills)
       ats_score = calculate_ats_score(text)
       total_score = calculate_total_score(found_skills)

       skill_weight = 0.7
       ats_weight = 0.3
       final_score = (total_score * skill_weight) + (ats_score * ats_weight)
       final_score = round(final_score, 2)

       job_description = request.form.get("job_description", "")
      
    
       job_skills = find_skills(job_description)

       matched_skills = []
       for skill in job_skills:
          if skill in found_skills:
             matched_skills.append(skill)
        
       missing_job_skills = [] 
       for skill in job_skills:
          if skill not in found_skills:
             missing_job_skills.append(skill)
        
       
       if len(job_skills) > 0:
        job_match_score = (len(matched_skills) / len(job_skills)) * 100
       else:
        job_match_score = 0

       job_match_score = round(job_match_score, 2)

       if job_description.strip():

        nlp_score = calculate_nlp_score(
        text,
        job_description
         )
       else:
        nlp_score = 0
        job_match_score = 0
        matched_skills = []
        missing_job_skills = []

        
       nlp_weight = 0.3
       final_match_score = (
        job_match_score * skill_weight
        +
        nlp_score * nlp_weight
        )

       final_match_score = round(
        final_match_score,
        2
         )

       save_analysis(
       session.get("user_id"),
       resume.filename,
       final_score,
       ats_score,
       job_match_score,
       nlp_score,
       final_match_score,
       job_role,
       )

    return render_template(
        "index.html",
        skills=found_skills,
        total_score=total_score,
        missing=missing_skills,
        courses=recommended_course,
        job_role=job_role,
        ats_score=ats_score,
        final_score=final_score,
        job_skills=job_skills,
        matched_skills=matched_skills,
        missing_job_skills=missing_job_skills,
        job_match_score=job_match_score,
        nlp_score=nlp_score,
        final_match_score=final_match_score,
    )


@app.route("/signup", methods=["GET","POST"])
def signup():        
      if request.method == "POST":
         username = request.form.get("username")
         email = request.form.get("email")
         password = request.form.get("password")

         hash_password = generate_password_hash(password)

         create_user(username, email, hash_password)

         return redirect("/login")

      return render_template("signup.html")

@app.route("/login", methods=["GET","POST"])
def login():
      if request.method == "POST":
         email= request.form["email"]
         password= request.form["password"]

         user = get_user_by_email(email)

         if not user:
            return "USER NOT FOUND"
         if check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect("/")
         else: 
            return "INVALID PASSWORD"
      return render_template("login.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@app.route("/history")
def history():
  
  if "user_id" not in session:
    return redirect("/login")
  
  history_data= get_analysis_history(
     session["user_id"]
  )
  
  return render_template(
    "history.html",
    history=history_data
  )


if __name__ == "__main__": 
    app.run(debug=True) 
