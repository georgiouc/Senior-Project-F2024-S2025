
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



