# utils/token_helper.py
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

def sign_payload(payload_dict, private_key_path="certs/private.pem"):
    """
    Creates a digital signature for the JSON request body using RSA RS256.
    """
    # 1. Convert dictionary to a compact JSON string (no extra spaces, sorted keys)
    # This ensures the signature is consistent for the same data
    payload_string = json.dumps(payload_dict, separators=(',', ':'), sort_keys=True)
    
    # 2. Load the private RSA key from the specified path
    with open(private_key_path, 'r') as f:
        key = RSA.importKey(f.read())
    
    # 3. Create a SHA-256 hash of the payload string
    h = SHA256.new(payload_string.encode('utf-8'))
    
    # 4. Sign the hash using the private key (PKCS#1 v1.5)
    signature = pkcs1_15.new(key).sign(h)
    
    # 5. Encode the binary signature to Base64 string for HTTP headers
    return base64.b64encode(signature).decode('utf-8')