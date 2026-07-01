job_roles = {
                    "Python Backend Developer": ["Python", "Flask"],
                    "Data Analyst": ["Python", "SQL", "Pandas"],
                    "ML Engineer": ["Python", "Machine Learning"]
}

def recommend_job_role(found_skills):
  
  job_role = "no suitable job role found"
  for roles,skills in job_roles.items():
           if all(skill in found_skills for skill in skills):
              job_role = roles
              break
  return job_role