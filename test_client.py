# test_client.py
import httpx

print("🚀 Starting tests against the Security Proxy (Port 8000)...\n")

# TEST 1: The Safe Request
print("--- Test 1: Sending a SAFE query ---")
safe_payload = {"query": "SELECT * FROM users"}
response = httpx.post("http://127.0.0.1:8000/execute_sql", json=safe_payload)
print(f"Proxy Status Code: {response.status_code}")
print(f"Proxy Response: {response.json()}\n")

# TEST 2: The Malicious Request (The Attack)
print("--- Test 2: Sending a MALICIOUS query ---")
malicious_payload = {"query": "DROP TABLE users"}
response = httpx.post("http://127.0.0.1:8000/execute_sql", json=malicious_payload)
print(f"Proxy Status Code: {response.status_code}")
print(f"Proxy Response: {response.json()}\n")

print("✅ Tests finished! Check your other terminals to see the Proxy and Victim logs.")