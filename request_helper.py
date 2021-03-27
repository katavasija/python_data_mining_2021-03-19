import requests
import time

def get_response(url):
    """http get request"""
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            return response
        time.sleep(1)


def get_url_with_params(url, params_dict):
    from requests.models import PreparedRequest
    req = PreparedRequest()
    req.prepare_url(url, params_dict)
    return req.url