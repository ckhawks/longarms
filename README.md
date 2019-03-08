# longarms
Automatically grabbing YouTube uploads (songs) and adding them to an "ingest" Spotify playlist

## Configuration and Setup
Add a file named `spotify.json` in the same directory as the rest of the files and fill the contents as such. Information for setting up authentication can be found [on Spotify's documentation](https://developer.spotify.com/documentation/general/guides/authorization-guide/).
```json
{
  "spotifyClientID": "",
  "spotifyClientSecret": "",
  "spotifyAccessToken": "",
  "spotifyRefreshToken": ""
}
```

Add or modify another file named `youtube.json`,  filling in the info for the YouTube channels you would like the script to watch.

Modify the timestamp in `lastrun` to your liking; the script will try to fetch any uploads since that time. I would advise just setting this to the current time and date. (I apologize this isn't automated; this was more of just an inhouse thing for my personal usage).

## Execution

```bash
python main.py
````
When the program runs, it will check the RSS feeds for each of the YouTube channels listed in `youtube.json`, and check their upload timestamps against the timestamp in `lastrun`. Then, it will search for those songs in Spotify, and then if found add them to your ingest playlist. 

## Future
I plan on making the script do the same things for Spotify playlists - grab new additions and push them to the ingest playlist.
I also would like to support external RSS feeds; for example, ones created from Zapier integrations.
