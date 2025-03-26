FROM python:3.11-slim

# Opusライブラリのインストール
RUN apt-get update && apt-get install -y libopus0 ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# pipをアップグレードしてライブラリをインストール
RUN pip install --upgrade pip && \
    pip install discord.py pynacl requests python-dotenv boto3 yt-dlp

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
