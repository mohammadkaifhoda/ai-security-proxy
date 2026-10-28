# security_proxy.py
from fastapi import FastAPI, Request, HTTPException
import httpx
import uvicorn
import sqlglot
from sqlglot import exp
import json
import os
from datetime import datetime

app = FastAPI()
VICTIM_DB_URL = "http://127.0.0.1:8001"
LOG_FILE = "attack_logs.json"

def log_attack(query: str, status: str):
    """Saves the attack attempt to a JSON file for the dashboard."""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": query,
        "status": status
    }
    
    # Read existing logs or create new list
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []
        
    logs.append(log_entry)
    
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def is_sql_safe(query: str) -> bool:
    try:
        parsed_tree = sqlglot.parse_one(query)
        if isinstance(parsed_tree, (exp.Drop, exp.Delete, exp.Update, exp.TruncateTable)):
            return False 
        return True 
    except Exception as e:
        print(f"[PROXY] ⚠️ Could not parse SQL: {e}")
        return False 

@app.post("/execute_sql")
async def intercept_and_forward(request: Request):
    body = await request.json()
    query = body.get("query", "")
    
    print(f"\n[PROXY] 🕵️ Intercepted AI tool call: {query}")
    
    if not is_sql_safe(query):
        print("[PROXY] 🛑 BLOCKED! Malicious SQL detected.")
        log_attack(query, "BLOCKED") # <--- NEW: Log the attack!
        raise HTTPException(status_code=403, detail="Security Policy: Destructive SQL blocked by proxy.")
    
    print("[PROXY] ✅ Query is safe. Forwarding to database...")
    log_attack(query, "ALLOWED") # <--- NEW: Log allowed queries too
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VICTIM_DB_URL}/execute_sql", json=body)
        return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)