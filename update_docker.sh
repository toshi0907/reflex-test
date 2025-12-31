#!/bin/bash

docker compose down
git pull origin main || { echo "git pull failed, aborting deployment." >&2; exit 1; }
docker compose up -d --build