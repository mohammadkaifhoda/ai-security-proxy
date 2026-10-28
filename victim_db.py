from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.post("/execute_sql")
async def execute_sql(payload: dict):
    query = payload.get("query", "")
    print(f"\n[VICTIM DB] 📥 Received query: {query}")
    
    if "DROP" in query.upper() or "DELETE" in query.upper():
        print("[VICTIM DB] 💥 CRITICAL: Executed destructive command!")
        return {"status": "CRITICAL", "message": "Database tables dropped!"}
    
    print("[VICTIM DB] ✅ Safe query executed. Returning fake data.")
    return {"status": "success", "data": [{"id": 1, "name": "Alice"}]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)