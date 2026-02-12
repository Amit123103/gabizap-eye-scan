# GABIZAP Local Deployment Script

Write-Host "Starting GABIZAP Global Identity Platform..." -ForegroundColor Cyan

# Check for Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker is not installed or not in PATH."
    exit 1
}

# Build and Run
Write-Host "Building and starting services..." -ForegroundColor Yellow
docker-compose up --build -d

# Status
Write-Host "Services started!" -ForegroundColor Green
Write-Host "API Gateway: http://localhost:8000"
Write-Host "Frontend:    http://localhost:3000"
Write-Host "Auth Service: http://localhost:8001"
Write-Host "Iris Engine:  http://localhost:8003"

Write-Host "Logs are streaming... (Press Ctrl+C to stop)" -ForegroundColor Gray
docker-compose logs -f
