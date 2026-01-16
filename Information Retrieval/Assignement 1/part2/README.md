# Assignment 1 - Part 2: Cosine Similarity Product Search

## Description
This part implements a product similarity search using cosine similarity on the TF-IDF matrix built in Part 1.

## Objective
Find the closest products for a given list of query products using cosine similarity.

## Features
- **Cosine Similarity**: Computes similarity between query products and all products in the dataset
- **TF-IDF Reuse**: Reuses the TF-IDF matrix and preprocessing functions from Part 1
- **Top-K Results**: Returns the 5 most similar products for each query

## Query Products
The script searches for similar products to:
- pantalon noir
- balai essuie glaces avant
- fromage fondu kiri
- lentilles 265g
- croutons à l'ail tipiak
- mozarella bille 150g
- sac a bandouillere en nylon
- mais doux saint eloi
- croustibat findus
- pipe rigate carrefour

## Usage
Run the script:
```bash
python scripte/cosine_similarity_search.py
```

## Implementation Details
- **Cosine Similarity Formula**: `cos(θ) = (A · B) / (||A|| * ||B||)`
- The script imports and reuses all preprocessing and TF-IDF functions from Part 1
- Only the cosine similarity calculation and search logic are new in this part

## Note
Scikit-learn is **not authorized** for this assignment. All calculations are implemented manually.
