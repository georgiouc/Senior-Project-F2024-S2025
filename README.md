
#  PCAP Analysis on IoT Attacks
## Senior Project ~ F2024-S2025
This guide will help you set up the environment for running the PCAP analysis on IoT attacks. Follow the steps below to ensure a smooth installation process. 

## Installation Guide :
### 1) Clone the repository from GitHub.

```bash
git clone https://github.com/georgiouc/Senior-Project-F2024-S2025.git
```
### 2) Navigate into the cloned repository folder.
```bash
cd Senior-Project-F2024-S2025
```
>**Disclaimer**: 
Make sure Python is installed, is added to the system's PATH environment variable, and pip and venv are also installed.
<br>**Note:** If you are on Linux, you may need to install the `python3-pip` & `python3-venv` package using your package manager. For example, on Ubuntu, you can run:
>```bash
>sudo apt install python3 python3-pip python3-venv
>```
### 3) Create a Python virtual environment 

### 🔹 On Linux/ macOS/ WSL:

>```bash
>python3 -m venv myvenv
>```
>**Note:** 'myvenv' is the name of the virtual environment, you can change it to whatever you like.

Activate using:
```bash
source myvenv/bin/activate
```
or (alternative for advanced users familiar with the syntax):
```bash
. myvenv/bin/activate
```
### 🔹 On Windows

>```bash
>python -m venv myvenv
>```
>**Note:** 'myvenv' is the name of the virtual environment, you can change it.

Activate using:
```bash
myvenv\Scripts\activate
```
or (alternative for advanced users familiar with the syntax):
```bash
myvenv\Scripts\activate.bat
```
### 🔹 On Windows (PowerShell)
Navigate into repository folder and run:
>**Note:** 'myvenv' is the name of the virtual environment, you can change it.
```bash
python -m venv myvenv
```
Activate using:
```bash
myvenv\Scripts\Activate.ps1
```
or (alternative for advanced users familiar with the syntax):
```bash
myvenv\Scripts\Activate
```


### 4) Install the required pip modules
#### When in (venv):
Install pip modules, using:
```bash
pip install -r requirements.txt
```
#### Modules that should be installed:
- dpkt
- pandas
- scapy
- scipy
- tqdm
- Jinja2
- matplotlib

#### To check installed modules, run:

```bash
pip list
```

>Disclaimer : You can always deactivate the virtual environment by running:
```bash
deactivate
```
### 5) Install  `tcpdump`


>##### **Note:** `tcpdump` is a command-line packet analyzer tool. It allows you to capture and analyze network packets in real-time, in this context we use it to split pcap files. Please make sure to update your system's package manager before installing `tcpdump` to ensure you get the latest version.


### Debian/Ubuntu
```bash
sudo apt install -y tcpdump
```
### Arch Linux
```bash
sudo pacman -S --noconfirm tcpdump
```
### Fedora
```bash
sudo dnf install -y tcpdump
```
### Mac (Homebrew)
```bash
brew install tcpdump
```
<br>

## Windows🪟(WinDump)

 **Download:** [WinDump - Official Site](https://www.winpcap.org/windump/)
 
 #### **Disclamer** :
<div style="display: flex; align-items: center;">
  <img src="image.png" alt="Alt text" style="width: 60px; height: 60px; border-radius: 50%; margin-right: 10px;">
  <span>It's generally recommended to use <a href="https://learn.microsoft.com/en-us/windows/wsl/">WSL (Windows Subsystem for Linux)</a> instead for better compatibility and tools.</span>
</div>


<br>
<br>
<br>
<br>
<br>





## **Usage Instructions**

>**Note** : The following instructions assume you have already set up the environment and installed the required dependencies as per the installation guide above.
>### 📂 PCAP Folder Structure
>
>You can organize your `.pcap` files in any way:
>
>- Place them directly in the "PCAP" folder, **or**
>- Organize them in subfolders by category (e.g., Benign, BruteForce, etc.), **or**
>- Use a mix of both.
>
>**Be aware :** Our script will automatically detect the `.pcap` files in the "PCAP" folder and its subfolders, so you can organize them as you like.
>
>
>### 🏷️ Automatic Categorization
>
>- Categories are detected from both the parent folder name and keywords in the filename.
>- Output CSVs are moved to category subfolders in CSV and a `metadata.csv` file is generated, listing all categories for each sample.
><br>
><br>

### 🚀 How to Use

1. **Generate the dataset**
    - Run the following command in your terminal or command prompt:
    ```bash
    python3 Miner/Generate_dataset.py
    ```

    - This script will process all `.pcap` files in the "PCAP" folder and its subfolders.
    - It will generate CSV files for each category and save them in the "CSV" folder.
    - A `metadata.csv` file will be created, listing all categories for each sample.
2. **View the results**:
    - The output CSV files will be in the CSV folder.
    - A `metadata.csv` file will be generated, listing all categories for each sample.
    
3. **Analyze the dataset (Optional)**:

    **Options:**
    - `--base`: Base CSV file for comparison (required)
    - `--compare`: CSV file to compare against base (required)  
    - `--tex`: Generate LaTeX tables alongside CSV files

    **Example:**
    ```bash
    python3 Analyser/Analyse_dataset.py --base Benign.csv --compare Attack.csv --tex 
    ```

    **What it generates:**
    - Feature occurrence analysis for all CSVs ( + LaTeX if `--tex` used)
    - Feature comparison between specified files ( + LaTeX if `--tex` used)

    **Results location:**
    - All analysis results are saved in `Analysis/`
    - Occurrence data: `Analysis/Occurrences/`
    - Comparison data: `Analysis/Comparison/`

    >**Note:** To specify a .csv file use the CSV/ and then tab key to autocomplete the file name.

4. **Visualize the dataset**:
    -Use the `--visualize` flag to visualize the analysis results.
    - Example command:
    ```bash
    python3 Analyser/Analyse_dataset.py --base BenignTraffic.csv --compare DDoS-ACK_Fragmentation.csv --visualize
    ```
    - This will generate various plots and save them in the `Analysis/Plots` folder, based on magnitude.

5. **Generate reports (coming soon)**:
    - Use the `report.py` script to generate reports based on the analysis results.
    - The script will generate a PDF report and save it in the `reports` folder.

