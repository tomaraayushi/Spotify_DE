# Understanding the basics of API 
import requests
import os
import json 

from typing import Dict, Any, Callable
from dotenv import load_dotenv

# Get Token
load_dotenv('./src/env', override= True)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Get Token Function

def get_token(client_id: str, client_secret:str, url: str) -> Dict[Any, Any]:
    """Allows to perform a POST request o obtain an access token
    
    Args:
        client_id (str): The client id for the API
        client_secret(str): The client secret for the API
        url(str): The URL to the API endpoint
        
    Returns:
        Dict[Any, Any]: Dictionary containing the access token
    """

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'grant_type': 'client_credentials', 
        'client_id': client_id,
        'client_secret': client_secret
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        print(type(response))
        response.raise_for_status()
        response_json = json.loads(response.content)

    except Exception as err:
        print(f"Error: {err}")
        return {}
    

URL_TOKEN = "https://accounts.spotify.com/api/token"
token = get_token(CLIENT_ID, CLIENT_SECRET, URL_TOKEN)

print(token)




