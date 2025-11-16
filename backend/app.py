from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="DNA GC% API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to your SWA domain later
    allow_methods=["*"],
    allow_headers=["*"],
)

class DnaIn(BaseModel):
    seq: str

@app.get("/ping")
def ping():
    return {"ok": True}

@app.post("/gc")
def gc(inb: DnaIn):
    s = inb.seq.upper().strip()
    if not s or any(c not in "ACGTN" for c in s):
        raise HTTPException(status_code=400, detail="Only A/C/G/T/N")
    gc_count = s.count("G") + s.count("C")
    denom = len(s) - s.count("N")
    pct = 0.0 if denom == 0 else round(100.0 * gc_count / denom, 2)
    return {"gc_percent": pct}

