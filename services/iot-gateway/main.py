import asyncio
import json
import httpx
import logging
from gmqtt import Client as MQTTClient
from gabizap_common.logger import setup_logger

logger = setup_logger("iot-gateway")

MQTT_BROKER = "mosquitto" # Docker service name
AUTH_SERVICE_URL = "http://auth-service:8001"

async def on_message(client, topic, payload, qos, properties):
    # Topic: /gate/{gate_id}/scan
    try:
        data = json.loads(payload.decode())
        gate_id = topic.split('/')[2]
        user_token = data.get('token')
        
        logger.info(f"Received scan from Gate {gate_id}")
        
        # Verify with Auth Service
        async with httpx.AsyncClient() as http:
            resp = await http.post(f"{AUTH_SERVICE_URL}/auth/validate", 
                                 headers={"Authorization": f"Bearer {user_token}"})
            
            if resp.status_code == 200:
                # ACCESS GRANTED
                logger.info(f"Access GRANTED for Gate {gate_id}")
                client.publish(f"/gate/{gate_id}/command", "OPEN", qos=1)
            else:
                # ACCESS DENIED
                logger.warning(f"Access DENIED for Gate {gate_id}")
                client.publish(f"/gate/{gate_id}/command", "REJECT", qos=1)
                
    except Exception as e:
        logger.error(f"Error processing MQTT message: {e}")

async def main():
    client = MQTTClient("iot-gateway-service")
    client.on_message = on_message
    
    await client.connect(MQTT_BROKER, 1883)
    client.subscribe("/gate/+/scan", qos=1)
    
    logger.info("IoT Gateway Active. Listening for Physical Access events...")
    
    # Keep running
    stop = asyncio.Event()
    await stop.wait()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
