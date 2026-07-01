def calculate_ats_score(text):

  ats_score = 0
  
  if "bachelor"  in text.lower() or "b.tech" in text.lower() or "bachelor's" in text.lower():
           ats_score +=30
  if "built" in text.lower() or "created" in text.lower() or "developed" in text.lower():
       ats_score += 30
  if "certified" in text.lower() or "certification" in text.lower():
           ats_score += 20
  if "internship" in text.lower():
           ats_score += 20

  return min(ats_score,100)

