import sys
import os
import streamlit as st
from pypdf import PdfReader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from utils.llm_client import LLMClient

st.set_page_config(page_title="PDF RAG", page_icon="🤖")

# ---- Sidebar PDF Upload ----
with st.sidebar:
    st.subheader("PDF Source")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = None

if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        text_chunks = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_chunks.append(text.strip())

        st.session_state.pdf_context = "\n\n".join(text_chunks)
        st.sidebar.success("PDF Loaded Successfully")

    except Exception as e:
        st.sidebar.error(f"Error reading PDF: {e}")
        st.session_state.pdf_context = None

context_str = st.session_state.pdf_context

if not context_str:
    context_str = "No PDF uploaded."

SYSTEM_PROMPT = f"""
You are a helpful assistant.
Answer ONLY using the context below.
If answer not found, say: "The answer is not available in the uploaded PDF."

Context:
{context_str}
"""

# ---- Chat UI ----
import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="The Starry Night", page_icon="🌌", layout="wide")

# -----------------------------
# SIDEBAR SETTINGS
# -----------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
    max_tokens = st.slider("Max Tokens", 100, 1000, 300, 50)

    model_choice = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o"],
        index=0
    )

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Built with ❤️ using Streamlit")

# -----------------------------
# HEADER SECTION
# -----------------------------
st.title("🌌 The Starry Night")
st.caption("Ask questions based on the uploaded PDF knowledge base.")

# -----------------------------
# SESSION INIT
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# CHAT DISPLAY CONTAINER
# -----------------------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------
if prompt := st.chat_input("Ask a question based on the PDF..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    api_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *st.session_state.messages
    ]

    try:
        client = LLMClient()

        with st.spinner("Thinking... 🤖"):
            response = client.get_chat_completion(
                api_messages,
                model=model_choice,
                temperature=temperature,
                max_tokens=max_tokens
            )

        if response and response.content:
            answer = response.content
        else:
            answer = "⚠️ No response from the model."

    except Exception as e:
        answer = f"❌ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)

# -----------------------------
# DOWNLOAD CHAT HISTORY
# -----------------------------
if st.session_state.messages:
    chat_json = json.dumps(st.session_state.messages, indent=4)

    st.download_button(
        label="📥 Download Chat History",
        data=chat_json,
        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption("PDF RAG System • Powered by LLMClient")
# st.title("The Starry Night")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input("Ask a question based on the PDF"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     api_messages = [
#         {"role": "system", "content": SYSTEM_PROMPT},
#         *st.session_state.messages
#     ]

#     try:
#         client = LLMClient()

#         with st.spinner("Thinking..."):
#             response = client.get_chat_completion(
#                 api_messages,
#                 temperature=0.2,
#                 max_tokens=300
#             )

#         if response and response.content:
#             answer = response.content
#         else:
#             answer = "⚠️ No response from the model."

#     except Exception as e:
#         answer = f"Error: {e}"

#     st.session_state.messages.append({"role": "assistant", "content": answer})
#     st.chat_message("assistant").write(answer)
# import sys
# import os
# import streamlit as st
# import pypdf

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
# from utils.llm_client import LLMClient
# from utils.tracer import SimpleTracer

# try:
#     from pypdf import PdfReader
# except ImportError:
#     PdfReader = None

# trace_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/traces/trace_streamlit.json"))
# tracer = SimpleTracer(trace_path)
# tracer.clear()  # clear previous run

# st.set_page_config(page_title="PDF RAG", page_icon=":robot_face:")

# # ---- Left panel: PDF upload as knowledge source ----
# with st.sidebar:
#     st.subheader("PDF source")
#     st.caption("Upload a PDF to use as context for answers.")
#     uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], key="pdf_upload")

# # Extract text from uploaded PDF and store as context (replaces context_str)
# if "pdf_context" not in st.session_state:
#     st.session_state.pdf_context = None

# if uploaded_file is not None:
#     if PdfReader is None:
#         st.sidebar.error("Install `pypdf` to use PDF upload: pip install pypdf")
#     else:
#         try:
#             reader = PdfReader(uploaded_file)
#             chunks = []
#             for page in reader.pages:
#                 text = page.extract_text()
#                 if text:
#                     chunks.append(text.strip())
#             st.session_state.pdf_context = "\n\n".join(chunks) if chunks else None
#             st.sidebar.success(f"Loaded {len(reader.pages)} page(s).")
#         except Exception as e:
#             st.sidebar.error(f"Could not read PDF: {e}")
#             st.session_state.pdf_context = None
# else:
#     st.session_state.pdf_context = None

# # Build system prompt from PDF context (instead of hardcoded context_str)
# context_str = st.session_state.pdf_context
# if not context_str:
#     context_str = "[No PDF uploaded. Please add a PDF in the sidebar to use as knowledge base.]"

# SYSTEM_PROMPT = (
#     "You are a helpful assistant. You must answer ONLY using the context below from the uploaded PDF.\n"
#     "STRICT RULES:\n"
#     "- Use ONLY information that appears in the context. Do not use any external or general knowledge.\n"
#     "- If the answer is not in the context, say so and do not invent an answer.\n"
#     "- Do not combine context information with outside knowledge.\n"
#     f"\nContext from PDF:\n{context_str}\n"
# )

# # ---- Main area: chat ----
# st.title("PDF RAG")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input("Ask a question based on the uploaded PDF!"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)

#     api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

#     client = LLMClient()
#     with st.spinner("Thinking…"):
#         response = client.get_chat_completion(api_messages, temperature=0.2, max_tokens=100)
#         tracer.log_event("send_llm_query", {"query": api_messages, "model": client._get_default_model()})

#     answer = response.content if response else "⚠️ No response from the model."
#     st.session_state.messages.append({"role": "assistant", "content": answer})
#     st.chat_message("assistant").write(answer)