from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

def indeed_jobs(title, location, total_jobs):
    jobs = []
    
    encoded_title = quote(title)
    encoded_location = quote(location)
    
    url = f'https://ph.indeed.com/jobs?q={encoded_title}&l={encoded_location}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try different selectors
    print("Trying 'job_seen_beacon':")
    cards1 = soup.find_all('div', class_='job_seen_beacon')
    print(f"Found: {len(cards1)}")
    
    print("\nTrying 'jobsearch-SerpJobCard':")
    cards2 = soup.find_all('div', class_='jobsearch-SerpJobCard')
    print(f"Found: {len(cards2)}")
    
    print("\nTrying 'slider_container':")
    cards3 = soup.find_all('div', class_='slider_container')
    print(f"Found: {len(cards3)}")
    
    print("\nTrying 'cardOutline':")
    cards4 = soup.find_all('div', class_='cardOutline')
    print(f"Found: {len(cards4)}")
    
    # Save HTML to file to inspect
    with open('indeed_page.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("\nSaved HTML to indeed_page.html - check this file!")
    
    return []

indeed_jobs('backend developer', 'manila', 10)