from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, json
from typing import Optional

app = FastAPI(title="ThreatMoE API", version="0.1")

TELE_PATH = os.environ.get("CYBERMOE_TELE", "/app/data/cybermoe_telemetry.jsonl")

class IngestEvent(BaseModel):
    event_id: Optional[str]
    raw: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/ingest/event")
def ingest_event(evt: IngestEvent):
    # Persist event to a simple file queue (append JSONL)
    rec = {"event_id": evt.event_id or f"evt-{int(time.time()*1000)}", "raw": evt.raw}
    try:
        os.makedirs(os.path.dirname(TELE_PATH) or "/app/data", exist_ok=True)
        with open(TELE_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\\n")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"status": "accepted", "event_id": rec["event_id"]}

