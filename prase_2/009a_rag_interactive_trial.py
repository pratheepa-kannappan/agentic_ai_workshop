import sys
import os
import streamlit as st
import openai

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.llm_client import LLMClient
from utils.tracer import SimpleTracer #

trace_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/traces/trace_streamlit.json"))
tracer = SimpleTracer(trace_path)
tracer.clear() # clear previous run

# context_str = [
#     "France has many cities.",
#     "Paris is a city in Texas.", # Misleading
#     "The capital of France is Paris." # Correct but buried
#     "The capital of Tamil Nadu is Chennai."
# ]

context_str = [
    "France has many cities.",
    "Paris is a city in Texas.", # Misleading
    "The capital of France is Paris." # Correct but buried
    "The capital of Tamil Nadu is Chennai."
]
    
# Set the behavior or the persona of our assistant bot.
SYSTEM_PROMPT = f"You are a helpful assistant of Geography.\nAnswer the question. \nContext: {context_str}\nInstruction: Ignore irrelevant information and focus on the correct answer.\nIf the query is irrelevant to Geography or if it is NOT present in the context, force the user back to topics in the Geography topic - within the context. DO NOT answer."

st.set_page_config(page_title="Geography AI Tutor", page_icon=":robot_face:")
st.title("Geography AI Tutor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask a geography question!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

    # Generate response
    client = LLMClient()
    with st.spinner("Thinking…"):
        response = client.get_chat_completion(api_messages, temperature=0.2, max_tokens=100)
        # Create a log/trace
        tracer.log_event("send_llm_query", {"query": api_messages, "model": client._get_default_model()})

    answer = response.content if response else "⚠️ No response from the model."
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)