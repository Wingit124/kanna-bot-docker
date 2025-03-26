#!/bin/bash

# ライブラリアップデートをバックグラウンドで開始（1時間ごと）
while true; do
  sleep 3600
  echo "Updating dependencies..."
  pip install --upgrade yt-dlp --root-user-action=ignore
  echo "Waiting 1 hour before next update..."
done &

# メインBotを起動（こっちはフォアグラウンド）
python main.py
