import pandas as pd
import os

# Set the input directory to the CSV folder (relative to this script)
csv_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../CSV'))
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
            # Count non-zero / non-null entries
            count = df[feature].astype(bool).sum()
            occurrence_data.append([feature, count])

        occurrence_df = pd.DataFrame(occurrence_data, columns=["Feature", "Present"])
        # Output paths
        occurence_csv_path = os.path.join(output_dir, f"{csv_filename}_occurrence.csv")
        occurrence_df.to_csv(occurence_csv_path, index=False)
        print(f"\n{csv_file} Feature Occurrence Count Table:")
        print(occurrence_df.to_string(index=True))
