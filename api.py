from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

app = FastAPI()

def indeed_jobs(title, location, total_jobs):
    jobs = []
    start = 0
    
    encoded_title = quote(title)
    encoded_location = quote(location)
    
    try:
        while len(jobs) < total_jobs:
            url = f'https://ph.indeed.com/jobs?q={encoded_title}&l={encoded_location}&start={start}'
            
            headers = {
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Cache-Control': 'max-age=0',
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            if not job_cards:
                break
            
            for job in job_cards:
                try:
                    jobTitle = job.find('h2', class_='jobTitle css-1o1rnx9 eu4oa1w0').text.strip()
                    company = job.find('span', class_='css-19eicqx eu4oa1w0').text.strip()
                    locationn = job.find('div', class_='css-1f06pz4 eu4oa1w0').text.strip()
                    salary_element = job.find('li', class_='salary-snippet-container mosaic-provider-jobcards-fswglz e1xnxm2i0')
                    job_salary = salary_element.strip() if salary_element else "Not disclosed"
                    link = job.find('a', class_='jcs-JobTitle css-1baag51 eu4oa1w0')['href']
                    
                    jobs.append({
                        'job': jobTitle,
                        'company': company,
                        'location': locationn,
                        'salary': job_salary,
                        'url': link
                    })
                    
                    if len(jobs) >= total_jobs:
                        break
                    
                except:
                    continue
            
            start += 10
            time.sleep(1)
                    
    except Exception as e:
        return {'error': str(e)}
    
    return jobs

def jobstreet_jobs(title, location, total_jobs):
    jobs = []
    page = 1
    
    encoded_title = title.replace(" ", "-")
    encoded_location = location.replace(" ", "-")
    
    try:
        while len(jobs) < total_jobs:
            url  = f"https://ph.jobstreet.com/{encoded_title}-jobs/in-{encoded_location}?page={page}"

            headers = {
                
            }
        
    except Exception as e:
        return {'error': str(e)}
    
    return jobs
    
@app.get('/')
def home():
    return{
        'message': 'Job Scraper API - /help/help - to see all directories'
    }
    
@app.get('/jobstreet/search')
def tangina(title: str, location: str = "Metro Manila", total_jobs: int = 20):
    jobs = jobstreet_jobs(title, location, total_jobs)
    return {
        'count': len(jobs),
        'jobs': jobs
    }
    
    

@app.get('/indeed/search')
def indeed(
    title: str,
    location: str = "Philippines",
    total_jobs: int = 20
):
    jobs = indeed_jobs(title, location, total_jobs)
    
    return{
        'count': len(jobs),
        'jobs': jobs
    }