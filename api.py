from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

app = FastAPI()

def indeed_jobs(title, location, total_jobs):
    jobs = []
    start = 0
    
    encoded_title = quote(title)
    encoded_location = quote(location)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        while len(jobs) < total_jobs:
            url = f'https://ph.indeed.com/jobs?q={encoded_title}&l={encoded_location}&start={start}'
            driver.get(url)
            time.sleep(3)
            
            
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
        driver.quit()
        return {'error': str(e)}
    
    driver.quit()
    return jobs

def jobstreet_jobs(title, location, total_jobs):
    jobs = []
    page = 1
    
    encoded_title = title.replace(" ", "-")
    encoded_location = location.replace(" ", "-")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')  
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        while len(jobs) < total_jobs:
            url = f"https://ph.jobstreet.com/{encoded_title}-jobs/in-{encoded_location}?page={page}"
            print(f"Fetching: {url}")
            
            driver.get(url)
            time.sleep(5)  
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            job_cards = soup.find_all("div", class_='lsj4yq0')
            print(f"Found {len(job_cards)} job cards")
            
            if not job_cards:
                print("No job cards found, breaking...")
                break
            
            for job in job_cards:
                try:
                    jobTitle = job.find("a", class_='lsj4yq0 lsj4yqg lsj4yq8  lsj4yq0 lsj4yqg lsj4yq8 _6qwuykd _6qwuykf')
                    jobDesc = job.find("span", class_='lsj4yq0 _2t4ma4x _1ruehm40 _1ruehm41 _1ruehm41u _1ruehm44 _1rtxcgx4')
                    jobLink = job.find("a", class_='lsj4yq0 lsj4yqg lsj4yq8  lsj4yq0 lsj4yqg lsj4yq8 _6qwuyke')
                    company = job.find("a", class_='lsj4yq0 lsj4yqg lsj4yq8  lsj4yq0 lsj4yqg lsj4yq8 _1pcuioo0 _1pcuioo1')
                    jobLocation = job.find("a", class_='lsj4yq0 lsj4yqg lsj4yq8  lsj4yq0 lsj4yqg lsj4yq8 _1pcuioo0 _1pcuioo2')
                    jobModality = job.find("span", class_='lsj4yq0 _2t4mafh')
                    jobSalary = job.find("span", class_='lsj4yq0 _1o2r1g52 _2t4ma4x _2t4ma0 _2t4mar _1o2r1g54')
                    
                    jobs.append({
                        'title': jobTitle.text.strip() if jobTitle else "null",
                        'company': company.text.strip() if company else "null",
                        'Description': jobDesc.text.strip() if jobDesc else "null",
                        'url': jobLink['href'] if jobLink else "null",
                        'location': jobLocation.text.strip() if jobLocation else "null",
                        'modality': jobModality.text.strip() if jobModality else "null",
                        'salary': jobSalary.text.strip() if jobSalary else 'not disclosed'
                    })
                
                    if len(jobs) >= total_jobs:
                        break
                    
                except Exception as e:
                    print(f"Error parsing job: {e}")
                    continue
            
            page += 1
            time.sleep(2)
        
    except Exception as e:
        driver.quit()
        return {'error': str(e)}
    
    driver.quit()
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