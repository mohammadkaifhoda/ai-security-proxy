# Aegis: AI Agent Security Proxy and Observability Dashboard

An application security tool designed to protect backend infrastructure from malicious AI Agent tool calls and Prompt Injection attacks.

## Executive Summary
As enterprises deploy Agentic AI systems capable of executing code and querying databases, a critical attack surface emerges. Traditional Web Application Firewalls (WAFs) fail to detect these threats because the malicious traffic originates from authorized internal services using legitimate JSON API calls. Aegis solves this by implementing a semantic analysis layer between the AI agent and the backend database.

## Problem Statement
Large Language Models (LLMs) are susceptible to Prompt Injection. If an attacker tricks an AI agent into executing a destructive command (e.g., `DROP TABLE` or `DELETE FROM users`), the backend database will execute it, resulting in data loss or corruption.

## Solution and Architecture
Aegis is a custom reverse proxy built with FastAPI. It intercepts all outbound tool calls from the AI agent. Instead of relying on basic regular expressions, which are easily bypassed via obfuscation, Aegis utilizes Abstract Syntax Tree (AST) parsing via the `sqlglot` library. 

By parsing the SQL payload into a structural tree, the proxy can semantically understand the intent of the query. If the AST contains destructive nodes (DROP, DELETE, UPDATE, TRUNCATE), the proxy terminates the connection and returns a 403 Forbidden response before the query reaches the database.

## Key Features
- **AST-Based Payload Inspection:** Semantic analysis of SQL queries to block destructive operations regardless of syntax obfuscation.
- **Local and Private Execution:** Integrates with local LLMs (Ollama/Llama 3.2) to ensure zero data leakage to third-party cloud APIs.
- **Real-Time Observability:** Includes a Streamlit dashboard for security analysts to monitor tool call telemetry and audit blocked injection attempts.
- **Zero-Trust Design:** Implements a default-deny policy for unverified or unparseable SQL structures.

## Technology Stack
- **Backend:** Python, FastAPI, Uvicorn, HTTPX
- **Security Engine:** sqlglot (AST Parsing)
- **AI Engine:** Ollama (Llama 3.2)
- **Frontend/Observability:** Streamlit, Pandas

## Installation and Usage

### Prerequisites
1. Install [Ollama](https://ollama.com/) and pull the required model: `ollama pull llama3.2`
2. Python 3.10 or higher.

### Setup
```bash
git clone https://github.com/mohammadkaifhoda/ai-security-proxy.git
cd ai-security-proxy

python3 -m venv venv
source venv/bin/activate

pip install fastapi uvicorn httpx ollama sqlglot streamlit pandas