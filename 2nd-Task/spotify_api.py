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


def get_token():
    '''
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


def get_auth_header(token):
    '''
    Returns header
    '''
    return {'Authorization': 'Bearer ' + token}


def search_for_artist(token, artist):
    '''
    Searches for artist
    '''
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist}&type=track&limit=5'

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)['tracks']
    if not json_result:
        print('No such artist!')
        return
    return json_result


def search_for_top_tracks(token, artist_id):
    '''
    Searches for top artist's track
    '''
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_header(token)
    
    result = get(url, headers = headers)
    json_result = json.loads(result.content)['tracks']
    if not json_result:
        print('No such artist!')
        return
    return json_result



if __name__ == '__main__':
    token = get_token()
    result = search_for_artist(token, 'Metallica')
    for song in result['items']:
        print(song['name'])
    # artist_id = result['id']
    # songs = search_for_top_tracks(token, artist_id)

    # for song in songs:
    #     print(song['name'])
