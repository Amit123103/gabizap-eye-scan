import requests
import numpy as np
import cv2
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("red-team")

TARGET_URL = "http://localhost:8000"
LIVENESS_URL = "http://localhost:8009/check" # Testing direct service or via gateway

def generate_noise_image():
    # White noise attack
    img = np.random.randint(0, 255, (240, 320, 3), dtype=np.uint8)
    _, buf = cv2.imencode(".jpg", img)
    return buf.tobytes()

def generate_blur_attack():
    # Simulate a blurry photo (recapture attack)
    img = np.zeros((240, 320, 3), dtype=np.uint8)
    cv2.putText(img, "FAKE FACE", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
    img = cv2.blur(img, (20, 20)) # Heavy blur
    _, buf = cv2.imencode(".jpg", img)
    return buf.tobytes()

def run_attack_vector(attack_name, generator_func):
    logger.info(f"Launching Attack Vector: {attack_name}")
    img_data = generator_func()
    
    try:
        # 1. Attack Liveness
        resp = requests.post(LIVENESS_URL, files={'file': ('attack.jpg', img_data, 'image/jpeg')})
        if resp.status_code == 200:
            result = resp.json()
            if result['is_live']:
                logger.critical(f"[VULNERABILITY] {attack_name} BYPASSED Liveness Check!")
            else:
                logger.info(f"[DEFENDED] {attack_name} caught by Liveness Engine. Conf: {result['confidence']:.2f}")
        else:
            logger.error(f"Attack failed (Network/500): {resp.text}")
            
    except Exception as e:
        logger.error(f"Attack execution error: {e}")

if __name__ == "__main__":
    logger.info("Initializing Red Team Adversarial Suite...")
    time.sleep(1)
    
    run_attack_vector("White Noise Injection", generate_noise_image)
    run_attack_vector("Blurred Recapture (Screen Spoof)", generate_blur_attack)
    
    logger.info("Red Team Simulation Complete.")
