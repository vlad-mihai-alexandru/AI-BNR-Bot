import os
from typing import Dict, Any

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Lite RON Converter", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FX_API_URL = "https://open.er-api.com/v6/latest"


def fetch_live_rate(base: str = "RON", target: str = "RSD") -> Dict[str, Any]:
    """Fetch a lightweight live FX quote with RON as the fixed base currency."""
    try:
        resp = requests.get(FX_API_URL + f"/{base.upper()}", timeout=20)
        resp.raise_for_status()
        payload = resp.json()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Unable to fetch live FX rate: {exc}") from exc

    if "rates" not in payload or target not in payload["rates"]:
        raise HTTPException(status_code=502, detail="Live FX response did not contain the requested rate.")

    rate = float(payload["rates"][target])
    return {
        "base": payload.get("base_code", base),
        "target": target,
        "rate": rate,
        "date": payload.get("time_last_update_utc"),
        "source": "ExchangeRate-API (lightweight fallback)",
        "note": "This lite helper keeps RON as the base currency and lets the destination currency be chosen by the user.",
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "service": "lite-ron-converter"}


@app.get("/api/quote")
def quote(from_currency: str = "RON", to_currency: str = "RSD") -> Dict[str, Any]:
    return fetch_live_rate(base=from_currency.upper(), target=to_currency.upper())


@app.get("/api/convert")
def convert(amount: float, from_currency: str = "RON", to_currency: str = "RSD") -> Dict[str, Any]:
    quote_data = fetch_live_rate(base=from_currency.upper(), target=to_currency.upper())
    converted = amount * quote_data["rate"]
    return {
        "amount": amount,
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "rate": quote_data["rate"],
        "converted": converted,
        "date": quote_data.get("date"),
        "source": quote_data.get("source"),
        "note": quote_data.get("note"),
    }


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    with open("static/index.html", "r", encoding="utf-8") as fh:
        return HTMLResponse(content=fh.read())


app.mount("/static", StaticFiles(directory="static"), name="static")
