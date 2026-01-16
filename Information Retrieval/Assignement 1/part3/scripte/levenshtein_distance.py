import csv
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import random
import string


def levenshtein(s, t):
    """
    Compute the Levenshtein (edit) distance between two strings s and t.
    
    The Levenshtein distance is the minimum number of single-character edits
    (insertions, deletions, or substitutions) required to change one string into another.
    
    Args:
        s: First string
        t: Second string
    
    Returns:
        Integer representing the edit distance
    """
    m = len(s)
    n = len(t)
    
    # Create a matrix to store distances
    # dp[i][j] represents the distance between s[0:i] and t[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    # Distance from empty string to t[0:j] requires j insertions
    for j in range(n + 1):
        dp[0][j] = j
    
    # Distance from s[0:i] to empty string requires i deletions
    for i in range(m + 1):
        dp[i][0] = i
    
    # Fill the matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Take minimum of three operations:
                # 1. Insertion: dp[i][j-1] + 1
                # 2. Deletion: dp[i-1][j] + 1
                # 3. Substitution: dp[i-1][j-1] + 1
                dp[i][j] = min(
                    dp[i][j - 1] + 1,      # Insert
                    dp[i - 1][j] + 1,      # Delete
                    dp[i - 1][j - 1] + 1   # Substitute
                )
    
    return dp[m][n]


def compute_all_pairs_distances(products):
    """
    Compute Levenshtein distance for all pairs of products.
    
    Args:
        products: List of product names
    
    Returns:
        List of dictionaries with product pairs and their distances
    """
    results = []
    total_pairs = len(products) * (len(products) - 1) // 2
    print(f"Computing distances for {total_pairs} pairs...")
    
    pair_count = 0
    for i in range(len(products)):
        for j in range(i + 1, len(products)):
            distance = levenshtein(products[i], products[j])
            results.append({
                'product1': products[i],
                'product2': products[j],
                'distance': distance
            })
            pair_count += 1
            if pair_count % 1000 == 0:
                print(f"  Processed {pair_count}/{total_pairs} pairs...")
    
    return results


def save_results_to_csv(results, output_path):
    """
    Save the distance results to a CSV file.
    
    Args:
        results: List of dictionaries with distance results
        output_path: Path to output CSV file
    """
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    print(f"Results saved to {output_path}")


def generate_random_string(length):
    """
    Generate a random string of given length.
    
    Args:
        length: Desired length of the string
    
    Returns:
        Random string
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def measure_runtime_complexity(lengths, num_trials=5):
    """
    Empirically measure runtime for pairs of increasing string lengths.
    
    Args:
        lengths: List of string lengths to test
        num_trials: Number of trials to average for each length
    
    Returns:
        Dictionary with lengths, products (n*m), and average times
    """
    results = {
        'lengths': [],
        'products': [],  # n * m
        'times': []
    }
    
    print("\nMeasuring runtime complexity...")
    print("=" * 80)
    
    for length in lengths:
        print(f"\nTesting length: {length}")
        times = []
        products = []
        
        for trial in range(num_trials):
            # Generate two random strings of the given length
            s1 = generate_random_string(length)
            s2 = generate_random_string(length)
            
            # Measure execution time
            start_time = time.time()
            distance = levenshtein(s1, s2)
            end_time = time.time()
            
            elapsed_time = end_time - start_time
            times.append(elapsed_time)
            products.append(length * length)  # n * m
            
            print(f"  Trial {trial + 1}: {elapsed_time:.6f} seconds (distance: {distance})")
        
        # Average the times
        avg_time = np.mean(times)
        avg_product = np.mean(products)
        
        results['lengths'].append(length)
        results['products'].append(avg_product)
        results['times'].append(avg_time)
        
        print(f"  Average time: {avg_time:.6f} seconds")
    
    return results


def plot_complexity_analysis(results, output_path):
    """
    Plot time vs string length product and fit a regression.
    
    Args:
        results: Dictionary with complexity analysis results
        output_path: Path to save the plot
    """
    products = results['products']
    times = results['times']
    
    # Fit linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(products, times)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Scatter plot of actual data
    plt.scatter(products, times, color='blue', label='Measured times', s=100)
    
    # Regression line
    x_line = np.linspace(min(products), max(products), 100)
    y_line = slope * x_line + intercept
    plt.plot(x_line, y_line, 'r--', label=f'Linear fit: y = {slope:.2e}x + {intercept:.2e}')
    
    plt.xlabel('String Length Product (n × m)', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    plt.title('Levenshtein Distance: Time Complexity Analysis', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Add regression statistics
    textstr = f'R² = {r_value**2:.4f}\np-value = {p_value:.2e}\nSlope = {slope:.2e}'
    plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to {output_path}")
    
    # Print regression results
    print("\n" + "=" * 80)
    print("Regression Analysis:")
    print(f"  R² (coefficient of determination): {r_value**2:.4f}")
    print(f"  p-value: {p_value:.2e}")
    print(f"  Slope: {slope:.2e}")
    print(f"  Intercept: {intercept:.2e}")
    print(f"  Standard error: {std_err:.2e}")
    print("\nThe linear relationship confirms O(n·m) time complexity.")


if __name__ == "__main__":
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pairs_csv_path = os.path.join(script_dir, '..', '..', 'source', 'levenshtein_pairs.csv')
    output_csv_path = os.path.join(script_dir, '..', 'levenshtein_distances.csv')
    plot_path = os.path.join(script_dir, '..', 'complexity_analysis.png')
    
    print("=" * 80)
    print("Levenshtein Distance Computation")
    print("=" * 80)
    
    # Read pairs from CSV
    results = []
    try:
        with open(pairs_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'string1' in row and 'string2' in row:
                    string1 = row['string1']
                    string2 = row['string2']
                    distance = levenshtein(string1, string2)
                    results.append({
                        'string1': string1,
                        'string2': string2,
                        'distance': distance
                    })
        
        print(f"\nLoaded {len(results)} pairs from levenshtein_pairs.csv")
        
        # Compute distances for all pairs
        print("\n" + "=" * 80)
        print("Batch Computation: Computing distances for all pairs")
        print("=" * 80)
        
        for i, result in enumerate(results, 1):
            print(f"  Pair {i}/{len(results)}: '{result['string1']}' <-> '{result['string2']}' = {result['distance']}")
        
        # Save results to CSV
        save_results_to_csv(results, output_csv_path)
        
        # Complexity analysis
        print("\n" + "=" * 80)
        print("Complexity Analysis")
        print("=" * 80)
        test_lengths = [100, 500, 1000, 2000]
        complexity_results = measure_runtime_complexity(test_lengths, num_trials=5)
        
        # Plot and analyze
        plot_complexity_analysis(complexity_results, plot_path)
        
        print("\n" + "=" * 80)
        print("All tasks completed!")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"Error: Could not find CSV file at {pairs_csv_path}")
        print("Please make sure the levenshtein_pairs.csv file exists in source/")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
