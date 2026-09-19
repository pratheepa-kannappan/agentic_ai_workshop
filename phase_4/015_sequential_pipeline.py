import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.llm_client import LLMClient

class Agent:
    def __init__(self, name, role_prompt, client):
        self.name = name
        self.role_prompt = role_prompt
        self.client = client
        
    def act(self, input_text):
        prompt = f"{self.role_prompt}\nInput: {input_text}"
        print(f"[{self.name}] Processing...")
        return self.client.get_completion(prompt)

def sequential_pipeline_demo():
    """
    Demonstrate Sequential Pipeline Pattern.
    """
    client = LLMClient()
    print("--- SEQUENTIAL PIPELINE DEMO ---\n")
    
    user_email = """
    Subject: LOGIN ISSUE
    Body:
    Hi support, 
    I've been trying to reset my password for 3 days. 
    The link you sent is expired. 
    This is ridiculous. Fix it now context: I'm a premium user ID 999.
    - Bob
    """
    print(f"Original Input:\n{user_email}\n")
    
    # 1. Classifier Agent
    classifier = Agent("Classifier", 
                       "You are a triage agent. Classify the email as URGENT or NORMAL. Return only the class.", 
                       client)
    
    # 2. Extractor Agent
    extractor = Agent("Extractor", 
                      "Extract the User ID and specific issue from the text. Return JSON format.", 
                      client)
            
    # 3. Writer Agent
    writer = Agent("Writer", 
                   "You are a support agent. Write a short, empathetic response based on urgency and issue.", 
                   client)
                   
    # Execution Flow
    urgency = classifier.act(user_email)
    print(f"Urgency: {urgency}")
    
    details = extractor.act(user_email)
    print(f"Details: {details}")
    
    # Pass accumulated state to writer
    writer_input = f"Urgency: {urgency}\nDetails: {details}\nOriginal Email: {user_email}"
    response = writer.act(writer_input)
    
    print(f"\nFinal Response:\n{response}")

if __name__ == "__main__":
    sequential_pipeline_demo()