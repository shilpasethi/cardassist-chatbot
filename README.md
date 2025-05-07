

# CardAssist Chatbot Prototype
CardAssist is a agentic conversational assistant designed to help users navigate card management processes such as activation, deactivation, and policy queries using AI-powered responses.

An Agentic Streamlit chatbot powered by LLMs and FAISS that assists users with card management tasks using document-based retrieval and simulated APIs

# Built using:

LLMs (Groq API / Mistral)

RAG (Retrieval-Augmented Generation)

FAISS vector search

PDF content parsing (TOC-based)

Multi-agent system architecture

# Features
Interactive Streamlit Chat Interface

Intent Classification: Determines what the user wants

Knowledge Agent: Answers based on indexed document sections

API Agent (Simulated): Executes commands like activation/deactivation

PDF Preprocessing: Cleans footers, extracts TOC-based sections

FAISS Indexing: Fast semantic search over the PDF content

# Installation & Execution

### 1. Clone the repository
git clone https://github.com/shilpasethi/cardassist-chatbot.git
cd cardassist-chatbot

### 2. Create a virtual environment
python -m venv agentic_venv
agentic_venv\Scripts\activate  # On Windows
Or
source agentic_venv/bin/activate  # On macOS/Linux

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set environment variables in .env file
GROQ_API_KEY=your_groq_api_key_here

### 5. Run the Application
streamlit run app.py
