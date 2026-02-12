import time
import json
import bisect
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [CHRONOS] %(message)s')

class TemporalEngine:
    """
    Implements Infinite State Rollback via Event Sourcing.
    Allows queries like: "What was User X's risk score exactly 43 days, 2 hours, 11 seconds ago?"
    """
    
    def __init__(self):
        # In-memory event log (simulating an Append-Only Ledger like Kafka/Amazon QLDB)
        self.event_stream = [] 
        
    def record_event(self, entity_id, event_type, data):
        timestamp = time.time()
        event = {
            "ts": timestamp,
            "entity": entity_id,
            "type": event_type,
            "data": data
        }
        self.event_stream.append(event)
        logging.info(f"Recorded Event: {event_type} for {entity_id}")
        
    def time_travel_query(self, entity_id, target_time_epoch):
        """
        Reconstructs state by replaying all events up to 'target_time_epoch'.
        """
        logging.info(f"⏳ INITIATING TEMPORAL ROLLBACK to T={target_time_epoch}")
        
        # 1. Filter events for this entity
        entity_events = [e for e in self.event_stream if e['entity'] == entity_id]
        
        # 2. Replay Loop
        current_state = {}
        processed_count = 0
        
        for event in entity_events:
            if event['ts'] > target_time_epoch:
                break
                
            # Apply State Transitions
            if event['type'] == "ACCESS_GRANTED":
                current_state['last_access'] = event['ts']
                current_state['status'] = "ACTIVE"
            elif event['type'] == "RISK_SCORE_UPDATE":
                current_state['risk_score'] = event['data']['score']
            elif event['type'] == "ACCOUNT_LOCKED":
                current_state['status'] = "LOCKED"
                
            processed_count += 1
            
        logging.info(f"✅ State Reconstructed. Replayed {processed_count} events.")
        return current_state

if __name__ == "__main__":
    chronos = TemporalEngine()
    
    # Simulate History
    user = "USER_007"
    chronos.record_event(user, "ACCESS_GRANTED", {})
    time.sleep(1)
    t1 = time.time() # Bookmark T1
    chronos.record_event(user, "RISK_SCORE_UPDATE", {"score": 45})
    time.sleep(1)
    chronos.record_event(user, "RISK_SCORE_UPDATE", {"score": 99})
    chronos.record_event(user, "ACCOUNT_LOCKED", {})
    
    # Query Present
    print("Present State:", chronos.time_travel_query(user, time.time()))
    
    # Query Past (T1) -> Should be Active with no risk score yet (or default)
    print("Past State (T1):", chronos.time_travel_query(user, t1))
