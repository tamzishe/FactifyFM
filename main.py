from dotenv import load_dotenv
import os
import base64
from requests import post, get 
import json

load_dotenv()

client_id= os.getenv("CLIENT_ID")
client_secret= os.getenv("CLIENT_SECRET")

def getToken():
    authString = client_id + ":" + client_secret
    authBytes = authString.encode("utf-8")
    authBase64 = str(base64.b64encode(authBytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " +authBase64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    jsonResult = json.loads(result.content)
    token = jsonResult["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artistName):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query= f"?q={artistName}&type=artist&limit=1"

    queryURL = url + query
    result = get(queryURL, headers=headers)
    jsonResult = json.loads(result.content)["artists"]["items"]
    if len(jsonResult)==0:
        print("Could not find an artist with this name")
        return None
    return jsonResult[0]

def getSongsByArtist(token, artistId):
    url = f"https://api.spotify.com/v1/artists/{artistId}/top-tracks?country=CA"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    jsonResult = json.loads(result.content)["tracks"]
    return jsonResult

def getAlbumsByArtist(token, artistId):
    url = f"https://api.spotify.com/v1/artists/{artistId}/albums?country=CA&limit=50"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    jsonResult = json.loads(result.content)["items"]
    return jsonResult
def getArtistInfo(token, artistId):
    url = f"https://api.spotify.com/v1/artists/{artistId}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    jsonResult = json.loads(result.content)
    return jsonResult
