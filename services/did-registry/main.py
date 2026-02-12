from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
import hashlib
import json
import datetime

app = FastAPI(title="GABIZAP DID Registry")

# In-memory registry for simulation (would be Blockchain/IPFS in prod)
DID_REGISTRY = {}

class DIDDocument(BaseModel):
    id: str
    context: List[str] = ["https://www.w3.org/ns/did/v1"]
    verificationMethod: List[dict]
    authentication: List[str]
    service: Optional[List[dict]] = None

@app.post("/did/create")
async def create_did(public_key_pem: str = Body(..., embed=True)):
    """
    Registers a new decentralized identity from a public key.
    Generates: did:gabizap:<hash_of_key>
    """
    # 1. Generate unique identifier based on key hash (IPFS style multihash)
    key_hash = hashlib.sha256(public_key_pem.encode()).hexdigest()[:32]
    did = f"did:gabizap:{key_hash}"
    
    # 2. Construct DID Document
    doc = DIDDocument(
        id=did,
        verificationMethod=[{
            "id": f"{did}#key-1",
            "type": "JsonWebKey2020",
            "controller": did,
            "publicKeyPem": public_key_pem
        }],
        authentication=[f"{did}#key-1"]
    )
    
    DID_REGISTRY[did] = doc
    
    return {"did": did, "document": doc}

@app.get("/did/{did_id}")
async def resolve_did(did_id: str):
    """
    DID Resolver. Returns the DID Document associated with the ID.
    """
    if did_id not in DID_REGISTRY:
        raise HTTPException(status_code=404, detail="DID not found")
    
    return DID_REGISTRY[did_id]

@app.post("/vc/issue")
async def issue_credential(did_subject: str = Body(...), claims: dict = Body(...)):
    """
    Issues a W3C Verifiable Credential (VC) signed by the GABIZAP Authority.
    """
    # In a real ZK system, this would sign a hash of the claim
    vc = {
        "context": ["https://www.w3.org/2018/credentials/v1"],
        "type": ["VerifiableCredential", "IdentityCard"],
        "issuer": "did:gabizap:authority",
        "issuanceDate": datetime.datetime.utcnow().isoformat(),
        "credentialSubject": {
            "id": did_subject,
            **claims # e.g., {"clearance": "top-secret", "age_over_21": true}
        },
        "proof": {
            "type": "EcdsaSecp256k1Signature2019",
            "created": datetime.datetime.utcnow().isoformat(),
            "proofPurpose": "assertionMethod",
            "verificationMethod": "did:gabizap:authority#key-1",
            "jws": "eyJhbGciOiJ...signed_by_authority..." 
        }
    }
    return vc
