import requests
import json

FASTAPI_URL = "http://127.0.0.1:8000/api/access"
OLLAMA_URL = "http://localhost:11434/api/generate"

def check_rbac_permission(user_id: str, resource_id: str, token: str = None):
    """Calls the FastAPI endpoint to check access permissions."""
    params = {"user_id": user_id, "resource_id": resource_id}
    if token:
        params["token"] = token
        
    try:
        response = requests.get(FASTAPI_URL, params=params)
        return response.status_code, response.json()
    except requests.exceptions.ConnectionError:
        return 500, {"error": "FastAPI server is not running at http://127.0.0.1:8000"}

def query_llama_agent(prompt: str):
    """Sends a context-aware prompt to local Llama 3.1 via Ollama."""
    payload = {
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.ConnectionError:
        return "❌ Error: Ollama server is not running on http://localhost:11434."

def run_agent_workflow(user_id: str, resource_id: str, token: str = None):
    print(f"\n[AGENT WORKFLOW] Processing request for User: '{user_id}' -> Resource: '{resource_id}'...")
    
    # Step 1: Query the FastAPI authorization gateway
    status_code, rbac_data = check_rbac_permission(user_id, resource_id, token)

    # Step 2: Construct structured prompt for Llama 3.1 based on permission response
    if status_code == 200:
        system_context = (
            f"Access granted for user '{user_id}' to resource '{resource_id}'. "
            f"Retrieved data: '{rbac_data.get('data')}'. "
            "Formulate a direct, professional confirmation message informing the user that access was approved."
        )
    else:
        detail = rbac_data.get("detail", {})
        approval_token = detail.get("approval_token", "N/A")
        notified_lead = detail.get("notified_lead", "Team Lead")
        
        system_context = (
            f"Access denied for user '{user_id}' attempting to access resource '{resource_id}'. "
            f"Team Lead '{notified_lead}' has been notified with Approval Token '{approval_token}'. "
            "Formulate a helpful denial message explaining that access was blocked, their team lead was alerted, and provide the token for reference."
        )

    # Step 3: Get Llama 3.1 natural language response
    ai_response = query_llama_agent(system_context)
    
    print("\n🤖 Llama 3.1 AI Agent Response:")
    print("-" * 50)
    print(ai_response)
    print("-" * 50)

# --- RUN TEST WORKFLOWS ---
if __name__ == "__main__":
    # Test 1: Authorized user (Alice / U1)
    run_agent_workflow(user_id="U1", resource_id="Project_A_API")

    # Test 2: Unauthorized user (Bob / U2)
    run_agent_workflow(user_id="U2", resource_id="Project_A_API")
