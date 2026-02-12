# Quick Start Guide - Working Version

## The Problem

The full docker-compose.yml tries to build services that don't have complete implementation files yet. 

## Solution: Use the Simplified Version

### Step 1: Start Infrastructure Only

```powershell
cd D:\Projects\Scan
docker-compose -f docker-compose.simple.yml up -d
```

This will start:
- ✅ PostgreSQL (database)
- ✅ Redis (cache)
- ✅ Prometheus (monitoring)
- ✅ Grafana (dashboards)

### Step 2: Verify It's Running

```powershell
docker ps
```

You should see 4 containers running.

### Step 3: Access the Services

- **Grafana Dashboard**: http://localhost:3000
  - Username: `admin`
  - Password: `admin`

- **Prometheus**: http://localhost:9090

- **PostgreSQL**: 
  ```powershell
  docker exec -it gabizap-postgres psql -U postgres -d gabizap
  ```

- **Redis**:
  ```powershell
  docker exec -it gabizap-redis redis-cli
  ```

### Step 4: Run the Frontend (Optional)

```powershell
cd frontend
npm install
npm run dev
```

Open: http://localhost:5173

---

## What's Next?

Once the infrastructure is running, you can:

1. **Manually run backend services** (one at a time)
2. **Build out the missing service files**
3. **Test individual components**

---

## Stop Everything

```powershell
docker-compose -f docker-compose.simple.yml down
```

---

## Why This Works

This simplified version only uses **pre-built Docker images** from Docker Hub, not custom services that need to be built from source code.

The full system requires all service files to be complete, which would take significant development time.
