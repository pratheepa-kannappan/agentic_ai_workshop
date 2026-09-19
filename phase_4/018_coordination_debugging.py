import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.llm_client import LLMClient

def coordination_failure_demo():
    """
    Simulate an infinite delegation loop.
    """
    client = LLMClient()
    print("--- COORDINATION FAILURE DEMO ---\n")
    
    history = []
    
    def agent_a(query):
        # A help desk agent that delegates technical issues
        prompt = f"""
        You are Help Desk. If query is technical, say "DELEGATE: TECH".
        Otherwise answer it.
        Query: {query}
        """
        return client.get_completion(prompt)
        
    def agent_b(query):
        # A tech support agent that delegates non-tech issues... 
        # But let's say they misunderstand "Account Locked" as administrative (Help Desk)
        # while Help Desk thinks it's technical.
        prompt = f"""
        You are Tech Support. If query is administrative (like billing or simple account status), say "DELEGATE: HELPDESK".
        Otherwise fix it.
        Query: {query}
        """
        return client.get_completion(prompt)
        
    query = "My account is locked."
    print(f"Query: {query}\n")
    
    current_agent = "HELPDESK"
    
    for i in range(6):
        print(f"Iteration {i}: Handled by {current_agent}")
        time.sleep(1)
        
        response = ""
        if current_agent == "HELPDESK":
            response = agent_a(query)
        else:
            response = agent_b(query)
            
        print(f"  Response: {response}")
        
        if "DELEGATE: TECH" in response:
            current_agent = "TECH"
        elif "DELEGATE: HELPDESK" in response:
            current_agent = "HELPDESK"
        else:
            print("  Resolved!")
            break
            
        if i == 5:
            print("\nANALYSIS: Infinite Loop detected! Agents are bouncing the ticket back and forth.")
            print("FIX: Introduce a 'Manager' or 'Router' agent, or shared state to track handoffs.")

if __name__ == "__main__":
    coordination_failure_demo()