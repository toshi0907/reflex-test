#!/bin/bash

FRONT_END_PORT=3000
BACK_END_PORT=8000
FRONTEND_HOST=main.test.com
BACKEND_HOST=api.test.com

sed -i -e "s/__FRONT_END_PORT__/${FRONT_END_PORT}/g" docker-compose.yml
sed -i -e "s/__BACK_END_PORT__/${BACK_END_PORT}/g" docker-compose.yml

cp .env.example .env
sed -i -e "s/__FRONTEND_HOST__/${FRONTEND_HOST}/g" .env
sed -i -e "s/__FRONTEND_HOST__/${FRONTEND_HOST}/g" Dockerfile
sed -i -e "s/__BACKEND_HOST__/${BACKEND_HOST}/g" .env
sed -i -e "s/__BACKEND_HOST__/${BACKEND_HOST}/g" Dockerfile
