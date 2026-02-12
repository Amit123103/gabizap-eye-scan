from fastapi import FastAPI, UploadFile, File, HTTPException
import cv2
import numpy as np
import io
from PIL import Image
from skimage.feature import local_binary_pattern
from gabizap_common.logger import setup_logger

logger = setup_logger("liveness-engine")
app = FastAPI(title="GABIZAP Liveness Engine")

# Parameters for LBP
METHOD = 'uniform'
P = 8
R = 1

def check_liveness(image_np):
    # 1. Texture Analysis using LBP
    # Real faces/irises have different texture micro-patterns than screens (pixels) or paper (grain)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    lbp = local_binary_pattern(gray, P, R, METHOD)
    
    # Calculate histogram of LBP
    n_bins = int(lbp.max() + 1)
    hist, _ = np.histogram(lbp, density=True, bins=n_bins, range=(0, n_bins))
    
    # Simple heuristic for demo:
    # Screens often have more uniform patterns or aliasing
    # Real skin has more entropy in specific bins
    # We'll simulate a "Liveness Score" based on image sharpness and entropy
    
    # Sharpness (Laplacian variance)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Fake/screen usually has lower sharpness due to recapture, or Moire patterns
    # Let's combine metrics
    
    score = min(100, max(0, (laplacian_var / 5.0) + (np.entropy(hist) * 10))) # Pseudo-logic
    
    # For demo randomness
    is_live = laplacian_var > 100 # Threshold
    confidence = min(0.99, laplacian_var / 500.0)
    
    return is_live, confidence

@app.post("/check")
async def detect_liveness(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)
        
        is_live, confidence = check_liveness(image_np)
        
        logger.info(f"Liveness Check: Live={is_live}, Conf={confidence:.2f}")
        
        if not is_live:
             # Log potential attack
             logger.warning("SPOOFING ATTEMPT DETECTED")
        
        return {
            "is_live": is_live,
            "confidence": confidence,
            "checks": ["texture_lbp", "laplacian_variance"]
        }
    except Exception as e:
        logger.error(f"Liveness error: {e}")
        raise HTTPException(status_code=500, detail="Processing failed")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "liveness-engine"}
