"""NASA API integration for Flokapp"""
import requests
import json
import os

# NASA API key - users should get their own from https://api.nasa.gov
API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')  # DEMO_KEY for testing
BASE_URL = 'https://api.nasa.gov'

class NASAAPI:
    """Class to handle NASA API calls"""

    @staticmethod
    def get_apod():
        """Get Astronomy Picture of the Day"""
        url = f"{BASE_URL}/planetary/apod?api_key={API_KEY}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    @staticmethod
    def get_mars_photos(rover='curiosity', sol=1000, camera='NAVCAM'):
        """Get Mars rover photos"""
        url = f"{BASE_URL}/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&camera={camera}&api_key={API_KEY}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json().get('photos', [])
        except requests.RequestException:
            return []

    @staticmethod
    def get_earth_imagery(lat=29.78, lon=-95.33, date='2020-01-01'):
        """Get Earth imagery from EPIC"""
        url = f"{BASE_URL}/EPIC/api/natural/date/{date}?api_key={API_KEY}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return []

    @staticmethod
    def get_space_weather():
        """Get space weather data from DONKI"""
        url = f"{BASE_URL}/DONKI/CME?startDate=2024-01-01&endDate=2024-01-31&api_key={API_KEY}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return []

    @staticmethod
    def get_near_earth_objects(start_date='2024-01-01', end_date='2024-01-07'):
        """Get near Earth objects data"""
        url = f"{BASE_URL}/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={API_KEY}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {}

    @staticmethod
    def get_mars_weather():
        """Get Mars weather data from InSight"""
        url = f"{BASE_URL}/insight_weather/?api_key={API_KEY}&feedtype=json&ver=1.0"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {}