import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.llm_client import LLMClient

def prompt_engineering_demo():
    """
    Demonstrate prompt engineering techniques for RAG.
    """
    client = LLMClient()
    
    print("--- PROMPT ENGINEERING DEMO ---\n")
    
    context = """
ART STUDIO GUIDE: Aurora Fine Arts Workshop
- Course: Watercolor Landscapes (Level: Beginner to Intermediate)
- Materials Required: 300gsm watercolor paper, round brushes (size 4 & 8), watercolor palette.
- Studio Rules: No food or drinks near artwork. Clean brushes after every session.
- Exhibition Policy: Students may display up to 3 artworks in the annual gallery show.
- Instructor: Ms. Elena Rivera (Senior Artist)
- Contact Email: aurorafinearts@gmail.com
"""
    
    scenarios = [
        {"query": "What type of paper do I need?", "type": "Trivial"},
        {"query": "Can I bring coffee while painting?", "type": "Inference"},
        {"query": "As an instructor, can I display 5 paintings in the exhibition?", "type": "Role-Based"}
    ]
    
    for scenario in scenarios:
        query = scenario["query"]
        q_type = scenario["type"]
        print(f"\nScenario: {q_type} - '{query}'")
        
        # 1. Zero-Shot / Naive
        prompt_naive = f"Context: {context}\nQuestion: {query}"
        print("  [Naive Prompt] Response:")
        print("  " + client.get_completion(prompt_naive).replace("\n", "\n  "))
        
        # 2. Role-Playing + Constraints
        prompt_role = f"""
        You are a helpful technical support agent for CloudGazer.
        Use the context below to answer the customer's question.
        If the answer is not in the context, say "I don't know" and refer them to support.
        Keep answers concise (under 2 sentences).
        
        Context:
        {context}
        
        Customer Question: {query}
        """
        print("  [Role-Play Prompt] Response:")
        print("  " + client.get_completion(prompt_role).replace("\n", "\n  "))
        
        # 3. Chain-of-Thought
        prompt_cot = f"""
        Context: {context}
        Question: {query}
        
        Let's think step by step.
        1. Analyze the user's problem.
        2. Check the manual for relevant sections.
        3. Formulate the answer.
        """
        print("  [CoT Prompt] Response:")
        print("  " + client.get_completion(prompt_cot).replace("\n", "\n  "))

if __name__ == "__main__":
    prompt_engineering_demo()