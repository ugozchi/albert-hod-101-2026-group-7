import re
import numpy as np
from collections import Counter
import math


def preprocess_text(text):
    """
    Preprocess text by:
    - removing punctuation and special characters
    - removing numbers
    - removing words with less than 3 letters
    - tokenize the data
    """
    # prep text and remove punctuation and special characters
    ## Convert to lowercase
    text = text.lower()
    
    ## Remove punctuation and special characters (keep only alphanumeric and spaces)
    text = re.sub(r'[^\w\s]', '', text)
    
    ## Remove numbers
    text = re.sub(r'\d+', '', text)
    
    ## Tokenize (split by whitespace)
    tokens = text.split()
    
    ## Remove words with less than 3 letters
    tokens = [token for token in tokens if len(token) >= 3]
    
    return tokens


def compute_tf(document_tokens):
    """
    Compute Term Frequency (TF) for a document.
    TF = (number of times term appears in document) / (total number of terms in document)
    
    Args:
        document_tokens: List of tokens (words) in the document
    
    Returns:
        Dictionary mapping terms to their TF values
    """
    if len(document_tokens) == 0:
        return {}
    
    # Count term frequencies
    term_counts = Counter(document_tokens)
    total_terms = len(document_tokens)
    
    # Calculate TF
    tf = {term: count / total_terms for term, count in term_counts.items()}
    
    return tf


def compute_idf(documents_tokens):
    """
    Compute Inverse Document Frequency (IDF) for all terms.
    IDF = log(total number of documents / number of documents containing the term)
    
    Args:
        documents_tokens: List of lists, where each inner list contains tokens of a document
    
    Returns:
        Dictionary mapping terms to their IDF values
    """
    total_docs = len(documents_tokens)
    
    # Count in how many documents each term appears
    doc_frequency = Counter()
    for doc_tokens in documents_tokens:
        unique_terms = set(doc_tokens)
        doc_frequency.update(unique_terms)
    
    # Calculate IDF
    idf = {}
    for term, doc_count in doc_frequency.items():
        idf[term] = math.log(total_docs / doc_count)
    
    return idf


def build_tfidf_matrix(documents):
    """
    Build a TF-IDF matrix from a list of documents.
    
    Args:
        documents: List of strings (documents)
    
    Returns:
        tfidf_matrix: numpy array of shape (n_documents, n_features)
        feature_names: list of feature (word) names (vocabulary)
    """
    # Preprocess all documents
    documents_tokens = [preprocess_text(doc) for doc in documents]
    
    # Get all unique terms (vocabulary)
    all_terms = set()
    for doc_tokens in documents_tokens:
        all_terms.update(doc_tokens)
    
    # Sort vocabulary for consistent ordering
    vocabulary = sorted(list(all_terms))
    
    # Compute IDF for all terms
    idf_dict = compute_idf(documents_tokens)
    
    # Compute TF-IDF for each document
    tfidf_matrix = []
    for doc_tokens in documents_tokens:
        # Compute TF for this document
        tf_dict = compute_tf(doc_tokens)
        
        # Compute TF-IDF for each term in vocabulary
        tfidf_row = []
        for term in vocabulary:
            tf_value = tf_dict.get(term, 0.0)
            idf_value = idf_dict.get(term, 0.0)
            tfidf_value = tf_value * idf_value
            tfidf_row.append(tfidf_value)
        
        tfidf_matrix.append(tfidf_row)
    
    # Convert to numpy array
    tfidf_matrix = np.array(tfidf_matrix)
    
    return tfidf_matrix, vocabulary


def display_tfidf_matrix(tfidf_matrix, feature_names, document_names=None):
    """
    Display the TF-IDF matrix in a readable format.
    
    Args:
        tfidf_matrix: numpy array of TF-IDF values
        feature_names: list of feature names
        document_names: optional list of document names
    """
    print("\nTF-IDF Matrix:")
    print("=" * 100)
    
    # Print header
    header = f"{'Term':<20}"
    for term in feature_names:
        header += f"{term[:10]:>12}"
    print(header)
    print("-" * 100)
    
    # Print each document's TF-IDF values
    for i, row in enumerate(tfidf_matrix):
        doc_name = document_names[i] if document_names else f"Doc {i+1}"
        row_str = f"{doc_name:<20}"
        for value in row:
            row_str += f"{value:>12.4f}"
        print(row_str)
    
    print("=" * 100)


# Example usage
if __name__ == "__main__":
    import csv
    import os
    
    # Get the path to the CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', '..', 'source', 'tf_idf.csv')
    
    # Read documents from CSV
    documents = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'product_name' in row:
                    documents.append(row['product_name'])
        
        print(f"Loaded {len(documents)} documents from CSV")
        print(f"First 10 documents:")
        for i, doc in enumerate(documents[:10], 1):
            print(f"  {i}. {doc[:100]}...")
        print("\n" + "="*100 + "\n")
        
        # Build TF-IDF matrix
        print("Building TF-IDF matrix...")
        tfidf_matrix, feature_names = build_tfidf_matrix(documents)
        
        print(f"\nMatrix shape: {tfidf_matrix.shape} (documents x features)")
        print(f"Number of features: {len(feature_names)}")
        print(f"\nFirst 20 features: {feature_names[:20]}")
        
        # Display a sample of the matrix (first 5 documents, first 10 features)
        print("\n" + "="*100)
        print("Sample TF-IDF Matrix (first 5 documents, first 10 features):")
        print("="*100)
        sample_matrix = tfidf_matrix[:5, :10]
        sample_features = feature_names[:10]
        for i in range(5):
            print(f"\nDoc {i+1}: {documents[i][:60]}...")
            for j, feature in enumerate(sample_features):
                print(f"  {feature}: {sample_matrix[i][j]:.4f}")
        
    except FileNotFoundError:
        print(f"Error: Could not find CSV file at {csv_path}")
        print("Using example documents instead...")
        # Fallback to example documents
        documents = [
            "The quick brown fox jumps over the lazy dog.",
            "A quick brown dog jumps over a lazy fox.",
            "The dog and the fox are friends.",
            "Python is a great programming language for data science."
        ]
        tfidf_matrix, feature_names = build_tfidf_matrix(documents)
        display_tfidf_matrix(tfidf_matrix, feature_names)
        print(f"\nMatrix shape: {tfidf_matrix.shape} (documents x features)")
        print(f"Number of features: {len(feature_names)}")
    except Exception as e:
        print(f"Error reading CSV: {e}")