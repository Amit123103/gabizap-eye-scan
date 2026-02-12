import numpy as np
import logging
from scipy.signal import butter, lfilter

logging.basicConfig(level=logging.INFO, format='%(asctime)s [NEURO-CORE] %(message)s')
logger = logging.getLogger("BCI-Adapter")

class EEGProcessor:
    """
    Processes raw electroencephalography (EEG) signals.
    Focus: Detecting P300 Event-Related Potentials (ERPs).
    """
    
    SAMPLE_RATE = 250 # Hz
    
    @staticmethod
    def bandpass_filter(data, lowcut=0.5, highcut=30.0, fs=250, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y

    @staticmethod
    def detect_p300_response(signal_epoch: np.array) -> float:
        """
        Analyzes a 1-second epoch of EEG data for P300 signature.
        P300 is a positive deflection ~300ms after a stimulus.
        """
        # 1. Filter Signal
        filtered = EEGProcessor.bandpass_filter(signal_epoch)
        
        # 2. Extract window (250ms - 500ms)
        # 250Hz sample rate -> indices 62 to 125
        window = filtered[62:125]
        
        # 3. Peak Detection (Simple Amplitude Check)
        peak_amplitude = np.max(window)
        
        # 4. Stress/Duress Detection (High Beta waves > 20Hz often imply stress)
        beta_power = np.sum(filtered**2) / len(filtered)
        
        logger.info(f"Signal Analysis: Peak={peak_amplitude:.2f}uV, BetaPower={beta_power:.2f}")
        
        return peak_amplitude, beta_power

def auth_by_thought(raw_eeg_stream):
    """
    Simulates authenticating a user based on their unique P300 response to a secret image.
    """
    logger.info("Processing Neural Stream...")
    
    # Simulate processing chunks
    peak, stress = EEGProcessor.detect_p300_response(raw_eeg_stream)
    
    if stress > 50.0:
        logger.critical("⚠️ DURESS DETECTED: User is under extreme stress/coercion.")
        return "DURESS_LOCKDOWN"
        
    if peak > 15.0: # Threshold in microvolts
        logger.info("✅ P300 Confirmed: User recognized the secret stimulus.")
        return "ACCESS_GRANTED"
    else:
        logger.warning("❌ No P300 Response: User did not recognize stimulus.")
        return "ACCESS_DENIED"
