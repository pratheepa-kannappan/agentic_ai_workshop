import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.llm_client import LLMClient

def weather_worker(loc): 
    return f"Weather in {loc} is Sunny, 25C"

def email_worker(content): 
    return f"Email drafted: '{content}'"

def supervisor_demo():
    client = LLMClient()
    print("--- SUPERVISOR WORKER DEMO ---\n")
    
    task = "Check weather in Tokyo and tell the team."
    
    # Supervisor Prompt
    plan_prompt = f"""
    You are a Supervisor. 
    Task: {task}
    
    Available Workers:
    - WEATHER: takes location
    - EMAIL: takes content
    
    Return a list of steps in JSON format: 
    [{{"worker": "WEATHER", "input": "..."}}, {{"worker": "EMAIL", "input": "..."}}]
    """
    
    print("Supervisor Planning...")
    plan_raw = client.get_completion(plan_prompt)
    
    # Clean JSON
    plan_raw = plan_raw.replace("```json", "").replace("```", "").strip()
    
    try:
        plan = json.loads(plan_raw)
        print(f"Plan: {json.dumps(plan, indent=2)}\n")
        
        context = ""
        for step in plan:
            worker = step["worker"]
            inp = step["input"]
            
            # Dynamic linking: If input relies on previous output (e.g. "result from step 1")
            # a real supervisor would resolve variables. Here we simulate direct execution.
            
            if worker == "WEATHER":
                res = weather_worker(inp)
                context += f"Weather Report: {res}\n"
                print(f"[Worker: WEATHER] {res}")
                
            elif worker == "EMAIL":
                # If input has placeholder like "use weather", we replace it with context
                if "weather" in inp.lower() or "team" in inp.lower():
                    inp = f"{inp} | {context}"
                res = email_worker(inp)
                print(f"[Worker: EMAIL] {res}")
                
    except json.JSONDecodeError:
        print(f"Failed to parse plan: {plan_raw}")

if __name__ == "__main__":
    supervisor_demo()