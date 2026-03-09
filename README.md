# Wallester Automation Project

Hybrid API and UI testing framework for Wallester API services.

## Technical Highlights

### 1. API Security (RSA-SHA256)
The framework implements a high-security communication layer:
- **Payload Signing**: Every API request is signed using an RSA private key.
- **Integrity Verification**: Uses SHA-256 hashing to ensure data integrity.
- **Modular Utility**: Signing logic is decoupled into `utils/token_helper.py` for reuse across different test suites.

### 2. UI Automation (Playwright + POM)
- **Page Object Model**: Strict separation between page elements (`pages/`) and test logic (`tests/`).
- **Modern Stack**: Leverages Playwright for fast, reliable, and headless browser testing.
- **Navigation Flow**: Automated scenarios covering navigation from the home page to the API documentation.

### 3. Infrastructure & Portability
- **Dockerized Environment**: A custom Dockerfile based on `mcr.microsoft.com/playwright/python` ensures the environment is identical across all machines.
- **Dependency Management**: Precise version locking in `requirements.txt` to prevent regression.

## How to Run

### Docker (Preferred)
```bash
docker build -t wallester-tests .
docker run --rm wallester-tests
```

### Local Execution
```bash
pip install -r requirements.txt
playwright install chromium
./run_tests.sh
```

---
*Note: Private keys (.pem) are excluded from the repository for security reasons.*
