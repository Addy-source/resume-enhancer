<<<<<<< HEAD
print("hello world")
=======
import requests
from bs4 import BeautifulSoup

# job_title = "Software Engineer"
job_title = input("Enter a job title: ")

# Step 1: Search for the job title
search_url = f"https://www.onetonline.org/find/quick?s={job_title.replace(' ', '+')}"
headers = {"User-Agent": "Mozilla/5.0"}  # Avoid bot detection
response = requests.get(search_url, headers=headers)

if response.status_code != 200:
    print("Error: Could not access O*NET search page.")

soup = BeautifulSoup(response.text, "html.parser")

# Find all job titles and links using data-text
job_options = []
for job_td in soup.find_all("td", {"data-title": "Occupation"}):
    job_link = job_td.find("a", href=True, string=True)
    job_title_text = job_td.get("data-text", "").strip() 
    job_url = job_link["href"]
    job_code = job_link["href"].split("/")[-1]  # Extract job code
    # print(job_code)
    job_options.append((job_title_text, job_url, job_code))
    # print(job_options)

selected_job_options = job_options[:10] #to do : change to 15

print("\nAvailable Job Titles:\n")
for idx, (title, link, code) in enumerate(selected_job_options, start=1):
    print(f"{idx}. {title} ({link})")

choice = int(input("\nEnter the number of the job that best matches your dream occupation: ")) - 1

if 0 <= choice < len(job_options):
    selected_title, selected_link, selected_code= job_options[choice]
    print(f"\nYou selected: {selected_title}")
    print(f"Job URL: {selected_link}")
else:
    print("\nInvalid choice. Exiting.")


demand_url = f"https://www.onetonline.org/link/demand/{selected_code}"
response = requests.get(demand_url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all technology skill elements
    tech_skills = [td["data-text"] for td in soup.find_all("td", class_="w-85 mw-10e sorter-text")]

    if tech_skills:
        print("Technology Skills:")
        for skill in tech_skills:
            print(f"- {skill}")
    else:
        print("No technology skills found.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")


#  TO DO : CLEAN UP THE CODE FOR EXTENSIVE ERROR HANDLING 
>>>>>>> 18b555d (Added my code to the praise branch)
