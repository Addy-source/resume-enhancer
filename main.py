import phase1
import phase2
import phase3  # Import Phase 3 separately

# Example usage
job_title = input("Enter a job title: ")
required_skills = phase1.get_job_tech_skills(job_title)
print("Required skills for the job:", required_skills)

# Extract skills from resume
resume_path = "resume.pdf"
user_skills = phase2.analyze_resume_file(resume_path)
print("Extracted skills from resume:", user_skills)

# Find missing skills
missing = phase3.find_missing_skills(user_skills, required_skills)
print("Missing Skills:", missing)
