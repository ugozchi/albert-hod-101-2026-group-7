import numpy as np
import csv
import os
import sys
import importlib.util

# Import functions from part1
part1_script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'part1', 'scripte', 'tf_idf_matrix.py')
spec = importlib.util.spec_from_file_location("tf_idf_matrix", part1_script_path)
tf_idf_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tf_idf_module)

# Import the functions we need
preprocess_text = tf_idf_module.preprocess_text
compute_tf = tf_idf_module.compute_tf
compute_idf = tf_idf_module.compute_idf
build_tfidf_matrix = tf_idf_module.build_tfidf_matrix


def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two vectors.
    
    Cosine similarity = (A · B) / (||A|| * ||B||)
    
    Args:
        vec1: numpy array (vector 1)
        vec2: numpy array (vector 2)
    
    Returns:
        Cosine similarity score (between 0 and 1)
    """
    # Compute dot product
    dot_product = np.dot(vec1, vec2)
    
    # Compute norms
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    # Avoid division by zero
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    # Compute cosine similarity
    similarity = dot_product / (norm1 * norm2)
    
    return similarity


def find_closest_products(query_products, all_products, tfidf_matrix, vocabulary, idf_dict, top_k=5):
    """
    Find the closest products for each query product using cosine similarity.
    
    Args:
        query_products: List of product names to search for
        all_products: List of all product names in the dataset
        tfidf_matrix: TF-IDF matrix for all products
        vocabulary: List of feature names
        idf_dict: IDF dictionary from the corpus
        top_k: Number of closest products to return for each query
    
    Returns:
        Dictionary mapping query products to their closest matches
    """
    # Build TF-IDF vector for each query product
    query_vectors = []
    
    for query in query_products:
        query_tokens = preprocess_text(query)
        
        # Compute TF for query
        tf_dict = compute_tf(query_tokens)
        
        # Build TF-IDF vector for query using the existing IDF from corpus
        query_vector = []
        for term in vocabulary:
            tf_value = tf_dict.get(term, 0.0)
            idf_value = idf_dict.get(term, 0.0)  # Use existing IDF
            tfidf_value = tf_value * idf_value
            query_vector.append(tfidf_value)
        
        query_vectors.append(np.array(query_vector))
    
    # Find closest products for each query
    results = {}
    
    for i, query_product in enumerate(query_products):
        query_vector = query_vectors[i]
        
        # Compute cosine similarity with all products
        similarities = []
        for j, product_vector in enumerate(tfidf_matrix):
            similarity = cosine_similarity(query_vector, product_vector)
            similarities.append((similarity, j))
        
        # Sort by similarity (descending)
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        # Get top_k closest products (excluding the query itself if it exists in dataset)
        closest = []
        for similarity, idx in similarities[:top_k + 10]:  # Get more to filter out exact matches
            product_name = all_products[idx]
            # Skip if it's the exact same product (very high similarity)
            if similarity < 0.999:  # Threshold to avoid exact matches
                closest.append((product_name, similarity))
                if len(closest) >= top_k:
                    break
        
        results[query_product] = closest
    
    return results


if __name__ == "__main__":
    # Get the path to the CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', '..', 'source', 'tf_idf.csv')
    
    # Query products
    query_products = [
        "pantalon noir",
        "balai essuie glaces avant",
        "fromage fondu kiri",
        "lentilles 265g",
        "croutons à l'ail tipiak",
        "mozarella bille 150g",
        "sac a bandouillere en nylon",
        "mais doux saint eloi",
        "croustibat findus",
        "pipe rigate carrefour"
    ]
    
    print("=" * 100)
    print("Cosine Similarity Product Search")
    print("=" * 100)
    
    # Read documents from CSV
    all_products = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'product_name' in row:
                    all_products.append(row['product_name'])
        
        print(f"\nLoaded {len(all_products)} products from CSV")
        print(f"Building TF-IDF matrix...")
        
        # Build TF-IDF matrix using functions from part1
        tfidf_matrix, vocabulary = build_tfidf_matrix(all_products)
        
        # Compute IDF dictionary for reuse
        documents_tokens = [preprocess_text(doc) for doc in all_products]
        idf_dict = compute_idf(documents_tokens)
        
        print(f"TF-IDF matrix shape: {tfidf_matrix.shape} (products x features)")
        print(f"Vocabulary size: {len(vocabulary)}")
        
        # Find closest products
        print(f"\nFinding closest products for {len(query_products)} queries...")
        print("=" * 100)
        
        results = find_closest_products(query_products, all_products, tfidf_matrix, vocabulary, idf_dict, top_k=5)
        
        # Display results
        for query_product in query_products:
            print(f"\n🔍 Query: '{query_product}'")
            print("-" * 100)
            if query_product in results and results[query_product]:
                for rank, (product, similarity) in enumerate(results[query_product], 1):
                    print(f"  {rank}. {product[:80]}... (similarity: {similarity:.4f})")
            else:
                print("  No similar products found.")
        
        print("\n" + "=" * 100)
        
    except FileNotFoundError:
        print(f"Error: Could not find CSV file at {csv_path}")
        print("Please make sure the CSV file exists in source/")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
