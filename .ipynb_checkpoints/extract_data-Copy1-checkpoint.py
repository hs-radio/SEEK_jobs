import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

# go through list of skills and mark if it is in job ad.
def skill_list(soup, skills_array):  
    req_skills = []  # required skills for this job

    # Check if any of the skills are in the HTML content
    for j, skill in enumerate(skills_array):
        if skill in soup.get_text():
            req_skills.append(skill)
    return req_skills

# Check the tags are found and print results
def check_tag(tag):    
    if tag:
        tag_object = tag.get_text(strip=True)
        return tag_object
    else:
        tag_object = "N/A"
        return None

# start on the SEEK search page and get the URLs of all the jobs.
def get_URLs(max_pages):
    full_urls = set()  # Use a set to remove duplicates
    for num in range(max_pages):
        # SEEK search URL
        base_url = "https://www.seek.com.au"
        url_SEEK_search = f"https://www.seek.com.au/data-engineer-jobs/in-Sydney-NSW-2000?page={num}"
        
        # Send a GET request to the website
        response = requests.get(url_SEEK_search)
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all anchor tags (<a>) with the href attribute
        links = soup.find_all('a', href=True)
        
        # Extract specific job URLs
        for link in links:
            href = link['href']
            if href.startswith("/job/") and not (href.endswith("jobCard") or href.endswith("cardTitle")):
                full_urls.add(base_url + href)  # Add to set to prevent duplicates
    
    # Convert back to a list
    unique_urls = list(full_urls)
    return unique_urls  # Return the deduplicated list

# find days ago job ad was posted and compute the date.
def get_post_date(soup):
    # Use regex to find the span containing "Posted Xd ago"
    span = soup.find("span", string=re.compile(r"Posted \d+d ago"))
    
    if span:
        # Extract just the number using regex
        match = re.search(r"(\d+)", span.text)
        if match:
            days = int(match.group(1))  # Convert to integer
            
            # Get current date and subtract days
            current_date = datetime.today().date()
            post_date = current_date - timedelta(days=days)
            return post_date
    else:
        return None

# get data from SEEK advertisement.
def get_job_data(soup, skills_array):
    # Find the <h1> tag with the specific class
    job_title_tag = soup.find("h1", class_="gepq850 eihuid4z i7p5ej0 i7p5ejl _18ybopc4 i7p5ejs i7p5ej21")
    company_tag = soup.find("span", class_="gepq850 eihuid4z eihuidi7 i7p5ej0 i7p5ej1 i7p5ej21 _18ybopc4 i7p5eja", attrs={"data-automation": "advertiser-name"})
    location_tag = soup.find("span", class_="gepq850 eihuid4z i7p5ej0 i7p5ej1 i7p5ej21 _18ybopc4 i7p5ej7", attrs={"data-automation": "job-detail-location"})
    employment_type_tag = soup.find("span", class_="gepq850 eihuid4z i7p5ej0 i7p5ej1 i7p5ej21 _18ybopc4 i7p5ej7", attrs={"data-automation": "job-detail-work-type"})
    salary_tag = soup.find("span", class_="gepq850 eihuid4z i7p5ej0 i7p5ej1 i7p5ej21 _18ybopc4 i7p5ej7", attrs={"data-automation": "job-detail-salary"})
    
    # check for each property
    job_title = check_tag(job_title_tag)
    company = check_tag(company_tag)
    location = check_tag(location_tag)
    employment_type = check_tag(employment_type_tag)
    salary = check_tag(salary_tag)
    post_date = get_post_date(soup)
    
    # save a variable with all the job properties
    job_props = [job_title, company, location, employment_type, salary, post_date]
    
    # see what skills are in job advertisement
    req_skills = skill_list(soup, skills_array)
    
    # return all extracted data
    return job_props, req_skills
