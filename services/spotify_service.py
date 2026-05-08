import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

print(f"DEBUG ENV: ID starts with {client_id[:5] if client_id else 'NONE'}")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_artist_stats(artist_name):
    try:
        results = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
        items = results.get('artists', {}).get('items', [])
        
        if items:
            artist = items[0]
            similarity = SequenceMatcher(None, artist_name.lower(), artist['name'].lower()).ratio()

            if similarity < 0.7:
                print(f"DEBUG: Відхилено через невідповідність: {artist_name} != {artist['name']}")
                return None
                
            return {
                "name": artist['name'],
                "url": artist.get('external_urls', {}).get('spotify', ""),
                "genres": artist.get('genres', [])
            }
        return None
    except Exception as e:
        return None