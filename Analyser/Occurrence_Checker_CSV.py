import pandas as pd
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Check feature occurrence in CSV files.')
    parser.add_argument('--output', type=str, default=None, help='Output directory for occurrence files')
    parser.add_argument('--tex', action='store_true', help='Also output LaTeX tables')
    args = parser.parse_args()

    # Setup directories
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    csv_dir = os.path.join(project_root, 'CSV')
    
    # Use provided output dir or default to Occurrences in script directory
    if args.output:
        output_dir = args.output
    else:
        output_dir = os.path.join(os.path.dirname(__file__), 'Occurrences')
    
    os.makedirs(output_dir, exist_ok=True)

    # Process all CSV files in the CSV directory
    for csv_file in os.listdir(csv_dir):
        if csv_file.endswith('.csv'):
            csv_path = os.path.join(csv_dir, csv_file)
            csv_filename = os.path.splitext(csv_file)[0]
            df = pd.read_csv(csv_path)

            occurrence_data = []
            for feature in df.columns:
                present = df[feature].any()
                occurrence_data.append([feature, "✓" if present else "✗"])

            occurrence_df = pd.DataFrame(occurrence_data, columns=["Feature", "Present"])
            # Output paths
            occurence_csv_path = os.path.join(output_dir, f"{csv_filename}_occurrence.csv")
            occurrence_df.to_csv(occurence_csv_path, index=False)
            print(f"\n{csv_file} Feature Occurrence Table:")
            print(occurrence_df.to_string(index=True))

            # Output LaTeX version if requested
            if args.tex:
                occurrence_df['Feature'] = occurrence_df['Feature'].apply(
                    lambda x: x.replace('_', r'\\_').replace('[', r'\\texttt{[').replace(']', r']}'))
                occurrence_df.replace({'✓': r'\\checkmark', '✗': r'\\ding{55}'}, inplace=True)
                latex_table = occurrence_df.to_latex(index=False, escape=False)
                latex_table = "\\resizebox{\\textwidth}{!}{" + latex_table + "}"
                out_tex = os.path.join(output_dir, f"{csv_filename}_occurrence.tex")
                with open(out_tex, 'w') as f:
                    f.write(latex_table)
                print(f"✅ LaTeX table also saved as:\n- {out_tex}")

if __name__ == "__main__":
    main()
