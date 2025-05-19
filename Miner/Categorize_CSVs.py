import os
import shutil

# === CONFIGURABLE: Add or edit categories/keywords here ===
CATEGORY_KEYWORDS = {
    'DDoS': ['ddos', 'dos'],
    'Botnet': ['botnet'],
    'BruteForce': ['bruteforce', 'brute', 'force'],
    'Malware': ['malware'],
    'Benign': ['benign'],
    'Mirai': ['mirai' , 'bot'],
    'Reconnaissance': ['recon', 'reconnaissance'],
    'Scanning': ['scan', 'scanning' , 'portscan' , 'sweeping' , 'sweep'],
    'Injection': ['sql', 'injection'],
    'Hijacking': ['hijack', 'hijacking'],
    'Spoofing': ['spoof', 'spoofing'],


    # Add more categories/keywords as needed
}

PCAP_DIR = '../PCAP/'
CSV_DIR = '../CSV/'


def get_category(filename):
    """Return a set of categories this filename matches."""
    fname = filename.lower()
    matched = set()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in fname:
                matched.add(category)
    return matched


def main():
    pcap_files = [f for f in os.listdir(PCAP_DIR) if f.endswith('.pcap')]
    metadata_entries = []
    for pcap in pcap_files:
        base = os.path.splitext(pcap)[0]
        csv_name = base + '.csv'
        csv_path = os.path.join(CSV_DIR, csv_name)
        if not os.path.exists(csv_path):
            print(f"[!] CSV not found for {pcap}, skipping.")
            continue
        categories = list(sorted(get_category(pcap)))
        if not categories:
            print(f"[!] No category found for {pcap}, leaving in CSV root.")
            continue
        # Add to metadata
        metadata_entries.append((csv_name, ';'.join(categories)))
        # Move to first category, copy to others if needed
        first_cat = categories[0]
        first_cat_dir = os.path.join(CSV_DIR, first_cat)
        os.makedirs(first_cat_dir, exist_ok=True)
        first_dest = os.path.join(first_cat_dir, csv_name)
        if not os.path.exists(first_dest):
            shutil.move(csv_path, first_dest)
            print(f"[+] {csv_name} moved to ---> {first_cat}/")
        else:
            print(f"[=] {csv_name} already in {first_cat}/")
        # Copy to any additional categories
        for cat in categories[1:]:
            cat_dir = os.path.join(CSV_DIR, cat)
            os.makedirs(cat_dir, exist_ok=True)
            dest = os.path.join(cat_dir, csv_name)
            if not os.path.exists(dest):
                shutil.copy2(first_dest, dest)
                print(f"[++] {csv_name} copied to {cat}/")
            else:
                print(f"[=] {csv_name} already in {cat}/")
    # Write metadata.csv
    metadata_path = os.path.join(CSV_DIR, 'metadata.csv')
    with open(metadata_path, 'w') as meta_f:
        meta_f.write('filename,categories\n')
        for fname, cats in metadata_entries:
            meta_f.write(f'{fname},{cats}\n')
    print(f"[i] Metadata written to {metadata_path}")

if __name__ == "__main__":
    main()
