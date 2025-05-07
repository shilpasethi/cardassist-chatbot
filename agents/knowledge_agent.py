# agents/knowledge_agent.py

"""
KnowledgeAgent: Retrieves relevant information from the knowledge base and
uses an LLM to generate answers.
"""
import logging
from utils.faiss_indexer import FAISSIndexer
from utils.llm_wrapper import LLMWrapper

logger = logging.getLogger(__name__)


class KnowledgeAgent:
    """
    The KnowledgeAgent class coordinates information retrieval from the knowledge base
    and answer generation using a language model.
    """
    def __init__(self, search_simulator: FAISSIndexer, llm_wrapper: LLMWrapper):
        """
        Initialize with a search simulator (for knowledge base retrieval) and an LLM wrapper for answer generation.
        """
        self.search_simulator = search_simulator
        self.llm_wrapper = llm_wrapper

    def answer_question(self, question: str) -> str:
        """
        Retrieves relevant context for the question and uses the LLM to generate an answer.
        """
        # Retrieve top relevant passages from the knowledge base
        combined_result = self.search_simulator.search(question)
 
        if not combined_result:
            return "I'm sorry, I couldn't find information related to your question."

        prompt = f"Use the following information from the card user guide to answer the question:\n\n{combined_result}\n\nQuestion: {question}\nAnswer:"
        # Generate answer using the language model
        answer = self.llm_wrapper.generate_answer(prompt)
        return answer
