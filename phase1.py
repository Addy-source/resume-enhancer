import requests
from bs4 import BeautifulSoup

def get_job_tech_skills(job_title):
    search_url = f"https://www.onetonline.org/find/quick?s={job_title.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Avoid bot detection
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        return "Error: Could not access O*NET search page."
    
    soup = BeautifulSoup(response.text, "html.parser")
    job_options = []
    
    for job_td in soup.find_all("td", {"data-title": "Occupation"}):
        job_link = job_td.find("a", href=True, string=True)
        job_title_text = job_td.get("data-text", "").strip()
        job_url = job_link["href"]
        job_code = job_link["href"].split("/")[-1]  # Extract job code
        job_options.append((job_title_text, job_url, job_code))
    
    selected_job_options = job_options[:10]  # Change to 15 if needed
    
    print("\nAvailable Job Titles:\n")
    for idx, (title, link, code) in enumerate(selected_job_options, start=1):
        print(f"{idx}. {title} ({link})")
    
    choice = int(input("\nEnter the number of the job that best matches your dream occupation: ")) - 1
    
    if 0 <= choice < len(job_options):
        selected_title, selected_link, selected_code = job_options[choice]
        print(f"\nYou selected: {selected_title}")
        print(f"Job URL: {selected_link}")
    else:
        return "\nInvalid choice. Exiting."
    
    demand_url = f"https://www.onetonline.org/link/demand/{selected_code}"
    response = requests.get(demand_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        tech_skills = [td["data-text"] for td in soup.find_all("td", class_="w-85 mw-10e sorter-text")]
        return tech_skills

# # Example usage
# job_title = input("Enter a job title: ")
# print(get_job_tech_skills(job_title))
