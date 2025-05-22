import os
import sys
import subprocess
import argparse
import shutil

# Default input/output
MAIN_CSV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../CSV'))
ANALYSIS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Feature_Analysis'))
OCCURRENCES_DIR = os.path.join(ANALYSIS_DIR, 'Occurrences')
COMPARISON_DIR = os.path.join(ANALYSIS_DIR, 'Comparison')
os.makedirs(OCCURRENCES_DIR, exist_ok=True)
os.makedirs(COMPARISON_DIR, exist_ok=True)

# Update local tool paths to output to Feature_Analysis subfolders
OCCURRENCE_CHECKER = os.path.join(os.path.dirname(__file__), 'Occurrence_Checker_CSV.py')
FEATURE_COMPARATOR = os.path.join(os.path.dirname(__file__), 'FeatureComp_v1.1.py')

def run_occurrence_checker(output_tex=False):
    print(f"[INFO] Running Feature Occurrence Checker on all CSVs in {MAIN_CSV_DIR}...")
    cmd = [
        sys.executable, OCCURRENCE_CHECKER,
        '--output', OCCURRENCES_DIR
    ]
    if output_tex:
        cmd.append('--tex')
    subprocess.run(cmd, check=True)

def run_feature_comparator(base_csv, compare_csv, output_tex=False):
    print(f"[INFO] Running Feature Comparator between {base_csv} and {compare_csv}...")
    cmd = [
        sys.executable, FEATURE_COMPARATOR,
        base_csv, compare_csv,
        '--output', COMPARISON_DIR
    ]
    if output_tex:
        cmd.append('--tex')
    subprocess.run(cmd, check=True)

def resolve_csv_path(filename):
    # If the filename is an absolute or relative path and exists, use it as-is
    if os.path.isabs(filename) and os.path.exists(filename):
        return filename
    # If it's just a filename, look in the main CSV dir
    candidate = os.path.join(MAIN_CSV_DIR, filename)
    if os.path.exists(candidate):
        return candidate
    # Fallback: try as given
    return filename

def main():
    parser = argparse.ArgumentParser(description='Analyze feature occurrence and compare feature sets.')
    parser.add_argument('--base', type=str, required=True, help='Path to the baseline (benign) CSV file.')
    parser.add_argument('--compare', type=str, required=True, help='Path to the attack or comparison CSV file.')
    parser.add_argument('--tex', action='store_true', help='Also output LaTeX table for feature comparison and occurrences.')
    args = parser.parse_args()

    # 1. Run occurrence checker on all CSVs in the main CSV dir
    run_occurrence_checker(output_tex=args.tex)

    # 2. Run feature comparator on the two specified files (resolve their paths)
    base_csv = resolve_csv_path(args.base)
    compare_csv = resolve_csv_path(args.compare)
    run_feature_comparator(base_csv, compare_csv, output_tex=args.tex)

    print(f"[DONE] Feature analysis complete. See {OCCURRENCES_DIR}/ and {COMPARISON_DIR}/ for results.")

if __name__ == '__main__':
    main()
