import random
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s [PRE-CRIME] %(message)s')

class PreCrimeModel:
    """
    Predictive Justice Engine.
    Uses Causal AI to infer 'Intent' from behavioral metadata.
    """
    
    def predict_insider_threat(self, user_profile):
        logging.info(f"Analyzing behavioral vectors for {user_profile['id']}...")
        
        # Factors:
        # 1. Temporal Drift: Are they logging in at weird hours?
        # 2. Data Greed: Are they accessing more records than usual?
        # 3. Biometric Jitter: Is their hand shaking? (Stress)
        
        score = 0
        reasons = []
        
        if user_profile['login_hour_variance'] > 2.5:
            score += 30
            reasons.append("Erratic Temporal Pattern")
            
        if user_profile['data_access_volume'] > user_profile['historical_avg'] * 1.5:
            score += 50
            reasons.append("Data Exfiltration Anomaly")
            
        if user_profile['biometric_stress_marker'] > 0.8:
            score += 15
            reasons.append(" elevated Cortisol/Stress indicators")
            
        probability = min(0.99, score / 100.0)
        
        return probability, reasons

if __name__ == "__main__":
    # Simulation
    suspect = {
        "id": "EMP_9921",
        "login_hour_variance": 3.1, # Suspicious
        "data_access_volume": 500,
        "historical_avg": 200,      # Suspicious
        "biometric_stress_marker": 0.4
    }
    
    model = PreCrimeModel()
    prob, evidence = model.predict_insider_threat(suspect)
    
    if prob > 0.75:
        logging.critical(f"🔮 PRE-CRIME ALERT: Future Breach Probability {prob:.1%}")
        logging.critical(f"Evidence: {evidence}")
        logging.critical("RECOMMENDATION: Pre-emptive Administrative Leave.")
    else:
        logging.info(f"Subject Clearance Valid. Threat Probability {prob:.1%}")
