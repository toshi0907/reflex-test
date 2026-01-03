#!/bin/bash

docker compose down
git pull || { echo "git pull failed, aborting deployment." >&2; exit 1; }
docker compose up -d --build

# dockerイメージの不要なキャッシュを削除
docker image prune -f