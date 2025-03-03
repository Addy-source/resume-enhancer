def find_missing_skills(user_skills, required_skills):
    """
    Compares user's skills with required skills and returns the missing skills.
    :param user_skills: List of skills from the user's resume.
    :param required_skills: List of skills required for the job.
    :return: List of missing skills.
    """
    user_skills_set = set(user_skills)
    required_skills_set = set(required_skills)
    missing_skills = required_skills_set - user_skills_set
    return list(missing_skills)

