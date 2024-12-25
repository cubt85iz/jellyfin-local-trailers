"""
Identifies and downloads missing local trailers.
"""
import os
import yt_dlp

from jellyfin_api_client import AuthenticatedClient
from jellyfin_api_client.api.items import get_items
from jellyfin_api_client.models import ItemFields, BaseItemKind

JELLYFIN_ENDPOINT = os.environ("JELLYFIN_ENDPOINT")
JELLYFIN_TOKEN = os.environ("JELLYFIN_TOKEN")
JLT_EXCLUDED_PATHS = os.environ("JLT_EXCLUDED_PATHS").split(",")

# Create client for Jellyfin
jellyfin_client = AuthenticatedClient(
  base_url=JELLYFIN_ENDPOINT,
  token=f'Token={JELLYFIN_TOKEN}',
  prefix="MediaBrowser",
)

# Identify the Jellyfin movies that have trailers.
jellyfin_movies_with_trailers = get_items.sync(
  client=jellyfin_client,
  include_item_types=[BaseItemKind.MOVIE],
  fields=[ItemFields.LOCALTRAILERCOUNT, ItemFields.PATH, ItemFields.REMOTETRAILERS],
  has_trailer=True,
  recursive=True
).items

# Identify the Jellyfin movies that aren't excluded that are missing local trailers.
jellyfin_movies_without_local_trailers=[]
for movie in jellyfin_movies_with_trailers:
    EXCLUDED = False
    for folder in JLT_EXCLUDED_PATHS:
        if movie.path.startswith(folder):
            EXCLUDED = True
            break

    if movie.local_trailer_count == 0 and not EXCLUDED:
        jellyfin_movies_without_local_trailers.append(movie)

# Download missing local trailers.
for movie in jellyfin_movies_without_local_trailers:
    # Mounts must mirror those in Jellyfin for this to work.
    local_trailer_path=os.path.dirname(movie.path) + "/" + \
      os.path.splitext(os.path.basename(movie.path))[0] + "-trailer.mp4"
    trailer_url=movie.remote_trailers[0].url

    try:
        ydl_opts = {
          "quiet": True,
          "outtmpl": f"{local_trailer_path}",
          "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([trailer_url])
    except:
        print(f"Failed to download trailer for {movie.name} ({movie.production_year}).")
