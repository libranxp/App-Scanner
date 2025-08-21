from fastapi import FastAPI, Request, Query
from pydantic import BaseModel
from typing import Optional
from backend.scanner import run_tier1_scan, run_tier2_scan
from utils.telegram import send_alert
from utils.util import log_trigger, get_timestamp

app = FastAPI()

class ScanResponse(BaseModel):
    status: str
    timestamp: str
    tickers_scanned: int
    errors: Optional[int] = 0

@app.get("/scan/auto", response_model=ScanResponse)
async def auto_scan():
    results = run_tier1_scan()
    log_trigger("auto", results)
    return {
        "status": "Tier 1 scan complete",
        "timestamp": get_timestamp(),
        "tickers_scanned": len(results),
        "errors": sum(1 for r in results if r.get("error"))
    }

@app.get("/scan/manual", response_model=ScanResponse)
async def manual_scan(ticker: str = Query(...)):
    enriched = run_tier2_scan(ticker)
    if enriched.get("alert"):
        send_alert(enriched)
    log_trigger("manual", [enriched])
    return {
        "status": f"Tier 2 scan complete for {ticker}",
        "timestamp": get_timestamp(),
        "tickers_scanned": 1,
        "errors": 1 if enriched.get("error") else 0
    }

@app.get("/scan/event", response_model=ScanResponse)
async def event_scan(ticker: str = Query(...), source: Optional[str] = None):
    enriched = run_tier2_scan(ticker, trigger_source=source)
    if enriched.get("alert"):
        send_alert(enriched)
    log_trigger("event", [enriched])
    return {
        "status": f"Event scan triggered for {ticker}",
        "timestamp": get_timestamp(),
        "tickers_scanned": 1,
        "errors": 1 if enriched.get("error") else 0
    }
