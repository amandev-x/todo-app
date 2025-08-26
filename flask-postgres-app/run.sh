#!/bin/bash

echo "Building a todo app using flask+postgresql stack...💻🐘⚛️"

sleep 2

docker image build -t todo:v.1 .

sleep 1

echo "Image build successfull...🚀✅🐳"

sleep 2

echo "Creating docker network to connect flask and postgres database...🌐🚀💻"

docker network create flask-app

sleep 1

echo "Network build successfully...🌐✅🎯"

sleep 1

echo "Building flask and postgresql containers...📦🚀⚡"

sleep 1

cd ..

docker run -d --name postgre-db -e POSTGRES_PASSWORD=dockerpass -v ./postgres-db:/docker-entrypoint.initdb.d --network flask-app postgres:alpine

echo "Successfully build postgres container...🛢🚀📦"

sleep 1

docker run -d --name flask-todo -p 5000:5000 -e DB_HOST=postgre-db -e DB_PASSWORD=dockerpass --network flask-app todo:v.1

echo "Flask container build successfully...📦✅🎯"

echo "Running the application on port 5000"
