import requests
from bs4 import BeautifulSoup

url = "https://ph.jobstreet.com/software-engineer-jobs/in-Metro-Manila?page=1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

soup = BeautifulSoup(response.text, 'html.parser')
job_cards = soup.find_all("div", class_='lsj4yq0')
print(f"Job cards found: {len(job_cards)}")