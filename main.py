import feedparser
import dateutil.parser
from datetime import *
from dateutil.relativedelta import *
import pytz; utc = pytz.UTC
import json
import requests
from pprint import pprint
import urllib

#### General gist of the program:
# Pull list youtube channels from file
# check all of their RSS against lastrun time
# Search each new track on Spotify
    # If cannot find track, add to text file / download local file
# Get Spotify track ID
# Add Spotify track ID to playlist
# Automate running this script every so often (1 day is probably plenty)

spotifyClientID = ""
spotifyClientSecret = ""
spotifyAccessToken = ""
spotifyRefreshToken = ""
spotifyPlaylistID = "1YqE47KbtLcYRFaVrr4Sl9"

def refreshAccessToken(spotifyRefreshToken, spotifyClientID, spotifyClientSecret):
    # Refresh spotifyAccessToken using spotifyRefreshToken
    r = requests.post("https://accounts.spotify.com/api/token", data = {"grant_type": "refresh_token", "refresh_token": spotifyRefreshToken, "client_id": spotifyClientID, "client_secret": spotifyClientSecret})
    print("Refreshing access token: ", r.status_code, r.reason)
    #print(r.text)

    response = json.loads(r.text)
    #print(response)

    spotifyAccessToken = response["access_token"]
    if("refresh_token" in response):
        spotifyRefreshToken = response["refresh_token"]
    #else:
        # refresh_token didn't change

    # write new access token and maybe new refresh token to file
    with open('spotify.json', "w") as f:
        data = {}
        data['spotifyClientID'] = spotifyClientID
        data['spotifyClientSecret'] = spotifyClientSecret
        data['spotifyAccessToken'] = spotifyAccessToken
        data['spotifyRefreshToken'] = spotifyRefreshToken
        json_data = json.dump(data, f)

def searchAndAddToSpotifyPlaylist(trackname):
    #fucking spotify api now
    print("Attempting to add " + trackname + " to Spotify ingest playlist...")

    # Search Spotify for trackname
    headers = {"Authorization": "Bearer " + spotifyAccessToken}
    params = {"q": trackname.lower().replace("lyrics", "").replace("ft.", ""), "type": "track"}
    r1 = requests.get("https://api.spotify.com/v1/search", headers = headers, params = params)
    #print(r1.status_code, r1.reason)
    #print("r1: " + r1.text)
    search_result = json.loads(r1.text)
    if((not "tracks" in search_result) or len(search_result["tracks"]["items"]) == 0):
        # there isn't anything from this search, we lose
        print("Could not locate " + trackname + " on Spotify. Writing to file...?")
        with open("fails.txt", "a") as f:
            f.write(trackname + "\n")
    else:
        # yay something showed up ,lets just save the uri of the first result
        uri = search_result["tracks"]["items"][0]["uri"]

        # Add two tracks to ingest playlist
        headers = {"Authorization": "Bearer " + spotifyAccessToken, "Content-Type": "application/json"}
        shitjson = {"uris": [uri], "position": 0}
        r2 = requests.post("https://api.spotify.com/v1/playlists/" + spotifyPlaylistID + "/tracks", headers = headers, json = shitjson)
        #print(r2.status_code, r2.reason)
        #print("r2: " + r2.text)
        print("Added " + trackname + " to Ingest playlist.")

# Load spotify credentials from file
with open('spotify.json') as f:
    data = json.load(f)

    spotifyClientID = data["spotifyClientID"]
    spotifyClientSecret = data["spotifyClientSecret"]
    spotifyAccessToken = data["spotifyAccessToken"]
    spotifyRefreshToken = data["spotifyRefreshToken"]

# Read last run timestamp to file
timefilePath = "lastrun"
with open(timefilePath, "r") as timefile:
    timefile = timefile.read()
    lastruntime = dateutil.parser.parse(timefile)
    #print('test: ' + lastruntime.isoformat())

NOW = datetime.now()
print("Script was last run this much time ago: " + str(NOW - lastruntime))

# refresh access token using refresh token to start
refreshAccessToken(spotifyRefreshToken, spotifyClientID, spotifyClientSecret)

with open('youtube.json') as f:
    data = json.load(f)

    # pprint(data)
    print("Channels loaded from 'youtube.json': ")
    for channel in data["youtube"]:
        name = channel['name']
        channelid = channel['id']
        print(" - " + name + ": " + channelid)

        # grab RSS upload feed for channel
        rss = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=" + channelid)
        for post in rss.entries:
            # for each upload, we need to check the upload time

            uploadtime = dateutil.parser.parse(post.published)
            #print(post.title + " at " + uploadtime.isoformat())

            # if(upload date > lastrun): do shit with it
            # if upload date is farther in the future than last run time, do shit with it
            #if(utc.localize(uploadtime) > utc.localize(lastruntime)):

            uploadtime = uploadtime.replace(tzinfo=utc) - timedelta(hours=6)
            lastruntime = lastruntime.replace(tzinfo=utc)

            #print("Video uploaded at " + str(uploadtime))
            #print("The script was last run at " + str(lastruntime))
            #print("Right now it is " + str(datetime.now()))
            distance = uploadtime - lastruntime
            #print(str(distance)) - doesnt printcorrectly ???, adds a day for some reason

            if(uploadtime.replace(tzinfo=utc) > lastruntime.replace(tzinfo=utc)):
                # add to spotify playlist
                print("New upload: " + post.title + " at " + uploadtime.isoformat())
                searchAndAddToSpotifyPlaylist(post.title)

# Write current time to file at end of execution
with open(timefilePath, "w") as timefile:
    timefile.write(datetime.now().isoformat())
    print("Wrote current datetime to " + timefilePath + ".")
