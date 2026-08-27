import hmac
import hashlib
import json
import base64
import time
from backend.config.settings import settings

SECRET_KEY = settings.SECRET_KEY.encode('utf-8')

def create_access_token(data: dict, expires_delta: int = 3600) -> str:
    """
    Generates a secure signed token (hmac-sha256) for session management.
    Avoids external JWT library dependency issues on local runs.
    """
    payload = {
        **data,
        "exp": int(time.time()) + expires_delta
    }
    # Base64 encode payload
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
    
    # Sign payload
    signature = hmac.new(SECRET_KEY, payload_b64.encode('utf-8'), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode('utf-8')
    
    return f"{payload_b64}.{signature_b64}"

def verify_access_token(token: str) -> dict | None:
    """
    Verifies a secure signed token and returns the payload if valid.
    """
    try:
        if "." not in token:
            return None
        payload_b64, signature_b64 = token.split(".", 1)
        
        # Verify signature
        expected_sig = hmac.new(SECRET_KEY, payload_b64.encode('utf-8'), hashlib.sha256).digest()
        expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode('utf-8')
        
        if not hmac.compare_digest(expected_sig_b64, signature_b64):
            return None
            
        # Parse payload
        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode('utf-8')).decode('utf-8'))
        
        # Check expiry
        if payload.get("exp", 0) < int(time.time()):
            return None
            
        return payload
    except Exception:
        return None
