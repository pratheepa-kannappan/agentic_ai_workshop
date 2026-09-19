import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.llm_client import LLMClient

def debate_demo():
    """
    Simulate a debate chain.
    """
    client = LLMClient()
    topic = "Should we rewrite our backend in Rust?"
    print(f"Topic: {topic}\n")
    
    sys_prompt = "You are participating in a debate. Keep your answers short (2-3 sentences)."
    
    # Initial statement
    history = f"Topic: {topic}\n"
    
    # Round 1
    prompt_pro = f"{sys_prompt}\nYou are a Rust Evangelist. Argue FOR the topic.\nHistory:\n{history}"
    response_pro = client.get_completion(prompt_pro)
    print(f"PRO: {response_pro}\n")
    history += f"Proponent: {response_pro}\n"
    
    # Round 2
    # prompt_con = f"{sys_prompt}\nYou are a Pragmatic Tech Lead who loves Python. Argue AGAINST the proponent.\nHistory:\n{history}"
    # response_con = client.get_completion(prompt_con)
    # print(f"CON: {response_con}\n")
    # history += f"Opponent: {response_con}\n"
    
    # Round 3
    # prompt_judge = f"You are a CTO. Review the debate and make a final decision.\nHistory:\n{history}"
    # decision = client.get_completion(prompt_judge)
    # print(f"JUDGE: {decision}\n")

if __name__ == "__main__":
    debate_demo()