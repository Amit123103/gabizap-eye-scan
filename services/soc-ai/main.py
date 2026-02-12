from fastapi import FastAPI, Body
from pydantic import BaseModel
import random
import time

# SERVICE: Sentinelle AI (SOC Analyst)
# ARCHITECTURE: Uses RAG (Retrieval Augmented Generation) over Audit Logs
# MODEL (Simulated): Specialized SecBERT + GPT-4 wrapper

app = FastAPI(title="Sentinelle AI - Autonomous SOC Analyst")

class LogBatch(BaseModel):
    logs: list[str]
    context: str = "production"

@app.post("/analyze/threat")
async def analyze_threat(payload: LogBatch):
    """
    Analyzes a batch of logs using Generative AI to explain the attack textually.
    """
    # Simulate LLM Inference Latency
    time.sleep(1.5) 
    
    # Mock Analysis Generation
    threat_types = ["Brute Force", "SQL Injection", "Impossible Travel", "Device Spoofing"]
    detected = random.choice(threat_types)
    confidence = random.uniform(0.85, 0.99)
    
    analysis = f"""
    **THREAT ANALYSIS REPORT**
    **Detected Pattern:** {detected}
    **Confidence:** {confidence:.2%}
    
    **Executive Summary:**
    The AI model observed a sequence of anomalous events matching the signature of a {detected} attempt. 
    The source IP originated from a high-risk ASN tailored for anonymization.
    
    **Reasoning:**
    1. Velocity of requests exceeded standard human deviation by 400%.
    2. Header fingerprinting suggests a headless browser (Selenium/Puppeteer).
    3. Payload contained obfuscated SQL characters (if SQLi) or abnormal biometrics.
    
    **Recommended Action:**
    - Immediate IP Block (Auto-Executed by Guardian Agent).
    - Invalidate all active sessions for target user.
    - Flag identity for Manual Verification (Level 3).
    """
    
    return {
        "verdict": "MALICIOUS",
        "threat_class": detected,
        "analysis_text": analysis,
        "mitigation_plan_id": f"MIT-{random.randint(1000,9999)}"
    }

@app.post("/chat/ops")
async def chat_ops(query: str = Body(..., embed=True)):
    """
    ChatOps Interface. Allows human operators to ask questions in natural language.
    E.g., "Show me all failed logins from North Korea in the last hour."
    """
    return {
        "query": query,
        "response": f"I found 0 events matching '{query}'. However, I see 15 failed logins from unknown proxies. Would you like me to block the subnet?"
    }
