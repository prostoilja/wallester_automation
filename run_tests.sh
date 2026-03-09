#!/bin/bash

# ==============================================================================
# NOTE FOR REVIEWER: RSA SIGNATURE SETUP
# ==============================================================================
# This project requires an RSA private key to sign API requests (RSA-SHA256).
# Since 'certs/private.pem' is ignored by git for security, please either:
# 1. Place your own 'private.pem' in the 'certs/' directory.
# 2. Or create a dummy key for structural testing:
#    openssl genrsa -out certs/private.pem 2048
# ==============================================================================

# 1. Set PYTHONPATH to ensure local modules (utils) are discoverable
export PYTHONPATH=$PYTHONPATH:.

echo "--------------------------------------------------"
echo "🚀 Starting Wallester API Automation Suite..."
echo "--------------------------------------------------"

# 2. Execute tests and generate a self-contained HTML report
# Using 'tests/test_api.py' which contains all 6 test cases (GET, POST, PATCH, SEC)
pytest tests/test_api.py -v -s --html=report.html --self-contained-html

if [ $? -eq 0 ]; then
    echo "--------------------------------------------------"
    echo "✅ SUCCESS: All tests passed!"
    echo "📊 Report generated: report.html"
    echo "--------------------------------------------------"
else
    echo "--------------------------------------------------"
    echo "❌ FAILURE: Some tests failed. Check the report."
    echo "--------------------------------------------------"
fi

# 3. Instruction for Docker Execution
# To run the same suite in a fully isolated environment, use:
# docker build -t wallester-tests .
# docker run --rm wallester-tests