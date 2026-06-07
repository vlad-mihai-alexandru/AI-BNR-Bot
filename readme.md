# Lite RON converter

## Run

1. python -m venv .venv
2. .\.venv\Scripts\Activate.ps1
3. pip install -r requirements.txt
4. uvicorn main:app --reload --port 7772

Open http://localhost:7772/

## Notes
- This version is intentionally lite.
- It keeps RON as the base currency and lets the user enter any target currency code at runtime.
- It avoids heavy model/training dependencies.

