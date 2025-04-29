import os
import time
import requests
from requests.exceptions import RequestException
from flask import Flask, render_template_string

print("Trying to fetch homepage...")
try:
    response = requests.get("http://localhost:5000/", timeout=5)
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        html_content = response.text
        print(f"Received HTML content of length: {len(html_content)}")
        # Print the first 200 characters to see if it's the expected content
        print(f"Content preview: {html_content[:200]}")
    else:
        print(f"Failed to get page, status code: {response.status_code}")
except RequestException as e:
    print(f"Error making request: {e}")

print("\nTrying to fetch tooltip demo...")
try:
    response = requests.get("http://localhost:5000/tooltip-demo", timeout=5)
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Received tooltip demo content of length: {len(response.text)}")
    else:
        print(f"Failed to get tooltip demo, status code: {response.status_code}")
except RequestException as e:
    print(f"Error making request: {e}")

print("\nTrying to fetch world mood demo...")
try:
    response = requests.get("http://localhost:5000/world-mood", timeout=5)
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(f"Received world mood demo content of length: {len(response.text)}")
    else:
        print(f"Failed to get world mood demo, status code: {response.status_code}")
except RequestException as e:
    print(f"Error making request: {e}")

print("\nTrying API endpoints...")
try:
    response = requests.get("http://localhost:5000/api/tooltips", timeout=5)
    print(f"Tooltips API status code: {response.status_code}")
    if response.status_code == 200:
        print(f"API response: {response.json()[:2]}")  # Print first two items
except RequestException as e:
    print(f"Error making API request: {e}")

print("\nChecking server process...")
os.system("ps -ef | grep -i python | grep -v grep")