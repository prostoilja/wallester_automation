from utils.token_helper import sign_payload

# Mock data for testing
test_data = {"test": "data"}

try:
    signature = sign_payload(test_data)
    print("-" * 30)
    print("✅ Success! Cryptography library is working correctly.")
    print("Private key found at: certs/private.pem")
    print(f"Generated signature: {signature[:50]}...")
    print("-" * 30)
except Exception as e:
    print(f"❌ Error: {e}")
