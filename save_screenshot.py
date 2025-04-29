import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
import base64
import time
import os

def get_page_content(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except Exception as e:
        return f"Error fetching page: {e}"

def save_html_page(url, filename):
    content = get_page_content(url)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved HTML content to {filename}")

# Save the HTML files for manual viewing
save_html_page("http://localhost:5000/", "homepage.html")
save_html_page("http://localhost:5000/tooltip-demo", "tooltip_demo.html")
save_html_page("http://localhost:5000/world-mood", "world_mood.html")

print("HTML files have been saved. You can view them manually to see the project's interface.")