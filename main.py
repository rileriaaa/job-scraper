from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time

app = FastAPI()

