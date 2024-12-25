FROM python:3.13

WORKDIR /usr/src/app

ENV JELLYFIN_ENDPOINT
ENV JELLYFIN_TOKEN
ENV JLT_EXCLUDED_PATHS=""

# Install required packages
RUN apt-get update && \
  apt-get install -y ffmpeg && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Install required python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY missing_trailers.py ./

CMD ["python", "./missing_trailers.py"]
