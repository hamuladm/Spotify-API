'''
Laboratorna 2
'''


from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json


load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_token() -> str:
    '''
    () -> str
    Gets token
    '''
    auth_str = client_id + ':' + client_secret
    auth_bytes = auth_str.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type' : 'application/x-www-form-urlencoded'
    }

    data = {'grant_type': 'client_credentials'}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token  = json_result['access_token']

    return token


def get_auth_header(token: str) -> dict:
    '''
    (str) -> dict
    Returns header
    '''
    return {'Authorization': 'Bearer ' + token}


def search_for_artist(token: str, artist: str) -> dict:
    '''
    (str, str) -> dict
    Searches for artist
    '''
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist}&type=artist,track&limit=1'

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)
    if not json_result:
        print('No such artist!')
        return
    return json_result


def print_result(artist: str) -> list:
    '''
    Prints result
    '''
    token = get_token()
    result = search_for_artist(token, artist)
    print(f"ID of the artist: {result['artists']['items'][0]['id']}")
    print(f"Full name of the artist: {result['artists']['items'][0]['name']}")
    print(f"The most popular track: {result['tracks']['items'][0]['name']}")
    print(f"Available countries for the track: {' , '.join(result['tracks']['items'][0]['available_markets'])}")

    return result['tracks']['items'][0]['available_markets']



if __name__ == '__main__':
    # token = get_token()
    # result = search_for_artist(token, 'Ghostemane')

    # print(result['artists']['items'][0]['id']) # ID of the artist
    # print(result['artists']['items'][0]['name']) # Full name of the artist
    # print(result['tracks']['items'][0]['name']) # The most popular track
    # print(result['tracks']['items'][0]['available_markets']) # Available countries for the track

    print_result('Type O Negative')
