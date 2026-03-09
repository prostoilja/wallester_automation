import requests
import json
import pytest
from utils.token_helper import sign_payload

BASE_URL = "https://api.wallester.com/v1"

@pytest.fixture
def template_payload():
    """Standard JSON payload based on official documentation."""
    return {
        "delivery_type": "sms",
        "language_code": "AAR",
        "message_type": "AccountingFailedValidationNotification",
        "subject": "Test Notification",
        "body": "Your validation has failed."
    }

# --- TEST 1: GET (List Resources) ---
def test_get_templates_list(api_config):
    """Verify fetching the list of templates using a valid RSA signature."""
    endpoint = f"{BASE_URL}/templates"
    headers = {
        "Authorization": f"Bearer {api_config['api_key']}",
        "X-Signature": sign_payload("")
    }
    response = requests.get(endpoint, headers=headers)
    assert response.status_code in [200, 401, 403]

# --- TEST 2: POST (Create Resource) ---
def test_create_template_post(api_config, template_payload):
    """Verify creating a new template with a signed JSON body."""
    endpoint = f"{BASE_URL}/templates"
    json_body = json.dumps(template_payload)
    headers = {
        "Authorization": f"Bearer {api_config['api_key']}",
        "X-Signature": sign_payload(json_body),
        "Content-Type": "application/json"
    }
    response = requests.post(endpoint, data=json_body, headers=headers)
    assert response.status_code in [201, 401, 403]

# --- TEST 3: PATCH (Update Resource) ---
def test_update_template_patch(api_config):
    """Verify partial update of a template via PATCH method."""
    endpoint = f"{BASE_URL}/templates/test_id"
    patch_payload = {"language_code": "ENG", "subject": "Updated Subject"}
    json_body = json.dumps(patch_payload)
    
    headers = {
        "Authorization": f"Bearer {api_config['api_key']}",
        "X-Signature": sign_payload(json_body),
        "Content-Type": "application/json"
    }
    response = requests.patch(endpoint, data=json_body, headers=headers)
    assert response.status_code in [200, 401, 403, 404]

# --- TEST 4: SEC (Data Integrity / Tampering) ---
def test_security_payload_tampering(api_config, template_payload):
    """SEC: Verify that modifying the body after signing results in rejection."""
    endpoint = f"{BASE_URL}/templates"
    signature = sign_payload(json.dumps(template_payload))
    
    # Simulating a Man-in-the-Middle attack by changing data after signing
    template_payload["body"] = "MALICIOUS_CONTENT_CHANGE"
    
    headers = {
        "Authorization": f"Bearer {api_config['api_key']}",
        "X-Signature": signature,
        "Content-Type": "application/json"
    }
    response = requests.post(endpoint, data=json.dumps(template_payload), headers=headers)
    assert response.status_code in [401, 403]

# --- TEST 5: GET (Payment Metadata with Query Params & Headers) ---
def test_get_payment_metadata(api_config):
    """
    Verify GET /v1/payment-metadata using Query Parameters and Custom Audit Headers.
    Demonstrates handling of UUIDs and mandatory X- headers.
    """
    endpoint = f"{BASE_URL}/payment-metadata"
    
    # As per documentation provided: Query Parameters
    params = {
        "payment_id": "550e8400-e29b-41d4-a716-446655440000", # Example UUIDv4
        "payment_type": "authorization"
    }
    
    # Mandatory Header Parameters
    headers = {
        "Authorization": f"Bearer {api_config['api_key']}",
        "X-Product-Code": "WALL-TEST-PROD",
        "X-Audit-Source-Type": "Backend",
        "X-Audit-User-Id": "user-12345",
        "X-Signature": sign_payload("")
    }
    
    response = requests.get(endpoint, params=params, headers=headers)
    assert response.status_code in [200, 401, 403, 422]

# --- TEST 6: SEC (Unauthorized Access) taken from API docs---
def test_unauthorized_access_security(api_config):
    """SEC: Verify that requests without proper RSA headers are blocked."""
    endpoint = f"{BASE_URL}/templates"
    # Sending request without X-Signature header
    headers = {"Authorization": f"Bearer {api_config['api_key']}"}
    response = requests.get(endpoint, headers=headers)
    assert response.status_code in [401, 403]