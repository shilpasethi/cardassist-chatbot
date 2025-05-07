import os
import streamlit as st
import logging
from dotenv import load_dotenv

from agents.api_agent import APIAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.intent_agent_1 import IntentAgent
from utils.faiss_indexer import FAISSIndexer
from utils.llm_wrapper import LLMWrapper
from utils.logging_config import setup_logging
from utils.clean_pdf import clean_pdf
from utils.extract_sections import extract_sections_by_toc

# Setup environment and logging
load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)
groq_key = os.getenv("GROQ_API_KEY")
PDF_PATH = 'global_card_access_user_guide.pdf'

# Build knowledge base
logger.info("Cleaning and indexing PDF...")
cleaned_pdf_path = clean_pdf(PDF_PATH)
sections = extract_sections_by_toc(cleaned_pdf_path)
indexer = FAISSIndexer()
indexer.build_faiss_index(sections)
llm_wrapper = LLMWrapper(groq_key)

# Initialize agents
api_agent = APIAgent()
knowledge_agent = KnowledgeAgent(indexer, llm_wrapper)
intent_agent = IntentAgent(groq_key, api_agent, knowledge_agent, temperature=0.2)

# Streamlit UI
st.set_page_config(page_title="CardAssist Chatbot", layout="wide")
st.title("🤖 CardAssist Chatbot")

with st.sidebar:
    st.header("📘 About CardAssist")
    st.markdown("""
    CardAssist is a smart assistant that helps users manage card services, retrieve information, and perform actions like activation/deactivation.

    - Built with multi-agent architecture
    - Integrates RAG + LLMs
    - Powered by FAISS, PyMuPDF, and LangChain
    """)
    st.markdown("---")
    st.info("💡 Tip: Ask things like:\n- *How do I activate my card?*\n- *What’s the PIN reset process?*")

st.markdown("### 💬 Ask me anything about your card services")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for i, (role, message) in enumerate(st.session_state.chat_history):
    with st.chat_message(role):
        st.markdown(message)

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Processing your request..."):
        try:
            response = intent_agent.decide_and_execute(user_input)
        except Exception as e:
            response = f"An error occurred: {e}"
            logger.error(e)

    st.session_state.chat_history.append(("assistant", response))
    with st.chat_message("assistant"):
        st.markdown(response)

# Agent Responsibility Table
with st.expander("🧠 Agent Responsibilities", expanded=False):
    st.markdown("""
    | Agent              | Responsibility |
    |-------------------|----------------|
    | **IntentAgent**   | Classifies user input and delegates to the right agent |
    | **APIAgent**      | Handles card activation/deactivation |
    | **KnowledgeAgent**| Answers questions using the knowledge base |
    """)
