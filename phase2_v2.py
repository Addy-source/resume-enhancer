from rich.console import Console
import fitz  # PyMuPDF
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

MODEL_NAME = "gemma3:1b"
MODEL_BASE_URL = "http://35.192.59.10:11434"


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def get_user_skills_from_pdf(pdf_path: str):
    """
    Extract skills from a resume PDF using the Gemma LLM
    """
    resume_text = extract_text_from_pdf(pdf_path)

    model = ChatOllama(model=MODEL_NAME, base_url=MODEL_BASE_URL)
    prompt = PromptTemplate.from_template("""
    [Instructions] 
    Based on this resume, what skills does this user have? 
    Resume text:
    {resume}
    Answer:
    [/Instructions]
    """)
    
    chain = RunnableSequence(
        prompt,
        model
    )
    response = chain.invoke({"resume": resume_text})
    return response.content

# Example usage
pdf_resume_path = "resume2.pdf"
skills = get_user_skills_from_pdf(pdf_resume_path)

#  # Output to the console
# console = Console()
# console.print(skills)