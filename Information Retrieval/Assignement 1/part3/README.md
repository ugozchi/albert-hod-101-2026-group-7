# Assignment 1 - Part 3: Levenshtein Distance

## Description
This part implements the Levenshtein (edit) distance algorithm and performs complexity analysis.

## Features
- **Levenshtein Distance Function**: Computes the minimum number of single-character edits (insertions, deletions, substitutions) needed to transform one string into another
- **Batch Computation**: Applies the function to all pairs in `levenshtein_pairs.csv`
- **Complexity Analysis**: Empirically measures runtime for strings of increasing length (100, 500, 1000, 2000)
- **Visualization**: Plots time vs string length product (n·m) and fits a linear regression

## Input
- `source/levenshtein_pairs.csv`: Contains pairs of strings to compute distances for

## Output
- `levenshtein_distances.csv`: Results with columns `string1`, `string2`, and `distance`
- `complexity_analysis.png`: Plot showing time complexity analysis with regression

## Usage
Run the script:
```bash
python scripte/levenshtein_distance.py
```

## Implementation Details
- **Algorithm**: Dynamic programming approach with O(n·m) time complexity
- **Complexity Analysis**: Confirms linear relationship between time and string length product (n·m)

## Note
Scikit-learn is **not authorized** for this assignment. All calculations are implemented manually.
