from flask import Flask, request, jsonify
import requests
import base64
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

def get_spotify_token():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    auth_str = f"{client_id}:{client_secret}"
    auth_b64 = base64.b64encode(auth_str.encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if response.status_code != 200:
        print('Error:', response.status_code, response.json())
        response.raise_for_status()
    
    return response.json()['access_token']

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    token = get_spotify_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track', headers=headers)
    
    if response.status_code != 200:
        print('Error:', response.status_code, response.json())
        response.raise_for_status()
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)

