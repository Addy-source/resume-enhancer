import re
import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

def extract_skills_from_resume(resume_text): # Function to extract skills from resume text
    nlp = spacy.load("en_core_web_sm") # spacy is an nlp framework in python that helps process and analyze text
    resume_text = resume_text.lower() # convert the resume text to lowercase might have to change this later 
    doc = nlp(resume_text) # pass the resume text to the nlp spacy model called doc
    potential_skills = [] # create an empty list to store potential skills
    
    skill_sections = extract_skill_sections(resume_text) # extract sections that likely contain skills from 
    if skill_sections: 
        for section in skill_sections:
            section_doc = nlp(section)
            for chunk in section_doc.noun_chunks:
                if len(chunk.text.split()) <= 4:  # Limit to 4 words max
                    potential_skills.append(chunk.text.strip())
            
            technical_terms = re.findall(r'\b[A-Za-z\+\#\.]+(\.?[A-Za-z]+)*\b', section)
            potential_skills.extend(technical_terms)
    
    skill_verbs = ["proficient in", "experienced with", "knowledge of", "skilled in", 
                   "expertise in", "familiar with", "worked with", "utilized", "using"]
    
    for verb in skill_verbs:
        matches = re.finditer(r'{}(.*?)(?:[.]|$)'.format(verb), resume_text)
        for match in matches:
            skill_phrase = match.group(1).strip()
            skill_doc = nlp(skill_phrase)
            for chunk in skill_doc.noun_chunks:
                if len(chunk.text.split()) <= 4:
                    potential_skills.append(chunk.text.strip())
    
    tech_terms = re.findall(r'\b[A-Z][a-z]*(?:\+\+|#)?\b|\b[A-Z]{2,}\b', resume_text)
    potential_skills.extend([term.lower() for term in tech_terms])
    
    skill_context = ["skills", "abilities", "competencies", "proficiencies", "technologies"]
    for context in skill_context:
        context_pattern = r'(?:{})(.*?)(?:(?:\n\n)|$)'.format(context)
        matches = re.finditer(context_pattern, resume_text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            context_text = match.group(1).strip()
            list_items = re.split(r'[,•\n]', context_text)
            for item in list_items:
                item = item.strip()
                if 2 <= len(item.split()) <= 4:  # Between 2-4 words
                    potential_skills.append(item)
    
    cleaned_skills = clean_and_filter_skills(potential_skills, resume_text)
    
    ranked_skills = rank_skills(cleaned_skills, resume_text)
    
    return ranked_skills

def extract_skill_sections(text):
    """Extract sections that likely contain skills"""
    skill_section_headers = [
        "skills", "technical skills", "core competencies", "technologies",
        "expertise", "proficiencies", "qualifications", "tech stack", "projects", "work experience"
    ]
    
    sections = []
    for header in skill_section_headers:
        pattern = r'(?:{})(.*?)(?:(?:\n\n)|$)'.format(header)
        matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            sections.append(match.group(1).strip())
    
    return sections

def clean_and_filter_skills(skills, context):
    """Clean and filter the list of potential skills"""
    unique_skills = []
    seen = set()
    for skill in skills:
        skill_lower = skill.lower().strip()
        if skill_lower and skill_lower not in seen and len(skill_lower) > 1:
            if not re.search(r'^[,.\d\W]+$', skill_lower):  # Skip if only punctuation or numbers
                unique_skills.append(skill_lower)
                seen.add(skill_lower)
    
    nlp = spacy.load("en_core_web_sm")
    filtered_skills = []
    
    not_skills = {
        "resume", "curriculum", "vitae", "cv", "references", "page", "contact", 
        "email", "phone", "address", "summary", "objective", "profile", "experience",
        "education", "university", "college", "degree", "bachelor", "master", "phd",
        "year", "years", "month", "months", "present", "current", "date", "job",
        "position", "work", "role", "responsibility", "the", "and", "of", "in", "to",
        "with", "a", "an", "or", "for", "this", "that", "these", "those", "his", "her"
    }
    
    for skill in unique_skills:
        if len(skill) <= 1 and not skill.upper() in {"R", "C"}:
            continue
            
        if skill in not_skills:
            continue
            
        if len(skill.split()) == 1:
            token = nlp(skill)[0]
            if token.is_stop and not (token.text.upper() == token.text):  # Allow acronyms
                continue
        
        filtered_skills.append(skill)
    
    return filtered_skills

def rank_skills(skills, context):
    """Rank skills by relevance using frequency and context"""
    skill_counter = Counter()
    
    for skill in skills:
        exact_count = len(re.findall(r'\b{}\b'.format(re.escape(skill)), context, re.IGNORECASE))
        skill_counter[skill] += exact_count * 2  
        
        if len(skill.split()) > 1:
            for part in skill.split():
                if len(part) > 3:  
                    partial_count = len(re.findall(r'\b{}\b'.format(re.escape(part)), context, re.IGNORECASE))
                    skill_counter[skill] += partial_count
    
    skill_sections = extract_skill_sections(context)
    combined_sections = " ".join(skill_sections)
    
    for skill in skill_counter:
        if re.search(r'\b{}\b'.format(re.escape(skill)), combined_sections, re.IGNORECASE):
            skill_counter[skill] += 5  # Boost skills mentioned in skill sections
    
    return [skill for skill, count in skill_counter.most_common() if count > 0]

def analyze_resume_file(file_path):
    """Process a resume file and extract skills"""
    try:
        if file_path.endswith('.pdf'):
            # For PDF files
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
        elif file_path.endswith('.docx'):
            # For DOCX files
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        elif file_path.endswith('.txt'):
            # For text files
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        else:
            return f"Unsupported file format: {file_path}"
        
        skills = extract_skills_from_resume(text)
        return skills
    except Exception as e:
        return f"Error processing file: {str(e)}"

# skills = analyze_resume_file("resume.pdf")
# print(skills)