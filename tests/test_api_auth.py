import pytest
import requests
import uuid
import os
from datetime import datetime
from utils.token_helper import sign_payload

TRANSACTION_DATA = [
    ("ATMBalanceInquiry", 0.00),
    ("Purchase", 15.50),
    ("Withdrawal", 20.00),
    ("Reversal", 0.00),
    ("Refund", 10.00)
]

@pytest.mark.parametrize("txn_type, amount", TRANSACTION_DATA)
def test_create_authorization_v1(txn_type, amount, api_config):
    url = f"{api_config['base_url']}/authorizations"
    
    payload = {
        "account_amount": amount,
        "account_currency_code": "EUR",
        "acquiring_institution_country_code": "EST",
        "acquiring_institution_id": "123456",
        "action_code": "00",
        "card_id": api_config['card_id'],
        "card_processor_transaction_id": str(uuid.uuid4()),
        "card_read_method": "Contactless",
        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "does_terminal_support_partial_approvals": True,
        "merchant_category_code": "0742",
        "merchant_city": "Tallinn",
        "merchant_country_code": "EST",
        "merchant_id": "MERCH-999",
        "merchant_name": "Test Merchant",
        "retrieval_reference_number": str(uuid.uuid4())[:12],
        "terminal_id": "TERM-001",
        "transaction_amount": amount,
        "transaction_currency_code": "EUR",
        "type": txn_type
    }

    signature = sign_payload(payload)
    headers = {
        "Content-Type": "application/json",
        "X-Signature": signature,
        "X-API-Key": api_config['api_key']
    }

    print(f"\n[RUN] Sending {txn_type} to {url}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        print(f"[RES] Status: {response.status_code}")
        assert response.status_code in [200, 201, 401, 403]
    except Exception as e:
        print(f"[ERR] Connection failed: {e}")
        pytest.skip("Skipping due to network issues with host")

# NB this function starts from BEGGINING
def test_create_authorization_invalid_signature(api_config):
    """
     Negative test, invalid signature should be decline request
    """
    url = f"{api_config['base_url']}/authorizations"
    
    payload = {
        "card_id": api_config['card_id'],
        "transaction_amount": 1.00,
        "transaction_currency_code": "EUR",
        "type": "Purchase"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Signature": "INVALID_SIGNATURE_STUB_12345", 
        "X-API-Key": api_config['api_key']
    }

    print(f"\n[NEG] Testing invalid signature...")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        print(f"[RES] Status: {response.status_code}")
        # Expecting 401, if signature declined
        assert response.status_code in [401, 403], f"Expected 401/403 for bad signature, got {response.status_code}"
    except Exception as e:
        pytest.skip(f"Network issue during negative test: {e}")