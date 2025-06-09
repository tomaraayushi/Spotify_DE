import requests
import json

from typing import Callable
from spotify-authentication import get_auth_header

# Function to get new releases
def get_paginated_new_releases(base_url:str, access_token:str, get_token: Callable, **kwargs):
    """Performs paginated calls to the new release endpoint. Manages token refresh when required"""
    headers = get_auth_header(access_token)
    request_url = base_url
    new_releases_data = []

    try:
        while request_url:
            response = requests.get(url=request_url, headers=headers)
            
            if response.status_code == 401:
                token_response = get_token(**kwargs)
                if access_token in token_response:
                    access_token = token_response['access_token']
                    headers = get_auth_header(access_token)
                    continue
                else:
                    print(f"Failed to refresh token")
                    return []
                
            response_json = response.json()
            new_releases_data.extend(response_json['albums']['items'])
            request_url = response_json['albums']['next']

        return new_releases_data

    except Exception as err:
        print(f"Error: {err}")
        return {}
    
# Function to get albums tracks
def get_paginated_albums_tracks(base_url: str, album_id:str, access_token:str, get_token: Callable, **kwargs):
    """Performs paginaetd calls to the album/{album_id}/tracks endpoint"""

    headers = get_auth_header(access_token)

    request_url = f"{base_url}/{album_id}/tracks"
    album_data = []

    try:
        while request_url:
            response = requests.get(url = request_url, headers=headers)

            if response.status_code == 401:
                token_response = get_token(**kwargs)
                if access_token in token_response:
                    headers = get_auth_header(access_token = token_response.get('access_token'))
                    continue

                else:
                    print(f"Failed to refresh token")
                    return []
            
            response_json = response.json()
            album_data.extend(response_json.get('items'))
            request_url = response_json.get('next')

        return album_data

    except Exception as err:
        print(f"Error: {err}")
        return {}
    
    

                
        



