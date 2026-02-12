from locust import HttpUser, task, between
import random
import json

class GabizapUser(HttpUser):
    wait_time = between(1, 5)
    token = None

    def on_start(self):
        """User login to fetch JWT"""
        # Register if needed or just login
        # For simplicity, we assume pre-seeded user or simple login
        self.login()

    def login(self):
        # We might create a random user on the fly or use a pool
        email = f"user_{random.randint(1, 10000)}@example.com"
        password = "secure_password"
        
        # In a real test, we would hit the register endpoint first if user persists
        # Here we mock a successful token response structure if backend is mocked
        # But let's try to hit the real auth endpoint
        with self.client.post("/auth/token", json={"email": email, "password": password}, catch_response=True) as response:
            if response.status_code == 200:
                self.token = response.json().get("access_token")
            else:
                # Fallback for swarm testing if DB isn't seeded with 10k users
                pass

    @task(3)
    def scan_iris(self):
        """Simulate high-throughput biometric scanning"""
        if not self.token: return
        
        # Generate dummy image bytes (10KB)
        dummy_image = b'\x00' * 10240 
        files = {'file': ('iris.jpg', dummy_image, 'image/jpeg')}
        headers = {'Authorization': f'Bearer {self.token}'}
        
        self.client.post("/iris/embed", files=files, headers=headers)

    @task(1)
    def view_dashboard(self):
        """Simulate admin viewing analytics"""
        if not self.token: return
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/audit/logs", headers=headers)

    @task(5)
    def heartbeat(self):
        """Simulate continuous session validation (Zero Trust)"""
        if not self.token: return
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/auth/validate", headers=headers)
