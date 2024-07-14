from flask import Flask, render_template, url_for, request, redirect
from main import *

global token
token = getToken()
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            artist, jsonSongs, jsonAlbums, img = grabArtist(token)
            songs = grabSongs(jsonSongs, img)
            albums = grabAlbums(jsonAlbums, img)
            return render_template('viewartist.html', artistName = artist["name"], image = img, songs=songs, numSong = len(songs[0]), albums=albums, genre=artist['genres'], genres=len(artist['genres']), popularity=artist['popularity'])#img
        except:
            return "Server Error: Please Restart", 404
    else:
        return render_template('home.html')

def grabArtist(token): #this function grabs the essentials for the program, the artist, their songs and albums in json response format
    artist = request.form['content']
    artistId = search_for_artist(token, artist)["id"]
    artist = getArtistInfo(token, artistId)
    jsonSongs= getSongsByArtist(token, artistId)
    jsonAlbums= getAlbumsByArtist(token, artistId)
    try: #try to find the artists profile image
        img = artist["images"][0]['url'] 
    except: #cant find it? use placeholder
        img = url_for('static', filename='images/noArtist.png')
    return artist, jsonSongs, jsonAlbums, img
            
def grabSongs(jsonSongs, img):
    songTitles=[] #set up these lists
    songYear=[]
    songCover=[]
    for song in jsonSongs: #sort these songs' attributes into seperate indexed lists
        if len(song['name'])<40:
            songTitles.append(song['name'])
        else:
            songTitles.append(song['name'][0:40]+"...")
        try:
            songYear.append(song['album']['release_date'])
        except:
            songYear.append("no date")
        try:
            songCover.append(song['album']['images'][0]['url'])
        except:
            songCover.append(img)
    songs = [songTitles] + [songYear] + [songCover] # titles is 0, year is 1, cover is 2
    return songs

def grabAlbums(jsonAlbums, img):
    albumTitles=[]
    albumYear=[]
    albumCover=[]
    for album in jsonAlbums: #sort these albums' attributes into seperate indexed lists
        if (album['album_type'] == "album" or album['album_type'] == "compilation") and album['album_group'] != "appears_on": # appears on is from issue with jayz showing other projects
            if len(album['name'])<40: #if the album name is too long, just cut it off for clarity
                albumTitles.append(album['name'])
            else:
                albumTitles.append(album['name'][0:40]+"...") 
            try: 
                albumYear.append(album['release_date'][0:4])
            except:
                albumYear.append("No Date")
            try: 
                albumCover.append(album['images'][0]['url'])
            except:
                albumCover.append(img)
        else:
            pass
    albums = [albumTitles] + [albumYear] + [albumCover] + [len(albumTitles)]
    return albums

if __name__== "__main__":
    app.run(debug=True)