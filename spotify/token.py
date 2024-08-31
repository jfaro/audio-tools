import json
import os
import requests
import tempfile
import time
from typing import Optional


TOKEN_URL = "https://accounts.spotify.com/api/token"
TOKEN_PATH = os.path.join(tempfile.gettempdir(), "spotify-tools", "spotify.token")

def assert_token_dir():
    token_dir = os.path.dirname(TOKEN_PATH)
    if not os.path.isdir(token_dir):
        print("Creating token directory at", token_dir)
        os.mkdir(token_dir)


def load_access_token() -> Optional[str]:
    assert_token_dir()
    if not os.path.isfile(TOKEN_PATH):
        print("No token file at", TOKEN_PATH)
        return None
    
    print("Loading token from file", TOKEN_PATH)
    with open(TOKEN_PATH, 'r') as tokenfile:
        result = tokenfile.read()
        parsed = json.loads(result)
        max_age = parsed["expires_in"]
        token_age = time.time() - os.path.getmtime(TOKEN_PATH)
        if token_age > max_age:
            print("Cached token expired")
            return None
        return parsed["access_token"]


def save_access_token(token: str, expires_in: int):
    assert_token_dir()
    print("Saving token to file", TOKEN_PATH)
    with open(TOKEN_PATH, 'w') as f:
        json.dump({
            "access_token": token,
            "expires_in": expires_in
        }, f)
    

def request_access_token(client_id: str, client_secret: str) -> tuple[str, int]:
    print("Requesting access token")
    headers = { 'Content-type': 'application/x-www-form-urlencoded' }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    parsed = json.loads(response.text)
    return parsed["access_token"], parsed["expires_in"]


def get_access_token(client_id: str, client_secret: str) -> str:
    token = load_access_token()
    if token is None:
        token, expires_in = request_access_token(client_id, client_secret)
        save_access_token(token, expires_in)
    return token
    