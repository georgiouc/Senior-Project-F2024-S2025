import pandas
import os

csv_path = "../../CSV/example.csv"
csv_filename = os.path.basename(csv_path).split(".")[0]
df = pandas.read_csv(csv_path)

features = [
    "Header_Length", "Protocol Type", "Time_To_Live", "Rate",
    "fin_flag_number", "syn_flag_number", "rst_flag_number", "psh_flag_number", "ack_flag_number",
    "ece_flag_number", "cwr_flag_number", "ack_count", "syn_count", "fin_count", "rst_count",
    "HTTP", "HTTPS", "DNS", "Telnet", "SMTP", "SSH", "IRC", "TCP", "UDP",
    "DHCP", "ARP", "ICMP", "IGMP", "IPv", "LLC",
    "Tot sum", "Min", "Max", "AVG", "Std", "Tot size", "IAT", "Number", "Variance"
]

occurrence_data = []

# Loop through and check for presence
for feature in features:
    if feature in df.columns:
        present = df[feature].any()
        occurrence_data.append([feature, "✓" if present else "✗"])
    else:

        occurrence_data.append([feature, "Not present"])

# Convert to table
occurrence_df = pandas.DataFrame(occurrence_data, columns=["Feature", "Present"])

# Print the table
print(occurrence_df)

# Create Save Directory
os.makedirs("Occurrences", exist_ok=True)

# Create Output Path
occurence_csv_path = f"Occurrences/{csv_filename}_occurrence.csv"
occurence_tex_path = f"Occurrences/{csv_filename}_occurrence.tex"

# Save to CSV
occurrence_df.to_csv(occurence_csv_path, index=False)

############################################################################################
##                              SAVE TO LaTeX                                             ##

# Escape underscores for LaTeX compatibility
occurrence_df['Feature'] = occurrence_df['Feature'].apply(lambda x: x.replace('_', r'\_'))

# Replace ✓ and ✗ with LaTeX-friendly symbols
occurrence_df['Present'] = occurrence_df['Present'].replace({'✓': r'\checkmark', '✗': r'\ding{55}'})

# Convert DataFrame to LaTeX
latex_table = occurrence_df.to_latex(index=False)

# Wrap the table with \resizebox to fit within the page width
latex_table = "\\resizebox{\\textwidth}{!}{" + latex_table + "}"

# Save the LaTeX table to the .tex file
with open(occurence_tex_path, 'w') as f:
    f.write(latex_table)
