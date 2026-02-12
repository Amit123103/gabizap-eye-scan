import time
import json
import random
import logging
# We simulate MQTT client here (using direct print or mock if paho isn't installed, 
# but let's assume paho-mqtt for the script)
# For the sake of the environment where paho might not be present, we'll mock the interaction loop
# or imply it needs 'pip install paho-mqtt'

logging.basicConfig(level=logging.INFO, format='%(asctime)s [TURNSTILE-01] %(message)s')

def simulate_physical_access():
    gate_id = "GATE_MAIN_LOBBY"
    
    logging.info("Initializing Physical Access Controller (PAC)...")
    logging.info("Connected to Broker: tcp://localhost:1883")
    
    while True:
        # Simulate User Approach
        input("Press Enter to simulate Badge Tap / Iris Scan > ")
        
        logging.info("Reading Biometric Token...")
        user_token = f"jwt_mock_{random.randint(1000,9999)}"
        payload = json.dumps({"token": user_token, "biometric_type": "IRIS"})
        
        logging.info(f"📤 PUBLISH topic=/gate/{gate_id}/scan payload={payload}")
        
        # Simulate Network Latency
        time.sleep(0.2)
        
        # Simulate Response
        if random.random() > 0.2:
            logging.info(f"📥 RECEIVED topic=/gate/{gate_id}/command payload=OPEN")
            logging.info("🟢 ACTUATING SOLENOID. GATE OPEN.")
        else:
            logging.info(f"📥 RECEIVED topic=/gate/{gate_id}/command payload=REJECT")
            logging.info("🔴 ACCESS DENIED. ALARM TRIGGERED.")

if __name__ == "__main__":
    simulate_physical_access()
