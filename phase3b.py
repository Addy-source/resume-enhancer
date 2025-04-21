import phase1
import pdfkit
import phase2_v2
import phase3a
import markdown
import phase3 
import json
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate


# Example usage
job_title = input("Enter a job title: ")
required_skills = phase1.get_job_tech_skills(job_title)

# Extract skills from resume
resume_path = "resume2.pdf"
resume_text = phase2_v2.extract_text_from_pdf(resume_path) 
user_skills = phase2_v2.get_user_skills_from_pdf(resume_path)

# Find missing skills
missing = phase3.find_missing_skills(user_skills, required_skills)

# Personality traits
personality = json.dumps(phase3a.self_discovery_data, indent=2)

# Ensure Ollama model is correct
model = ChatOllama(model="llama3", base_url="http://localhost:11434")  # Check model availability

# Create and format the prompt
prompt = PromptTemplate.from_template(
 """
    <s> [Instructions] You are a project recommendation chatbot.
    Given a user's resume, current skills, missing skills for their desired job,
    their personality traits, and their future job title,
    generate a list of personalized project recommendations. These projects should:
    - Help the user gain missing skills needed for their future job.
    - Align with their personality traits and interests.
    - Enhance their resume by showcasing relevant experience.
    - Include a mix of small, medium, and large projects with clear objectives.
    - Provide real-world applications to make them stand out to employers
    - Projects they will genuinely care about and that matters to them .
    - When students build projects they genuinely care about, the passion shows—in the quality,
    - the effort, and even in how they talk about it later.
    - Output a structured list of projects with descriptions, the skills libraries or frameworks that will be used,
    estimated time to complete, and an example of how it will be inputted in the user's resume make sure they are numerics.
    - The skills that they will gain based on this project

    For each project recommendation, provide:
    - Project title and concise description (2-3 sentences)
    - Primary skills developed (prioritize those from their "missing skills" list)
    - Technologies/frameworks/libraries to utilize
    - Estimated completion time (in hours or weeks)
    - Impact statement for resume (25 words or less)
    - Difficulty level (1-5)
    - Why this project aligns with their personality and career goals
    - How this project will help them gain the missing skills
    - Why this project matters to them
    - Why this project will help them stand out to employers
    Consider the industry standards and emerging trends in their target field when making recommendations.
    
    [/Instructions]
    Future Job Title: {job_title}
    Required Skills: {required_skills}
    Resume: {resume_text}
    User Skills: {user_skills}
    Missing Skills: {missing}
    User Personality Discovery Engine: {personality}
 """
)

# Format the prompt
formatted_prompt = prompt.format(
    job_title=job_title,
    required_skills=", ".join(required_skills),  
    resume_text=resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,  
    user_skills=", ".join(user_skills),
    missing=", ".join(missing),
    personality=personality
)

# Generate response
response = model.invoke(formatted_prompt)
response_text = response.content

# Saving the response as a plain text file
with open("response.txt", "w") as file:
    file.write(response_text)

# Convert the response to Markdown and save it
response_text_markdown = markdown.markdown(response_text)
# Convert Markdown to HTML
html = markdown.markdown(response_text)
config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

pdfkit.from_string(response_text_markdown, 'response_pdf.pdf', configuration=config)


# # Output to the console
# console = Console()
# console.print(response_text)


# How to do markdown rendering in itself in the response
# email math teacher to ask if __ summary are mandatory 