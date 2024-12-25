build:
  podman build -t jellyfin-local-trailers:latest .

lint:
  python -m pylint .
