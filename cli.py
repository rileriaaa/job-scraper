from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
import json

def indeed_jobs():
    jobs = []
    start = 0
    
    try:
        
        title = input("Enter job title: ").strip()
        location = input("Enter preferred location: ").strip()
        total_jobs = int(input("Enter value to be scraped: ").strip())
            
    except Exception as e:
        return {'error': str(e)}
    
    
    encoded_title = quote(title)
    encoded_location = quote(location)
    
    try:
        while len(jobs) < total_jobs:
            url = f'https://ph.indeed.com/jobs?q={encoded_title}&l={encoded_location}&start=0'
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for job in job_cards:
                try:
                    jobTitle = job.find('h2', class_='jobTitle css-1o1rnx9 eu4oa1w0').text.strip()
                    company = job.find('span', class_='company-name').text.strip()
                    locationn = job.find('div', class_='css-1f06pz4 eu4oa1w0').text.strip()
                    job_salary = job.find('li', class_='salary-snippet-container mosaic-provider-jobcards-fswglz e1xnxm2i0').strip()
                    
                    job.append({
                        'job': jobTitle,
                        'company': company,
                        'location': locationn,
                        'salary': job_salary
                    })
                    
                    if len(job) >= total_jobs:
                        break
                    
                    start += 10
                    time.sleep(1)
                    
                except:
                    continue
                    
    except Exception as e:
        return {'error': str(e)}
    
    return jobs


jobs = indeed_jobs()
 
print(json.dumps(jobs, indent=2))