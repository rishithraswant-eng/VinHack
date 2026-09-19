Write-Host "Starting PHANTASM Demo Stack..."
docker compose up -d postgres neo4j redis minio

Write-Host "Waiting for services to be healthy..."
Start-Sleep -Seconds 10

Set-Location backend
Write-Host "Running database migrations..."
alembic upgrade head

Write-Host "Starting Backend server..."
Start-Process "uvicorn" -ArgumentList "app.main:app --host 0.0.0.0 --port 8000 --reload"

Set-Location ../frontend
Write-Host "Starting Frontend server..."
Start-Process "npm" -ArgumentList "run dev"

Write-Host "========================================="
Write-Host "PHANTASM Demo Environment Ready!"
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend API: http://localhost:8000"
Write-Host "========================================="
