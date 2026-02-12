import numpy as np
import time
import random
import logging
from eeg_processor import auth_by_thought

# Synthetic Data Generator
def generate_eeg_epoch(is_target: bool, is_stressed: bool = False):
    """
    Generates 1 second of EEG data (250 samples).
    Adds a P300 peak if is_target=True.
    Adds high-freq noise if is_stressed=True.
    """
    t = np.linspace(0, 1, 250)
    
    # Base Alpha Rhythm (8-12Hz) - Resting state
    signal = 5.0 * np.sin(2 * np.pi * 10 * t)
    
    # Noise
    signal += np.random.normal(0, 2.0, 250)
    
    if is_target:
        # P300 Injection: Gaussian bump at 300ms
        p300 = 20.0 * np.exp(-((t - 0.3)**2) / (2 * 0.05**2))
        signal += p300
        
    if is_stressed:
        # High Beta/Gamma injection (Stress)
        stress_wave = 15.0 * np.sin(2 * np.pi * 35 * t)
        signal += stress_wave
        
    return signal

if __name__ == "__main__":
    logging.info("Initiating Neural Link Simulation...")
    
    scenarios = [
        ("Valid User (Calm)", True, False),
        ("Intruder (No P300)", False, False),
        ("Valid User (Under Duress)", True, True)
    ]
    
    for name, is_target, is_duress in scenarios:
        print(f"\n--- SCENARIO: {name} ---")
        time.sleep(1)
        
        # 1. Present Stimulus (Simulated)
        print("Visual Stimulus Presented: [SECRET_image.png]")
        
        # 2. Capture EEG
        raw_data = generate_eeg_epoch(is_target, is_duress)
        
        # 3. Process
        result = auth_by_thought(raw_data)
        print(f"RESULT: {result}")
