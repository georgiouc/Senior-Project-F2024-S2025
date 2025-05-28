import pandas as pd
import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Compare feature sets between CSV files.')
    parser.add_argument('base_csv', help='Base/baseline CSV file')
    parser.add_argument('compare_csv', help='CSV file to compare against the baseline')
    parser.add_argument('--output', type=str, default=None, help='Output directory for comparison files')
    parser.add_argument('--tex', action='store_true', help='Also output LaTeX tables')
    args = parser.parse_args()

    csv_paths = [args.base_csv, args.compare_csv]
    csv_filenames = [os.path.basename(p).split(".")[0] for p in csv_paths]

    baseline_path = csv_paths[0]
    baseline_name = csv_filenames[0]
    baseline_df = pd.read_csv(baseline_path)

    # Dynamically get features from the baseline CSV
    baseline_features = list(baseline_df.columns)

    comparison_data = []

    for feature in baseline_features:
        row = {"Feature": feature}
        row[baseline_name] = baseline_df[feature].sum() if feature in baseline_df.columns else 0
        for path, name in zip(csv_paths[1:], csv_filenames[1:]):
            df = pd.read_csv(path)
            row[name] = df[feature].sum() if feature in df.columns else 0
        comparison_data.append(row)

    # Optional: find extra features in comparison files not in the baseline
    for path, name in zip(csv_paths[1:], csv_filenames[1:]):
        df = pd.read_csv(path)
        extra_features = set(df.columns) - set(baseline_features)
        for extra in extra_features:
            row = {"Feature": f"[Extra] {extra}"}
            row[baseline_name] = 0  # Doesn't exist in baseline
            for n in csv_filenames[1:]:
                row[n] = df[extra].sum() if n == name else ""
            comparison_data.append(row)

    # Convert to DataFrame
    comparison_df = pd.DataFrame(comparison_data)

    # Set output directory
    if args.output:
        output_dir = args.output
    else:
        output_dir = os.path.join(os.path.dirname(__file__), 'Comparison')
    
    os.makedirs(output_dir, exist_ok=True)

    # Save comparison as CSV
    comparison_name = f"comparison_numbers_to_{baseline_name}"
    csv_output_path = os.path.join(output_dir, f"{comparison_name}.csv")
    comparison_df.to_csv(csv_output_path, index=False)
    print(f"\nComparison Table:")
    print(comparison_df.to_string(index=False))
    print(f"\n✅ CSV saved as: {csv_output_path}")

    # Generate LaTeX table if requested
    if args.tex:
        comparison_df['Feature'] = comparison_df['Feature'].apply(
            lambda x: x.replace('_', r'\\_').replace('[', r'\\texttt{[').replace(']', r']}'))
        latex_table = comparison_df.to_latex(index=False, escape=False)
        latex_table = "\\resizebox{\\textwidth}{!}{" + latex_table + "}"
        tex_output_path = os.path.join(output_dir, f"{comparison_name}.tex")
        with open(tex_output_path, 'w') as f:
            f.write(latex_table)
        print(f"✅ LaTeX table also saved as: {tex_output_path}")

if __name__ == "__main__":
    main()
