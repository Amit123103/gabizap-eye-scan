from fastapi import FastAPI, Body
from pydantic import BaseModel
import hashlib
import json
import os
from gabizap_common.logger import setup_logger

logger = setup_logger("ledger-service")
app = FastAPI(title="GABIZAP Blockchain Ledger")

CHAIN_FILE = "ledger.json"

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

# Simple mock blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()
        if not self.chain:
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = {
            "index": 0,
            "timestamp": "GENESIS",
            "data": "Genesis Block",
            "previous_hash": "0",
            "hash": "0" # Simplified
        }
        self.chain.append(genesis_block)
        self.save_chain()

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data, user_id):
        latest = self.get_latest_block()
        new_index = latest["index"] + 1
        previous_hash = latest["hash"]
        
        # Simplify block creation
        block_data = {
            "user_id": user_id,
            "payload": data
        }
        
        block_content = json.dumps(block_data, sort_keys=True)
        block_hash = hashlib.sha256((str(new_index) + previous_hash + block_content).encode()).hexdigest()
        
        new_block = {
            "index": new_index,
            "timestamp": "NOW", # TODO: Real time
            "data": block_data,
            "previous_hash": previous_hash,
            "hash": block_hash
        }
        
        self.chain.append(new_block)
        self.save_chain()
        return block_hash

    def save_chain(self):
        with open(CHAIN_FILE, "w") as f:
            json.dump(self.chain, f, indent=4)

    def load_chain(self):
        if os.path.exists(CHAIN_FILE):
            with open(CHAIN_FILE, "r") as f:
                self.chain = json.load(f)

blockchain = Blockchain()

class AnchorRequest(BaseModel):
    template_hash: str
    user_id: str

@app.post("/anchor")
async def anchor_identity(req: AnchorRequest):
    tx_hash = blockchain.add_block(req.template_hash, req.user_id)
    logger.info(f"Anchored identity {req.user_id} on-chain. Hash: {tx_hash}")
    return {"status": "anchored", "tx_hash": tx_hash, "block_height": len(blockchain.chain)}

@app.get("/chain")
async def get_chain():
    return blockchain.chain

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ledger-service"}
