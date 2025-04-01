from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

MODEL_NAME = "gemma3:1b"
MODEL_BASE_URL = "http://35.192.59.10:11434"


def get_user_skills(resume: str):
    """
    Extract skills from a resume using the Gemma LLM
    """
    model = ChatOllama(model=MODEL_NAME, base_url=MODEL_BASE_URL)
    prompt = PromptTemplate.from_template("""
        [Instructions] 
        based on this resume what skills does this user have ? 
        Resume text:
        {resume}
        Answer:[/Instructions]
        """)
    
    chain = RunnableSequence(
        prompt,
        model
    )
    response = chain.invoke(resume)
    print(response)
    type(response)


resume = '''
Praise Ben

Upper Marlboro, MD, 20774 || 240-615-6202

praiseben13@gmail.com || https://www.linkedin.com/in/praise-ben/

EDUCATION

Bowie State University                                                                                                  		                  Bowie, MD

Bachelor of Science in Computer Science, 6x Dean’s List				               	    GPA: 4.0 | May 2026 

Courses: Data Structures & Algorithms, Calculus I, Probability & Statistics, Programming Languages.

Leadership: Vice President Bulldog Coders, Recruiter Women In Computer Science

TECHNICAL SKILLS

Programming Languages: Python, Java, SQL, JavaScript, HTML, CSS. 

Frameworks/Libraries: Tensorflow, ScikitLearn, Pandas, Numpy, Matplotlib, HuggingFace, LangChain.

Technologies: OpenAI API, Large Language Models (LLM), Natural Language Processing (NLP), Generative AI.

Certificates: AWS Machine Learning, AWS Developer, AWS Solutions Architect. AWS Cloud Practitioner.

WORK EXPERIENCE 

Apple - Incoming Data & Artificial Intelligence(AI) Intern   			         	         	   May 2025 - Aug 2025

Apple - Artificial Intelligence Machine Learning(AIML) Intern   			         	   May 2024 - Aug 2024

Engineered a Python-based LLM-Assisted App Crawler using advanced prompt engineering, increasing app interface navigation speed and reducing authentication bypass time.

Optimized app crawling algorithms, resulting in a 25% increase in unique screen discovery and 8x improvement in app coverage, enhancing data collection capabilities.

Architected a graph-based system to model app structure, facilitating the creation of a comprehensive dataset that increased data quality by 10% and expanded analysis capabilities by enabling 5 new types of insights.

Implemented Git version control for AI-driven app exploration and data analysis workflows, reducing code conflicts and improving team collaboration efficiency.

Streamlined AI experimentation processes, reducing cycle time and enhancing development efficiency and team collaboration through detailed documentation.

Runwei - Artificial Intelligence Machine Learning(AIML) Intern   			                  Jan 2025 - May 2025

Optimized AI-powered recommendation engine using Azure Machine Learning and advanced NLP, improving profile matching accuracy by 80% and reduced manual user input by 18%.

Enhanced matching algorithms, increasing accuracy by 30% and driving a 20% rise in successful funding connections through improved AI-powered recommendations.

Integrated LLM-powered support features, providing real-time, culturally sensitive assistance that improved user satisfaction scores by 35%.

Designed and implemented an AI-driven personalized learning prototype, increasing user engagement by 35% and improving skill assessment accuracy by 50%, leading to a 25% higher completion rate for training modules

CyDeploy - Machine Learning Engineer  Intern   			                  		   May 2023 - Aug 2023

Optimized AI pipeline efficiency by 40% through strategic integration of cutting-edge Machine Learning libraries (Hugging Face, OpenAI API), reducing processing time from 4 to 1.5 hours.

Automated RPA script outcome labeling using GPT-4 and OpenLLaMA, improving efficiency by 10% and increasing labeling speed by 5 times, enhancing overall process scalability.

PROJECTS

RAG CHATBOT : Developed a Retrieval-Augmented Generation (RAG) chatbot using LangChain and Llama3, achieving 95% semantic search accuracy and 3x faster response times via optimized ChromaDB vector storage.

ARGUS : Engineered a supervised learning model for crash detection, reaching 85% accuracy across car, train, and motorbike accidents using a balanced dataset (100 samples per category), securing 3rd place in a university challenge.

GOSPEL BREAKDOWN : Engineered an AI-driven web application using OpenAI's GPT-3, integrating a dual-text feature that provides personalized prayers and sermons, resulting in 50% increased user engagement and processing of 20+ daily requests for faith-based content.
'''

skills = get_user_skills(resume)
print(skills)