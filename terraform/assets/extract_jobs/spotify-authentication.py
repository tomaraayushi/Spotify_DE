import requests
import json

from typing import Any, Dict

def get_token(url:str, client_id:str, client_secret:str)-> Dict[Any, Any]:
    """Allows us to perform a POST request to obtain an access token
    
    Args:
        url(str): URL to perform the request
        client_id(str): App client id
        client_secret(str): App client secret
         
    Returns:
        Dict[Any, Any]: Dictionary containing the access token
         
    """

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    try:
        response = requests.post(url= url, headers= headers, data=payload)
        response.raise_for_status()
        response_json = json.loads(response.content)

        return response_json
    
    except Exception as err:
        print(f"Error: {err}")
        return {}
    

def get_auth_header(access_token:str) -> Dict[str, str]:
    return {'Authorization' : f'Bearer {access_token}'}

