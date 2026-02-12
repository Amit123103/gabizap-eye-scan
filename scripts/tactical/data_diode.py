import time
import os
import shutil
import logging
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s [DATA-DIODE] %(message)s')

HIGH_SIDE_DIR = "./tactical/high_side_out"
LOW_SIDE_DIR = "./tactical/low_side_in"

def ensure_dirs():
    os.makedirs(HIGH_SIDE_DIR, exist_ok=True)
    os.makedirs(LOW_SIDE_DIR, exist_ok=True)

def simulate_diode_transfer():
    """
    Simulates a hardware data diode (e.g., Owl Cyber Defense).
    Strictly One-Way: HIGH -> LOW (for logs) or LOW -> HIGH (for updates).
    Logic: Moves files and verifies checksums.
    """
    logging.info("Initializing Optical Data Diode Link...")
    
    # 1. Create a dummy classified log file
    filename = f"mission_log_{int(time.time())}.enc"
    src_path = os.path.join(HIGH_SIDE_DIR, filename)
    
    with open(src_path, "w") as f:
        f.write("CLASSIFIED_MISSION_DATA_PACKET_V1")
    
    logging.info(f"High-Side: Generated packet {filename}")
    
    # 2. 'Transfer' (Copy)
    # In real hardware, this is via UDP/Optical link
    dest_path = os.path.join(LOW_SIDE_DIR, filename)
    shutil.copy(src_path, dest_path)
    
    # 3. Verify Integrity
    src_hash = hashlib.sha256(open(src_path, 'rb').read()).hexdigest()
    dest_hash = hashlib.sha256(open(dest_path, 'rb').read()).hexdigest()
    
    if src_hash == dest_hash:
        logging.info(f"Diode Transfer Complete. Checksum: {src_hash[:8]}... MATCH")
        logging.info("Low-Side: Received packet successfully.")
        os.remove(src_path) # Cleanup source
    else:
        logging.critical("INTEGRITY CHECKSUM MISMATCH! POSSIBLE TAMPERING.")

if __name__ == "__main__":
    ensure_dirs()
    while True:
        simulate_diode_transfer()
        time.sleep(5)
