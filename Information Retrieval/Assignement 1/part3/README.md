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

## Results
We ran the complexity analysis on synthetic strings of lengths 100, 500, 1000, and 2000. The regression of runtime vs. string length product (n·m) gives an R² of about 0.9998, so the relationship is almost perfectly linear. The p-value is very small (< 0.05), so the link between time and n and m is statistically significant, this confirming that the Levenshtein implementation behaves as expected with **O(n*m)** * complexity.

## Note
Scikit-learn is **not authorized** for this assignment. All calculations are implemented manually.
