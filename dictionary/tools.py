# tools.py
'''Module for common tools'''

import requests
from bs4 import BeautifulSoup

def get_soup(url):
    '''
    Get BeautifulSoup object for a URL

    Args:
        url (str): URL to fetch and parse

    Returns:
        BeautifulSoup: BeautifulSoup object for the URL, or None if unable to retrieve
    '''
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None