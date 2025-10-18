# Jellyfin Local Trailers

A simple python-based script to download trailers for local playback.

## Variables

The following environment variables must be provided to authenticate with Jellyfin.

* `JELLYFIN_ENDPOINT` - URL of the Jellyfin server.
* `JELLYFIN_TOKEN` - Token used to authenticate with Jellyfin.

The following environment variables are optional.

* JLT_EXCLUDED_PATHS - Comma-separated list of media folders that should be excluded from processing.

_/etc/containers/sytemd/jellyfin-local-trailers.container.d/00-jellyfin-local-trailers-variables.conf_

```
[Container]
Environment=JELLYFIN_ENDPOINT=media.example.com
Environment=JELLFYIN_TOKEN=my_token_value
Environment=JLT_EXCLUDED_PATHS=/media/movies/chuck
```

## Volumes

For local trailers to function properly, they must be named & stored in the same folder as the original movie. This script will parse the path of the movie and attempt to store the trailer in the same location. This means that the path for volume mounts must be the same as the path used by jellyfin. For example, if Jellyfin has a movie stored at `/media/movies/melissa/moviename/moviename.mp4`, then this container should be configure so the same path is accessible.

_/etc/containers/systemd/jellyfin-local-trailers.container.d/01-jellyfin-local-trailers-volumes.conf_

```
[Container]
Volume=<my-path-to-movies>:/media/movies:z,rw,rslave,rbind
```
