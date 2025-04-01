import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Form
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import io, os , PyPDF2, docx
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

MODEL_NAME = "deepseek-r1:1.5b"
MODEL_BASE_URL = "http://35.192.59.10:11434"

from fastapi import FastAPI
app = FastAPI()

class JobOption(BaseModel):
    id: int
    title: str
    url: str
    code: str

class JobSearchResponse(BaseModel):
    job_options: List[JobOption]

class TechSkillsResponse(BaseModel):
    job_title: str
    job_code: str
    tech_skills: List[str]

class UserSkillsResponse(BaseModel):
    skills: str
    file_name: str


def extract_text_from_pdf(file_content):
    """Extract text from PDF file content"""
    pdf_file = io.BytesIO(file_content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(file_content):
    """Extract text from DOCX file content"""
    docx_file = io.BytesIO(file_content)
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def get_user_skills(resume_text: str):
    """
    Extract skills from a resume using the Gemma LLM
    """
    model = ChatOllama(model=MODEL_NAME, base_url=MODEL_BASE_URL)
    prompt = PromptTemplate.from_template("""
    [Instructions]
    based on this resume what skills does this user have?
    Resume text:
    {resume}
    Answer:[/Instructions]
    """)
    
    chain = RunnableSequence(
        prompt,
        model
    )
    
    response = chain.invoke({"resume": resume_text})
    return response.content if hasattr(response, 'content') else str(response)


@app.get('/')
def home():
        return {"hello world"}

@app.get("/search/{job_title}", response_model=JobSearchResponse, tags=["Job Search"])
async def search_jobs(job_title: str, limit: Optional[int] = Query(10, description="Maximum number of results to return")):
    """
    Search for job titles on O*NET Online.
    """
    search_url = f"https://www.onetonline.org/find/quick?s={job_title.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Avoid bot detection
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error accessing O*NET search page: {str(e)}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    job_options = []
    
    for job_td in soup.find_all("td", {"data-title": "Occupation"}):
        job_link = job_td.find("a", href=True, string=True)
        if not job_link:
            continue
            
        job_title_text = job_td.get("data-text", "").strip()
        job_url = job_link["href"]
        job_code = job_url.split("/")[-1]  # Extract job code
        
        job_options.append({
            "id": len(job_options) + 1,
            "title": job_title_text,
            "url": job_url,
            "code": job_code
        })
        
        if len(job_options) >= limit:
            break
    
    return {"job_options": job_options}

@app.get("/tech-skills/{job_code}", response_model=TechSkillsResponse, tags=["Tech Skills"])
async def get_tech_skills(job_code: str):
    """
    Get technology skills for a specific job code.
    """
    # First, get the job title
    job_url = f"https://www.onetonline.org/link/summary/{job_code}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(job_url, headers=headers)
        response.raise_for_status()
        job_soup = BeautifulSoup(response.text, "html.parser")
        job_title = job_soup.find("h1").text.strip() if job_soup.find("h1") else "Unknown Job"
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error accessing job details: {str(e)}")
    
    # Now get the tech skills
    demand_url = f"https://www.onetonline.org/link/demand/{job_code}"
    
    try:
        response = requests.get(demand_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error accessing technology skills: {str(e)}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    tech_skills = [td["data-text"] for td in soup.find_all("td", class_="w-85 mw-10e sorter-text")]    
   
    return {"tech_skills": tech_skills}

@app.post("/resume-skills", response_model=UserSkillsResponse, tags=["Resume Analysis"])
async def extract_skills_from_resume(resume_file: UploadFile = File(...)):
    """
    Extract skills from a resume using the Gemma LLM.
    Accepts PDF or DOCX files.
    """
    file_extension = os.path.splitext(resume_file.filename)[1].lower()
    
    if file_extension not in ['.pdf', '.docx']:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    # Read file content
    file_content = await resume_file.read()
    
    try: # Extract text based on file type
        if file_extension == '.pdf':
            resume_text = extract_text_from_pdf(file_content)
        else:  # .docx
            resume_text = extract_text_from_docx(file_content)
        
        # Use LLM to extract skills
        skills = get_user_skills(resume_text)
        
        return {
            "skills": skills,
            "file_name": resume_file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
    
# FIX EXTRACT SKILLS RESUME API ENDPOINT