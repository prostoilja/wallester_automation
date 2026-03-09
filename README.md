# Wallester Automation Project

Hybrid API and UI testing framework for Wallester API.

## Features
- **API Testing:** RSA-SHA256 request signing.
- **Dockerized:** Stable environment using Playwright Python image.
- **Reporting:** Pytest-html reports generated after each run.

## How to Run

### Option 1: Using Docker (Recommended)
This is the easiest way to run tests in a clean environment:
```bash
docker build -t wallester-tests .
docker run --rm wallester-tests
```

### Option 2: Local Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```
2. Execute the shell script:
   ```bash
   chmod +x run_tests.sh
   ./run_tests.sh
   ```

## Project Structure
- `tests/`: API and UI test cases.
- `utils/`: RSA signing and token helpers.
- `certs/`: RSA keys (excluded from Git for security).
- `Dockerfile`: Container configuration.
