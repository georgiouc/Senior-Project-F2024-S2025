import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np

def categorize_by_magnitude(values):
    """Categorize features into groups based on order of magnitude"""
    categories = {}
    
    for i, val in enumerate(values):
        if val == 0:
            magnitude = 0
        else:
            magnitude = int(np.log10(abs(val)))
        
        if magnitude not in categories:
            categories[magnitude] = []
        categories[magnitude].append(i)
    
    return categories

def plot_feature_group(features, base_counts, compare_counts, group_name, base_csv, compare_csv, output_dir):
    """Plot a specific group of features with similar magnitudes"""
    fig, ax = plt.subplots(figsize=(max(8, len(features) * 0.6), 6))
    
    width = 0.35
    x = np.arange(len(features))
    bars1 = ax.bar(x - width/2, base_counts, width, label=os.path.basename(base_csv), color='blue', alpha=0.7)
    bars2 = ax.bar(x + width/2, compare_counts, width, label=os.path.basename(compare_csv), color='orange', alpha=0.7)

    ax.set_ylabel('Value')
    ax.set_title(f'Feature Comparison - {group_name}')
    ax.set_xticks(x)
    ax.set_xticklabels(features, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add a horizontal line at y=0 to clearly show positive/negative regions
    ax.axhline(y=0, color='black', linewidth=0.8, alpha=0.8)

    # Format y-axis with thousands separators
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))

    # Annotate bars with values (handle both positive and negative values)
    for bar, value in zip(bars1, base_counts):
        height = bar.get_height()
        if height != 0:  # Only annotate non-zero values
            # Position text above positive bars, below negative bars
            xytext = (0, 3) if height > 0 else (0, -15)
            va = 'bottom' if height > 0 else 'top'
            
            ax.annotate(f'{value:,.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=xytext, textcoords="offset points",
                       ha='center', va=va, fontsize=8, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", fc="lightblue", ec="none", alpha=0.8))

    for bar, value in zip(bars2, compare_counts):
        height = bar.get_height()
        if height != 0:  # Only annotate non-zero values
            # Position text above positive bars, below negative bars
            xytext = (0, 3) if height > 0 else (0, -15)
            va = 'bottom' if height > 0 else 'top'
            
            ax.annotate(f'{value:,.1f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=xytext, textcoords="offset points",
                       ha='center', va=va, fontsize=8, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", fc="lightyellow", ec="none", alpha=0.8))

    plt.tight_layout()
    
    # Create scale-specific subfolder
    scale_folder = os.path.join(output_dir, group_name)
    os.makedirs(scale_folder, exist_ok=True)
    
    # Save plot in the appropriate subfolder
    plot_filename = f"barplot_{group_name}_{os.path.basename(base_csv).split('.')[0]}_vs_{os.path.basename(compare_csv).split('.')[0]}.png"
    plot_path = os.path.join(scale_folder, plot_filename)
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"Generated {group_name} chart")
    plt.close()
    
    return plot_path

def plot_feature_bars(base_csv, compare_csv, output_dir=None):
    # Load CSVs - handle both single dataset and comparison formats
    base_df = pd.read_csv(base_csv)
    
    # Check if this is a comparison CSV (has columns like Feature,Dataset1,Dataset2)
    if 'Feature' in base_df.columns and len(base_df.columns) >= 3:
        # This is already a comparison CSV
        features = base_df['Feature'].tolist()
        base_counts = []
        compare_counts = []
        
        # Get the dataset column names (excluding 'Feature')
        dataset_columns = [col for col in base_df.columns if col != 'Feature']
        base_col = dataset_columns[0]
        compare_col = dataset_columns[1] if len(dataset_columns) > 1 else dataset_columns[0]
        
        for _, row in base_df.iterrows():
            try:
                base_val = float(row[base_col]) if pd.notna(row[base_col]) and str(row[base_col]) != 'inf' else 0.0
                compare_val = float(row[compare_col]) if pd.notna(row[compare_col]) and str(row[compare_col]) != 'inf' else 0.0
                base_counts.append(base_val)
                compare_counts.append(compare_val)
            except (ValueError, TypeError):
                base_counts.append(0.0)
                compare_counts.append(0.0)
        
        print(f"Loaded comparison data: {base_col} vs {compare_col}")
        
    else:
        # Original format - two separate CSV files
        compare_df = pd.read_csv(compare_csv)
        features = list(base_df.columns)
        if not features:
            print("No features found in the baseline CSV file.")
            return

        # Sum/count values for each feature and convert to float
        base_counts = [float(base_df[feat].sum()) if feat in base_df.columns else 0.0 for feat in features]
        compare_counts = [float(compare_df[feat].sum()) if feat in compare_df.columns else 0.0 for feat in features]

    # Filter out features with inf/nan values but ALLOW negative values
    filtered = [
        (f, b, c)
        for f, b, c in zip(features, base_counts, compare_counts)
        if np.isfinite(b) and np.isfinite(c) and (b != 0 or c != 0)  # Include any non-zero values (positive or negative)
    ]
    if not filtered:
        print("No valid features to plot after filtering.")
        return
    features, base_counts, compare_counts = zip(*filtered)
    
    # Set up output directory
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), 'Analysis', 'Plots')
    os.makedirs(output_dir, exist_ok=True)

    # Group features by order of magnitude using the maximum absolute value for each feature
    max_abs_values = [max(abs(b), abs(c)) for b, c in zip(base_counts, compare_counts)]
    magnitude_groups = categorize_by_magnitude(max_abs_values)
    
    plot_paths = []
    
    # Create separate plots for each magnitude group
    for magnitude, indices in sorted(magnitude_groups.items()):
        if magnitude == 0:
            group_name = "Zero_Values"
        elif magnitude <= 3:
            group_name = f"Small_Scale_(10^{magnitude})"
        elif magnitude <= 6:
            group_name = f"Medium_Scale_(10^{magnitude})"
        elif magnitude <= 9:
            group_name = f"Large_Scale_(10^{magnitude})"
        else:
            group_name = f"Extreme_Scale_(10^{magnitude})"
            
        group_features = [features[i] for i in indices]
        group_base = [base_counts[i] for i in indices]
        group_compare = [compare_counts[i] for i in indices]
        
        if group_features:  # Only plot if there are features in this group
            plot_path = plot_feature_group(group_features, group_base, group_compare, 
                                         group_name, base_csv, compare_csv, output_dir)
            plot_paths.append(plot_path)

    # Create a comprehensive metadata log
    meta_path = os.path.join(
        output_dir,
        f"barplot_{os.path.basename(base_csv).split('.')[0]}_vs_{os.path.basename(compare_csv).split('.')[0]}_metadata.csv"
    )
    with open(meta_path, "w") as f:
        f.write("Feature,Base_Value,Compare_Value,Order_of_Magnitude,Ratio_Compare_to_Base\n")
        for ftr, b, c in zip(features, base_counts, compare_counts):
            max_abs = max(abs(b), abs(c))
            magnitude = int(np.log10(max_abs)) if max_abs > 0 else 0
            ratio = c / b if b != 0 else "inf" if c != 0 else "N/A"
            f.write(f"{ftr},{b},{c},{magnitude},{ratio}\n")
    
    print(f"Metadata log saved: {meta_path}")
    print(f"Generated {len(plot_paths)} charts grouped by scale")
    print("Feature bar plotting complete!")

def main():
    parser = argparse.ArgumentParser(description='Draw bar charts comparing features between two CSV files - grouped by scale for better visualization.')
    parser.add_argument('--base', required=True, help='Path to the baseline CSV file')
    parser.add_argument('--compare', required=True, help='Path to the comparison CSV file')
    parser.add_argument('--output', type=str, default=None, help='Output directory for plots')
    args = parser.parse_args()
    plot_feature_bars(args.base, args.compare, args.output)

if __name__ == "__main__":
    main()