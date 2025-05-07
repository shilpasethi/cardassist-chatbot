import os
import logging

#import faiss
import numpy as np
from langchain_community.vectorstores import FAISS
#from langchain_community.embeddings import HuggingFaceEmbeddings,
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.schema import Document

logger = logging.getLogger(__name__)


class FAISSIndexer:
    """
    FAISSIndexer: Index knowledge base documents using embeddings and FAISS.
    Supports structured PDFs including tables and TOC using pdfplumber.
    """

    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the indexer with a PDF path and embedding model.
        :param pdf_path: Path to the PDF knowledge base
        :param embedding_model_name: SentenceTransformer model name for embeddings
        """
        
        #self.embedding_model = SentenceTransformer(embedding_model_name)
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.vectorstore = None
        self.index = None


    def build_faiss_index(self, chunks):
        """
        Build a FAISS vectorstore from structured chunks.
        :param chunks: List of dicts with 'content', 'section_title', and 'chunk_index'
        :return: Initialized FAISS vectorstore
        """
        logger.info("Building FAISS index with %d chunks", len(chunks))
        # Create LangChain Document objects with metadata
        
        docs = [
            Document(
                page_content=chunk['text'],
                metadata={
                    "section_title": chunk['title'],
                    "chunk_index": chunk.get("chunk_index")
                }
            )
            for chunk in chunks
        ]
        # Create FAISS vectorstore and store on self for access by other methods
        self.vectorstore = FAISS.from_documents(docs, embedding=self.embeddings)
        logger.info("FAISS vectorstore built and saved to instance")
        return self.vectorstore

    def search(self, query: str, top_k: int = 3):
        """
        Perform semantic search over the FAISS vectorstore.
        :param query: Query string
        :param top_k: Number of results to return
        :return: List of Document objects with metadata
        """
        
        if not self.vectorstore:
            logger.error("Vectorstore is not initialized. Call build_faiss_index() first.")
            raise ValueError("Index not built. Please run build_faiss_index() before searching.")

        logger.info(f"Searching FAISS vectorstore for query: '{query}' (top_k={top_k})")
        results = self.vectorstore.similarity_search(query, k=top_k)
        logger.info("Search returned %d results", len(results))
        
        combined_result = ""
        for i, doc in enumerate(results):
            logger.info(f"\n--- Result {i+1} ---")
            logger.info(f"Section: {doc.metadata['section_title']} | Chunk: {doc.metadata['chunk_index']}")
            combined_result += doc.metadata['section_title'] + "  " + doc.page_content + "\n"
            print("combined_result", combined_result)
            #logger.info(doc.page_content)
        return combined_result

    
    
    # ---- 2. Search Function ----
    def semantic_search(self, query,  k: int = 3):
        results = vectorstore.similarity_search(query, k=k)
        for i, doc in enumerate(results):
            logger.info(f"\n--- Result {i+1} ---")
            logger.info(f"Section: {doc.metadata['section_title']} | Chunk: {doc.metadata['chunk_index']}")
            logger.info(doc.page_content[:400], "...")
        return results


# # Example usage
# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser(description="FAISS Indexer for PDF knowledge base")
#     parser.add_argument("pdf_path", type=str, help="Path to the PDF file to index")
#     parser.add_argument("--model", type=str, default="all-MiniLM-L6-v2", help="SentenceTransformer model name")
#     parser.add_argument("--query", type=str, default=None, help="Query string for search")
#     parser.add_argument("--top_k", type=int, default=3, help="Number of top search results")
#     args = parser.parse_args()

#     indexer = FAISSIndexer(args.pdf_path, args.model)
#     if args.query:
#         results = indexer.search(args.query, args.top_k)
#         for i, res in enumerate(results, start=1):
#             print(f"\nResult {i} (distance: {res['distance']:.4f}):\n{res['text']}")
