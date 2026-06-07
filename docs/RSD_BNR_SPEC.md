# RON → user-selected target (lite spec)

## Scope
This lightweight project is intentionally small and focused on one task: provide a fast RON-based conversion view with a target currency chosen by the user.

## Current approach
- Backend: FastAPI
- Frontend: one static page with a simple converter widget
- Data source: a lightweight live FX quote endpoint used as a practical fallback for the lite app
- Goal: stay simple, low-dependency, and easy to run on local machines

## Notes on BNR and RSD
- The official BNR website is the authoritative source for Romanian exchange rates.
- This lite implementation does not depend on heavy ML, scraping, or large model packages.
- It uses a small live quote endpoint to keep the app responsive, while keeping RON fixed as the base currency and allowing the destination currency to be entered by the user.

## Recommended next step
When an official BNR endpoint or a stable scrape source for RSD becomes available, replace the fallback rate source in `main.py` without changing the public API shape.

## Public endpoints
- GET /health
- GET /api/quote?from_currency=RON&to_currency=RSD
- GET /api/convert?amount=100&from_currency=RON&to_currency=RSD
