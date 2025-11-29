FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg for audio processing
RUN apt-get update && apt-get install -y ffmpeg

COPY . .

# Set up a non-root user
RUN useradd -m myuser
USER myuser

ENTRYPOINT ["/app/entrypoint.sh"]
