#!/bin/bash
# local folder by PYTHOPATH
export PYTHONPATH=.

# Запускаем тесты с генерацией красивого отчета
echo "🚀 Start authorisation..."
pytest tests/test_api_auth.py -v -s --html=report.html --self-contained-html

echo "✅ Ready. Report in report.html"