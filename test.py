def get_job_skills(job_title):
    job_skills = {
        "software engineer": ["Python", "Java", "Algorithms", "Data Structures", "Git", "Databases"],
        "data scientist": ["Python", "R", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
        "web developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "UI/UX"],
        "network engineer": ["Networking", "Cisco", "Routing & Switching", "Security", "Linux"],
        "cybersecurity analyst": ["Penetration Testing", "SIEM", "Firewalls", "Cryptography", "Ethical Hacking"],
        "accountant": ["Financial Analysis", "Excel", "Taxation", "Bookkeeping", "Auditing"],
        "graphic designer": ["Adobe Photoshop", "Illustrator", "Typography", "Branding", "UI/UX Design"],
    }

    return job_skills.get(job_title.lower(), ["Skills not found for this job title."])

# Example usage
job = input("Enter a job title: ")
skills = get_job_skills(job)
print(f"Relevant skills for {job}: {', '.join(skills)}")