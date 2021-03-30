import requests
import time


def get_response(url):
    """http get request"""
    for _ in range(15):
        response = requests.get(url)
        if response.status_code == 200:
            return response
        time.sleep(1)
    raise ValueError("URL DIE")
