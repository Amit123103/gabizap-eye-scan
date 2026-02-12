from fastapi import FastAPI, UploadFile, File, HTTPException
import mediapipe as mp
import numpy as np
from PIL import Image
import io
from gabizap_common.logger import setup_logger

logger = setup_logger("hand-engine")
app = FastAPI(title="GABIZAP Hand Engine")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

@app.post("/process")
async def process_hand(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)
        
        results = hands.process(image_np)
        
        if not results.multi_hand_landmarks:
            return {"status": "no_hand_detected"}
            
        # Extract landmarks and flatten to vector
        landmarks = []
        for hand_landmarks in results.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
                
        return {"embedding": landmarks, "version": "v1"}
        
    except Exception as e:
        logger.error(f"Error processing hand: {e}")
        raise HTTPException(status_code=500, detail="Processing failed") 

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "hand-engine"}
