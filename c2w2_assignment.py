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

        return response_json

    except Exception as err:
        print(f"Error: {err}")
        return {}
    

URL_TOKEN = "https://accounts.spotify.com/api/token"
token = get_token(CLIENT_ID, CLIENT_SECRET, URL_TOKEN)

#print(token)

# Authorization header function 
def get_auth_header(access_token: str) -> Dict[Any, Any]:
    return {"Authorization": f"Bearer {access_token}"}


# Some examples
# 1. Get New Releases
def get_new_releases(access_token: str, url: str, offset: int=0, limit: int=20, next: str="") -> Dict[Any, Any]:
    """Allows to perform a GET request to get new releases from Spotify
    
    Args:
        access_token(str): access token for authorization
        url(str): Base URL for new releases 
        offset(int, optional): Starting position(page offset for pagination). Defaults to 0
        limit(int, optional): Number of elements per page. Defaults to 20
        next(str, optional): Next URL to perform ext request.Defaults to ""
        
    Returns:
        Dict[Any, Any]: Request response 
        
    """

    if next == "":
        request_url = f"{url}?offset={offset}&limit={limit}"
    else:
        request_url = f"{next}"

    headers = get_auth_header(access_token)

    try:
        response = requests.get(url=request_url, headers=headers)
        response.raise_for_status()
        response_json = response.json()

        return response_json
    
    except Exception as err:
        print(f"Error: {err}")
        return {}
    
URL_GET_NEW_RELEASES = "https://api.spotify.com/v1/browse/new-releases"
new_releases = get_new_releases(access_token=token.get('access_token'), url=URL_GET_NEW_RELEASES)
#print(new_releases) 

#print(new_releases['albums'].keys())

total = new_releases.get('albums').get('total')
print(total)


