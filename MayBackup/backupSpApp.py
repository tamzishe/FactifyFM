from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from main import *

token = getToken()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        artist = request.form['content']
        artistId = search_for_artist(token, artist)["id"]
        artist = getArtistInfo(token, artistId)
        jsonSongs= getSongsByArtist(token, artistId)
        jsonAlbums= getAlbumsByArtist(token, artistId)
        img = artist["images"][0]['url']
        songTitles=[]
        songYear=[]
        songCover=[]
        for song in jsonSongs: #sort these songs' attributes into seperate indexed lists
            songTitles.append(song['name'])
            try:
                songYear.append(song['album']['release_date'])
            except:
                songYear.append("no date")
            try:
                songCover.append(song['album']['images'][0]['url'])
            except:
                songCover.append(img)
        songs = [songTitles] + [songYear] + [songCover] # titles is 0, year is 1, cover is 2
        albumTitles=[]
        albumYear=[]
        albumCover=[]
        for album in jsonAlbums: #sort these albums' attributes into seperate indexed lists
            if album['album_type'] == "album" or album['album_type'] == "compilation":
                albumTitles.append(album['name'])
                try:
                    albumYear.append(album['release_date'][0:4])
                except:
                    albumYear.append("no date")
                try:
                    albumCover.append(album['images'][0]['url'])
                except:
                    albumCover.append(img)
            else:
                pass
        albums = [albumTitles] + [albumYear] + [albumCover] + [len(albumTitles)]
        return render_template('viewartist.html', artistName = artist["name"], image = img, songs=songs, albums=albums)#img
    else:
        return render_template('home.html')

if __name__== "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)