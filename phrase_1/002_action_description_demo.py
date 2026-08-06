import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.llm_client import LLMClient

def demonstrate_action_vs_description():
    """
    Show how an LLM describes what it *would* do, rather than doing it.
    """
    client = LLMClient()
    
    prompt = "Check the current weather in Tokyo and tell me if I should wear a coat."
    response = client.get_completion(prompt)
    print(f"User: {prompt}\n")
    prompt_1="why didn't you check the weather in tokyo?" 
    response = client.get_completion(prompt_1)
    print(f"Goal 1:{prompt_1}")
    prompt_2="send an email to boss@gmail.com sayin im late for work"
    response = client.get_completion(prompt_2)
    print(f"Goal 2:{prompt_2}")
    print(f"LLM: {response}")
    # TODO: Get completion from LLM for the weather prompt
    
    # TODO: Observe that the LLM might say "I cannot check the weather..." or 
    # hallucinate a weather report, but it certainly didn't *actually* check.
    
    # TODO: Compare with a prompt that asks to *write code* to check weather

if __name__ == "__main__":
    demonstrate_action_vs_description()
