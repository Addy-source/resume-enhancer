import phase1
import phase2_v1
import phase3  # Import Phase 3 separately
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

# Example usage
job_title = input("Enter a job title: ")
required_skills = phase1.get_job_tech_skills(job_title)

# Extract skills from resume
resume_path = "resume2.pdf"
resume_text = phase2_v1.extract_text_from_pdf(resume_path)  # Ensure this extracts text
user_skills = phase2_v1.analyze_resume_file(resume_path)

# Find missing skills
missing = phase3.find_missing_skills(user_skills, required_skills)

# Ensure Ollama model is correct
model = ChatOllama(model="llama3", base_url="http://localhost:11434")  # Check model availability

# Create and format the prompt
prompt = PromptTemplate.from_template(
    """
    <s> [Instructions] You are a project recommendation chatbot. 
    Given a user's resume (derive their personality traits from their resume),
    current skills, missing skills for their desired job, and their future job title, 
    generate a list of personalized project recommendations. These projects should:

    - Help the user gain missing skills needed for their future job.
    - Align with their personality traits and interests.
    - Enhance their resume by showcasing relevant experience.
    - Include a mix of small, medium, and large projects with clear objectives.
    - Provide real-world applications to make them stand out to employers.
    - Output a structured list of projects with descriptions, required skills, 
      estimated time to complete, and potential impact on the user’s career trajectory.
    [/Instructions]
    
    Future Job Title: {job_title}
    Required Skills: {required_skills}
    Resume: {resume_text}
    User Skills: {user_skills}
    Missing Skills: {missing}
    """
)

# Format the prompt
formatted_prompt = prompt.format(
    job_title=job_title,
    required_skills=", ".join(required_skills),  # Ensure list is converted to string
    resume_text=resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,  # Trim text if too long
    user_skills=", ".join(user_skills),
    missing=", ".join(missing)
)

# Generate response
response = model.invoke(formatted_prompt)
print(response)
