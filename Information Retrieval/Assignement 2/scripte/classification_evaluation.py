import csv
import os
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


def load_classification_data(csv_path):
    """
    Load classification data from CSV file.
    
    Args:
        csv_path: Path to the CSV file
    
    Returns:
        Tuple of (true_labels, predicted_labels, categories)
    """
    true_labels = []
    predicted_labels = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if 'real_category' in row and 'prediction' in row:
                true_label = row['real_category'].strip()
                pred_label = row['prediction'].strip()
                
                # Skip empty labels
                if true_label and pred_label:
                    true_labels.append(true_label)
                    predicted_labels.append(pred_label)
    
    # Get unique categories
    all_categories = sorted(list(set(true_labels + predicted_labels)))
    
    return true_labels, predicted_labels, all_categories


def compute_global_accuracy(true_labels, predicted_labels):
    """
    Compute global accuracy.
    
    Args:
        true_labels: List of true labels
        predicted_labels: List of predicted labels
    
    Returns:
        Accuracy score (float)
    """
    return accuracy_score(true_labels, predicted_labels)


def compute_per_category_metrics(true_labels, predicted_labels, categories):
    """
    Compute precision, recall, and F1-score for each category.
    
    Args:
        true_labels: List of true labels
        predicted_labels: List of predicted labels
        categories: List of all categories
    
    Returns:
        Dictionary with metrics for each category
    """
    precision, recall, f1, support = precision_recall_fscore_support(
        true_labels, predicted_labels, labels=categories, zero_division=0
    )
    
    metrics = {}
    for i, category in enumerate(categories):
        metrics[category] = {
            'precision': precision[i],
            'recall': recall[i],
            'f1_score': f1[i],
            'support': support[i]  # Number of true instances
        }
    
    return metrics


def build_confusion_matrix(true_labels, predicted_labels, categories):
    """
    Build confusion matrix.
    
    Args:
        true_labels: List of true labels
        predicted_labels: List of predicted labels
        categories: List of all categories
    
    Returns:
        Confusion matrix (numpy array)
    """
    return confusion_matrix(true_labels, predicted_labels, labels=categories)


def plot_confusion_matrix(cm, categories, output_path):
    """
    Plot and save confusion matrix.
    
    Args:
        cm: Confusion matrix
        categories: List of category names
        output_path: Path to save the plot
    """
    plt.figure(figsize=(12, 10))
    
    # Normalize confusion matrix for better visualization
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues',
                xticklabels=categories, yticklabels=categories,
                cbar_kws={'label': 'Normalized Frequency'})
    
    plt.title('Confusion Matrix (Normalized)', fontsize=14, fontweight='bold')
    plt.xlabel('Predicted Category', fontsize=12)
    plt.ylabel('True Category', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nConfusion matrix plot saved to: {output_path}")


def assess_reliability(accuracy, metrics, categories):
    """
    Assess if the classification system is reliable enough.
    
    Args:
        accuracy: Global accuracy
        metrics: Dictionary with per-category metrics
        categories: List of all categories
    
    Returns:
        Assessment string
    """
    assessment = []
    assessment.append("\n" + "=" * 80)
    assessment.append("RELIABILITY ASSESSMENT")
    assessment.append("=" * 80)
    
    # Global accuracy assessment
    if accuracy >= 0.9:
        acc_level = "Excellent"
    elif accuracy >= 0.8:
        acc_level = "Good"
    elif accuracy >= 0.7:
        acc_level = "Moderate"
    elif accuracy >= 0.6:
        acc_level = "Fair"
    else:
        acc_level = "Poor"
    
    assessment.append(f"\nGlobal Accuracy: {accuracy:.4f} ({acc_level})")
    
    # Per-category analysis
    assessment.append("\nPer-Category Analysis:")
    assessment.append("-" * 80)
    
    poor_categories = []
    good_categories = []
    
    for category in categories:
        f1 = metrics[category]['f1_score']
        precision = metrics[category]['precision']
        recall = metrics[category]['recall']
        support = metrics[category]['support']
        
        if f1 < 0.5:
            poor_categories.append(category)
        elif f1 >= 0.7:
            good_categories.append(category)
    
    assessment.append(f"\nCategories with F1-score >= 0.7 (Good): {len(good_categories)}/{len(categories)}")
    assessment.append(f"Categories with F1-score < 0.5 (Poor): {len(poor_categories)}/{len(categories)}")
    
    if poor_categories:
        assessment.append(f"\nPoor performing categories: {', '.join(poor_categories[:10])}")
        if len(poor_categories) > 10:
            assessment.append(f"... and {len(poor_categories) - 10} more")
    
    # Overall assessment
    assessment.append("\n" + "-" * 80)
    if accuracy >= 0.8 and len(poor_categories) < len(categories) * 0.2:
        assessment.append("CONCLUSION: The classification system is RELIABLE ENOUGH")
        assessment.append("✓ Good global accuracy")
        assessment.append("✓ Most categories perform well")
    elif accuracy >= 0.7:
        assessment.append("CONCLUSION: The classification system is MODERATELY RELIABLE")
        assessment.append("⚠ Acceptable accuracy but some categories need improvement")
    else:
        assessment.append("CONCLUSION: The classification system is NOT RELIABLE ENOUGH")
        assessment.append("✗ Low accuracy and/or many categories underperform")
        assessment.append("✗ System needs significant improvement before deployment")
    
    assessment.append("=" * 80)
    
    return "\n".join(assessment)


if __name__ == "__main__":
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'source', 'classification_dataset_ground_truth.csv')
    output_plot_path = os.path.join(script_dir, '..', 'confusion_matrix.png')
    
    print("=" * 80)
    print("Classification System Evaluation")
    print("=" * 80)
    
    try:
        # Load data
        print("\nLoading classification data...")
        true_labels, predicted_labels, categories = load_classification_data(csv_path)
        
        print(f"Loaded {len(true_labels)} samples")
        print(f"Number of categories: {len(categories)}")
        print(f"Categories: {', '.join(categories)}")
        
        # Compute global accuracy
        print("\n" + "=" * 80)
        print("1. GLOBAL ACCURACY")
        print("=" * 80)
        accuracy = compute_global_accuracy(true_labels, predicted_labels)
        print(f"Global Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        
        # Compute per-category metrics
        print("\n" + "=" * 80)
        print("2. PER-CATEGORY METRICS (Precision / Recall / F1-Score)")
        print("=" * 80)
        metrics = compute_per_category_metrics(true_labels, predicted_labels, categories)
        
        # Display metrics in a table format
        print(f"\n{'Category':<30} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
        print("-" * 80)
        for category in categories:
            prec = metrics[category]['precision']
            rec = metrics[category]['recall']
            f1 = metrics[category]['f1_score']
            sup = metrics[category]['support']
            print(f"{category[:29]:<30} {prec:<12.4f} {rec:<12.4f} {f1:<12.4f} {sup:<10}")
        
        # Build confusion matrix
        print("\n" + "=" * 80)
        print("3. CONFUSION MATRIX")
        print("=" * 80)
        cm = build_confusion_matrix(true_labels, predicted_labels, categories)
        print(f"\nConfusion Matrix Shape: {cm.shape}")
        print("\nConfusion Matrix (first 10x10):")
        print(cm[:10, :10])
        if cm.shape[0] > 10:
            print(f"... (showing first 10x10 of {cm.shape[0]}x{cm.shape[1]} matrix)")
        
        # Plot confusion matrix
        plot_confusion_matrix(cm, categories, output_plot_path)
        
        # Assess reliability
        assessment = assess_reliability(accuracy, metrics, categories)
        print(assessment)
        
        print("\n" + "=" * 80)
        print("Evaluation completed!")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"Error: Could not find CSV file at {csv_path}")
        print("Please make sure the classification_dataset_ground_truth.csv file exists in source/")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
