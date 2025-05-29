import os
import shutil

# === CONFIGURABLE: Add or edit categories/keywords here ===
CATEGORY_KEYWORDS = {
    'DDoS': ['ddos', 'distributed denial of service'],
    'DoS': ['dos', 'denial of service'],
    'Botnet': ['botnet'],
    'BruteForce': ['bruteforce', 'brute', 'force'],
    'Malware': ['malware'],
    'Benign': ['benign', 'normal', 'clean','good'],
    'Mirai': ['mirai' , 'bot'],
    'Reconnaissance': ['recon', 'reconnaissance'],
    'Scanning': ['scan', 'scanning' , 'portscan' , 'sweeping' , 'sweep'],
    'Injection': ['sql', 'injection'],
    'Hijacking': ['hijack', 'hijacking'],
    'Spoofing': ['spoof', 'spoofing'],
    'Flooding': ['flood', 'flooding'],
    'Malformed': ['malformed'],
    'Modbus': ['modbus'],
    'Ping': ['ping'],
    'MitM': ['mitm', 'Man-in-the-Middle'],
    'MQTT': ['mqtt'],
    'TCP': ['tcp'],
    'UDP': ['udp'],
    'ICMP': ['icmp'],
    'ARP': ['arp'],
    'HTTP': ['http'],
    'HTTPS': ['https'],
    'FTP': ['ftp'],
    'DNS': ['dns'],
    'Telnet': ['telnet'],
    'SSH': ['ssh'],
    'SMTP': ['smtp'],


    # Add more categories/keywords as needed
}

PCAP_DIR = 'PCAP/'
CSV_DIR = 'CSV/'


def get_category(filename):
    """Return a set of categories this filename matches."""
    fname = filename.lower()
    matched = set()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in fname:
                matched.add(category)
    return matched


def get_category_from_path(filepath):
    """Return a set of categories from parent folder and filename keywords (case-insensitive)."""
    categories = set()
    parent = os.path.basename(os.path.dirname(filepath)).strip().lower()
    # Check if parent folder matches any category key (case-insensitive)
    for category in CATEGORY_KEYWORDS:
        if parent == category.lower():
            categories.add(category)
    # Check if parent folder contains any keyword for any category (case-insensitive)
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.strip().lower() in parent:  # Changed from == to 'in'
                categories.add(category)
    # Check filename for keywords (case-insensitive)
    fname = os.path.basename(filepath).strip().lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.strip().lower() in fname:
                categories.add(category)
    return categories


def main():
    metadata_entries = []
    # Recursively find all .pcap files in PCAP_DIR and subfolders
    for root, dirs, files in os.walk(PCAP_DIR):
        for file in files:
            if not file.endswith('.pcap'):
                continue
            pcap_path = os.path.join(root, file)
            base = os.path.splitext(file)[0]
            csv_name = base + '.csv'
            csv_path = os.path.join(CSV_DIR, csv_name)
            if not os.path.exists(csv_path):
                print(f"[!!] CSV not found for {file}, skipping.")
                continue
            categories = list(sorted(get_category_from_path(pcap_path)))
            if not categories:
                print(f"[!] No category found for {file}, leaving in CSV root.")
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