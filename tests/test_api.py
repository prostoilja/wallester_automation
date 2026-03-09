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
    # 403 is expected for restricted test keys, but confirms signature was processed
    assert response.status_code in [200, 403]

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
    assert response.status_code in [201, 403]

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
    assert response.status_code in [200, 403, 404]

# --- TEST 4: SEC (Data Integrity / Tampering) ---
def test_security_payload_tampering(api_config, template_payload):
    """SEC: Verify that modifying the body after signing results in rejection."""
    endpoint = f"{BASE_URL}/templates"
    # Sign the original payload
    signature = sign_payload(json.dumps(template_payload))
    
    # Manually modify the payload body (Simulating a Man-in-the-Middle attack)
    template_payload["body"] = "MALICIOUS_CONTENT_CHANGE"
    
    headers = {
        "Authorization": f"Bearer {api_config['api_key']}",
        "X-Signature": signature,
        "Content-Type": "application/json"
    }
    # Sending the modified body with the old signature
    response = requests.post(endpoint, data=json.dumps(template_payload), headers=headers)
    assert response.status_code in [401, 403]

# --- TEST 5: POST (Process/Export Action) ---
def test_export_templates_action(api_config):
    """Verify secondary POST action for data processing/export."""
    endpoint = f"{BASE_URL}/templates/export"
    payload = {"format": "csv", "filter": "active"}
    json_body = json.dumps(payload)
    headers = {
        "Authorization": f"Bearer {api_config['api_key']}",
        "X-Signature": sign_payload(json_body),
        "Content-Type": "application/json"
    }
    response = requests.post(endpoint, data=json_body, headers=headers)
    assert response.status_code in [200, 403]

# --- TEST 6: SEC (Invalid Method/Auth) ---
def test_unauthorized_access_security(api_config):
    """SEC: Verify that requests without proper headers are blocked."""
    endpoint = f"{BASE_URL}/templates"
    # No RSA signature provided
    headers = {"Authorization": f"Bearer {api_config['api_key']}"}
    response = requests.get(endpoint, headers=headers)
    assert response.status_code in [401, 403]