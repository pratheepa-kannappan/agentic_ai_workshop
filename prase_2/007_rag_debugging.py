import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.llm_client import LLMClient

def rag_debugging_demo():
    """
    Simulate a RAG pipeline failure and the debugging process.
    """
    client = LLMClient()
    
    print("--- RAG DEBUGGING DEMO ---\n")
    
    # CASE 1: Retrieval Failure (Noise)
    print("CASE 1: Noisy Retrieval")
    query = "Where a good pizza in chennai?"
    
    # Simulate a retriever that pulls irrelevant docs with high similarity scores due to keyword matching
    retrieved_docs = [
        "France has many cities.",
        "Paris is a city in Texas.", # Misleading
        "The capital of France is Paris." # Correct but buried
    ]
    
    # Bad prompt doesn't prioritize or handle conflict
    context_str = "\n".join(retrieved_docs)
    prompt_bad = f"Answer: {query}\nContext: {context_str}"
    
    print(f"Docs:\n{context_str}")
    print("Generating...")
    # Might get confused by "Paris, Texas"
    response = client.get_completion(prompt_bad)
    print(f"Response[bad]: {response}")
    print("FIX: Better specific prompt instructions ('Ignore irrelevant info').\n")
    prompt_fixed = f"Answer the question using ONLY the relevant information. Ignore irrelevant details.\nQuestion: {query}\nContext: {context_str}"
    response_fixed = client.get_completion(prompt_fixed)
    print(f"Response[fixed]: {response_fixed}")
"""    
    # CASE 2: Hallucination (Ignoring Context)
    print("CASE 2: Ignoring Context")
    query_2 = "What is the secret code mentioned in the text?"
    
    # Context has the answer
    context_2 = "The secret code is BLUE-BANANA-99."
    
    # Prompt doesn't explicitly enforce context usage strongly enough
    prompt_2 = f"Answer the question: {query_2}\nContext: {context_2}"
    
    # If the model has strong priors, it might ignore context (less likely here, but common with wellknown facts)
    # Let's force a failure by NOT including context in prompt but pretending we did
    prompt_broken = f"Answer the question: {query_2}" 
    
    print(f"Response (Broken Implementation): {client.get_completion(prompt_broken)}")
    print("DEBUGGING STEP: Inspect the actual prompt sent to LLM.")
    print(f"ACTUAL PROMPT:\n{prompt_broken}")
    print("ROOT CAUSE: Variable interpolation error.")
    
    # CASE 3: Logic Failure
    print("\nCASE 3: Logic Failure")
    # ...
"""
if __name__ == "__main__":
    rag_debugging_demo()