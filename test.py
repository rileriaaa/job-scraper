from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time




def wellfound_jobs(title, total_jobs):
    jobs = []
    page = 1
    
    encoded_title = title.replace(" ", "-")

    try:
        while len(jobs) < total_jobs:
            url = f'https://wellfound.com/role/l/{encoded_title}/philippines?page={page}'
            
            headers = {
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            job_cards = soup.find_all("div", class_='mb-6 w-full rounded border border-gray-400 bg-white')
            
            if not job_cards:
                break
            
            for job in job_cards:
                try:
                    company = job.find("h2", class_='inline text-md font-semibold').text.strip()
                    jobTitle = job.find("a", class_='mr-2 text-sm font-semibold text-brand-burgandy hover:underline').text.strip()
                    salary = job.find("span", class_='pl-1 text-xs').text.strip()
                    location = job.find("span", class_='pl-1 text-xs').text.strip()
                    link = job.find("a", class_='mr-2 text-sm font-semibold text-brand-burgandy hover:underline')['href']
                    
                    jobs.append({
                        'title': jobTitle,
                        'company': company,
                        'salary': salary,
                        'location': location,
                        'url': link
                    })
                    
                    if len(jobs) >= total_jobs:
                        break
                    
                except:
                    continue
                
                page += 1
                time.sleep(1) 
    
        return jobs
    
    except Exception as e:
        return {'error': str(e)}
    
jobs = wellfound_jobs("python developer", 10)
print(jobs)