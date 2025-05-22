
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
>Disclaimer: 
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

#### To check installed modules, run:

```bash
pip list
```

>Disclaimer : You can always deactivate the virtual environment by running:
```bash
deactivate
```
### 5) Install  `tcpdump`
>##### **Note:** `tcpdump` is a command-line packet analyzer tool. It allows you to capture and analyze network packets in real-time.


### Debian/Ubuntu
```bash
sudo apt update && sudo apt install -y tcpdump
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
 
 #### Disclamer :
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

>Note
>### 📂 PCAP Folder Structure
>
>You can organize your `.pcap` files in any way:
>
>- Place them directly in the PCAP folder, **or**
>- Organize them in subfolders by category (e.g., Benign,> BruteForce, etc.), **or**
>- Use a mix of both.
>
>The framework will automatically find and process all `.pcap` files, regardless of their location.
>
>### 🏷️ Automatic Categorization
>
>- Categories are detected from both the parent folder name and keywords in the filename.
>- Output CSVs are moved to category subfolders in CSV and a `metadata.csv` file is generated, listing all categories for each sample.
><br>
><br>

### 🚀 How to Use

1. **Place your `.pcap` files** in the PCAP folder.
2. **Run the main script**:
    ```bash
    python3 Miner/pcap_miner.py
    ```
3. **View the results**:
    - The output CSV files will be in the CSV folder.
    - A `metadata.csv` file will be generated, listing all categories for each sample.



    
4. **Analyze the results**:
    - Use the `analyze.py` script to analyze the generated CSV files.
    - The script will generate a summary of the analysis and save it in the `analysis` folder.
5. **Visualize the results**:
    - Use the `visualize.py` script to visualize the analysis results.
    - The script will generate various plots and save them in the `visualization` folder.
6. **Generate reports**:
    - Use the `report.py` script to generate reports based on the analysis results.
    - The script will generate a PDF report and save it in the `reports` folder.

