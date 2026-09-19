#!/bin/bash
echo "Starting PHANTASM Demo Stack..."
docker compose up -d postgres neo4j redis minio

echo "Waiting for services to be healthy..."
sleep 10

cd backend
echo "Running database migrations..."
alembic upgrade head

echo "Starting Backend server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

cd ../frontend
echo "Starting Frontend server..."
npm run dev &
FRONTEND_PID=$!

echo "========================================="
echo "PHANTASM Demo Environment Ready!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "========================================="

wait $BACKEND_PID $FRONTEND_PID
