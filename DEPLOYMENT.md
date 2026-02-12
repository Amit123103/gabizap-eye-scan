# GABIZAP Deployment Guide

## Quick Start - Run the Platform Locally

This guide will help you get the GABIZAP platform running on your Windows machine.

---

## Prerequisites

### Required Software
1. **Docker Desktop** (with WSL2 backend)
   - Download: https://www.docker.com/products/docker-desktop
   - Ensure it's running before proceeding

2. **Node.js** (v18 or higher)
   - Download: https://nodejs.org/
   - Verify: `node --version`

3. **Python** (3.10+)
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

4. **Git** (for version control)
   - Download: https://git-scm.com/
   - Verify: `git --version`

---

## Step 1: Install Dependencies

### Backend Services
```powershell
# Navigate to project root
cd d:\Projects\Scan

# Install Python dependencies for each service
cd services/auth-service
pip install -r requirements.txt

cd ../api-gateway
pip install -r requirements.txt

# Repeat for other services as needed
```

### Frontend
```powershell
cd d:\Projects\Scan\frontend
npm install
```

---

## Step 2: Start Core Infrastructure

### Option A: Full Stack (Docker Compose)
```powershell
cd d:\Projects\Scan

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Option B: Minimal Setup (Manual)
```powershell
# Start PostgreSQL
docker run -d --name gabizap-postgres \
  -e POSTGRES_PASSWORD=secure_password \
  -e POSTGRES_DB=gabizap \
  -p 5432:5432 \
  postgres:15

# Start Redis
docker run -d --name gabizap-redis \
  -p 6379:6379 \
  redis:7-alpine

# Verify they're running
docker ps
```

---

## Step 3: Start Backend Services

### Auth Service
```powershell
cd d:\Projects\Scan\services\auth-service
uvicorn main:app --reload --port 8001
```

### API Gateway
```powershell
# In a new terminal
cd d:\Projects\Scan\services\api-gateway
uvicorn main:app --reload --port 8000
```

### Other Services (Optional)
Start additional services in separate terminals:
```powershell
# Iris Engine
cd services/iris-engine
uvicorn main:app --port 8003

# Risk Engine
cd services/risk-engine
uvicorn main:app --port 8004
```

---

## Step 4: Start Frontend

```powershell
cd d:\Projects\Scan\frontend
npm run dev
```

The UI will be available at: **http://localhost:5173**

---

## Step 5: Verify Installation

### Check Service Health
```powershell
# API Gateway
curl http://localhost:8000/health

# Auth Service
curl http://localhost:8001/health

# Database connection
docker exec -it gabizap-postgres psql -U postgres -d gabizap -c "SELECT 1;"
```

### Access the Dashboard
1. Open browser: http://localhost:5173
2. You should see the GABIZAP login page
3. Default credentials (if implemented):
   - Username: `admin@gabizap.io`
   - Password: `Admin123!`

---

## Common Issues & Solutions

### Issue: Docker not starting
**Solution**: 
- Ensure Docker Desktop is running
- Check WSL2 is enabled: `wsl --status`
- Restart Docker Desktop

### Issue: Port already in use
**Solution**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID <process_id> /F
```

### Issue: Module not found
**Solution**:
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Database connection failed
**Solution**:
```powershell
# Check PostgreSQL is running
docker ps | findstr postgres

# Restart if needed
docker restart gabizap-postgres
```

---

## Simplified Demo Mode

If you just want to see the UI without backend:

```powershell
cd d:\Projects\Scan\frontend
npm run dev
```

The frontend will run in **demo mode** with mock data.

---

## Stopping the Platform

### Docker Compose
```powershell
docker-compose down
```

### Manual Services
```powershell
# Stop containers
docker stop gabizap-postgres gabizap-redis

# Remove containers (optional)
docker rm gabizap-postgres gabizap-redis
```

Press `Ctrl+C` in each terminal running backend services.

---

## Next Steps

Once running:
1. **Explore the Dashboard** - Navigate through the UI
2. **Test Authentication** - Try logging in
3. **View Logs** - Check `docker-compose logs` for activity
4. **Read API Docs** - Visit http://localhost:8000/docs (FastAPI auto-docs)

---

## Production Deployment

For production deployment, see:
- `infrastructure/k8s/` - Kubernetes manifests
- `infrastructure/terraform/` - Multi-region AWS setup
- `COMPLIANCE.md` - Security hardening checklist

---

## Support

If you encounter issues:
1. Check logs: `docker-compose logs -f [service-name]`
2. Verify all prerequisites are installed
3. Ensure ports 5173, 8000-8010, 5432, 6379 are available

**Status**: Ready to deploy 🚀
