import requests, os
from dotenv import load_dotenv
load_dotenv()

def fetchfromDB(url):
    headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.getenv("TMDB_API_KEY")
    }

    response = requests.get(url, headers=headers)

    if response.status_code!=200:
         raise Exception("Failed to fetch data from TMDB")
    
    return response.text
