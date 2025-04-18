import pandas as pd
import os
import sys

if len(sys.argv) < 3:
    print("Usage: python compare_features.py baseline.csv comparison1.csv [comparison2.csv ...]")
    sys.exit(1)

csv_paths = sys.argv[1:]
csv_filenames = [os.path.basename(p).split(".")[0] for p in csv_paths]

baseline_path = csv_paths[0]
baseline_name = csv_filenames[0]
baseline_df = pd.read_csv(baseline_path)

# Dynamically get features from the baseline CSV
baseline_features = list(baseline_df.columns)

comparison_data = []

for feature in baseline_features:
    row = {"Feature": feature}
    row[baseline_name] = "✓"

    for path, name in zip(csv_paths[1:], csv_filenames[1:]):
        df = pd.read_csv(path)
        row[name] = "✓" if feature in df.columns else "✗"

    comparison_data.append(row)

# Optional: find extra features in comparison files not in the baseline
for path, name in zip(csv_paths[1:], csv_filenames[1:]):
    df = pd.read_csv(path)
    extra_features = set(df.columns) - set(baseline_features)
    for extra in extra_features:
        row = {"Feature": f"[Extra] {extra}"}
        row[baseline_name] = "✗"  # Doesn't exist in baseline
        for n in csv_filenames[1:]:
            row[n] = "✓" if n == name else ""  # Mark only the relevant comparison file
        comparison_data.append(row)

# Convert to DataFrame
comparison_df = pd.DataFrame(comparison_data)

# Save folder
os.makedirs("Comparison", exist_ok=True)

# File output names
out_csv = f"Comparison/comparison_to_{baseline_name}.csv"
out_tex = f"Comparison/comparison_to_{baseline_name}.tex"

# Save CSV
comparison_df.to_csv(out_csv, index=False)

# Prepare LaTeX version
comparison_df['Feature'] = comparison_df['Feature'].apply(lambda x: x.replace('_', r'\_'))
comparison_df.replace({'✓': r'\checkmark', '✗': r'\ding{55}'}, inplace=True)

latex_table = comparison_df.to_latex(index=False, escape=False)
latex_table = "\\resizebox{\\textwidth}{!}{" + latex_table + "}"

with open(out_tex, 'w') as f:
    f.write(latex_table)

print(f"✅ Comparison complete. Files saved as:\n- {out_csv}\n- {out_tex}")
