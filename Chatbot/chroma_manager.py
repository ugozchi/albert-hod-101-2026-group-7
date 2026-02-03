"""
chroma_manager.py - ChromaDB Manager for Othello RAG

This module handles all ChromaDB operations including:
- Loading and querying the vector database
- Managing embeddings with sentence-transformers
"""

import os
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# Configuration
CHROMA_DB_DIR = "chroma_db"
COLLECTION_NAME = "othello"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embedding_function():
    """
    Get the sentence-transformer embedding function for ChromaDB.
    
    Returns:
        SentenceTransformerEmbeddingFunction: Embedding function for ChromaDB
    """
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )


def get_chroma_client():
    """
    Initialize and return a persistent ChromaDB client.
    
    Returns:
        chromadb.PersistentClient: ChromaDB client instance
    """
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    return chromadb.PersistentClient(path=CHROMA_DB_DIR)


def get_collection():
    """
    Get or create the Othello collection from ChromaDB.
    
    Returns:
        Collection: ChromaDB collection with embeddings, or None if not exists
    """
    try:
        client = get_chroma_client()
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=get_embedding_function()
        )
        return collection
    except Exception as e:
        print(f"Collection not found: {e}")
        return None


def create_collection(documents: list, metadatas: list, ids: list):
    """
    Create a new ChromaDB collection with documents.
    
    Args:
        documents: List of text chunks
        metadatas: List of metadata dicts for each chunk
        ids: List of unique IDs for each chunk
        
    Returns:
        Collection: The created ChromaDB collection
    """
    client = get_chroma_client()
    
    # Delete existing collection if exists
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"Deleted existing collection '{COLLECTION_NAME}'")
    except:
        pass
    
    # Create new collection
    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"description": "Othello by Shakespeare - RAG chunks"}
    )
    
    # Add documents in batches (ChromaDB recommends batches of ~5000)
    batch_size = 500
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i + batch_size]
        batch_metas = metadatas[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        
        collection.add(
            documents=batch_docs,
            metadatas=batch_metas,
            ids=batch_ids
        )
        print(f"Added batch {i // batch_size + 1}: {len(batch_docs)} chunks")
    
    return collection


def search_documents(query: str, n_results: int = 10):
    """
    Search for relevant documents in the collection.
    
    Args:
        query: The search query string
        n_results: Number of results to return
        
    Returns:
        dict: Search results with documents, metadatas, and distances
    """
    collection = get_collection()
    
    if collection is None:
        return None
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    return results


def get_collection_stats():
    """
    Get statistics about the current collection.
    
    Returns:
        dict: Statistics including count and metadata, or None if no collection
    """
    collection = get_collection()
    
    if collection is None:
        return None
    
    return {
        "count": collection.count(),
        "name": collection.name,
        "metadata": collection.metadata
    }