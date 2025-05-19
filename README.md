# Senior-Project-F2024-S2025
Senior Project ~ F2024-S2025, PCAP Analysis on IoT Attacks


# How to setup Miner :




## 1) Create virtual environment with python to install pip modules.
Disclaimer:
Make sure Python is installed, is added to the system's PATH environment variable, and pip is working

Navigate into Repository folder and run :
```bash
$python -m venv myenv  # Replace 'myenv' with your desired virtual environment name
```
activate using:
```bash
$source myenv/bin/activate
```
or (alternative for advanced users familiar with the syntax):
```bash
. myenv/bin/activate
```

> **Note:** Replace `{PathToMiner}` with the full path to the directory where the Miner folder is located. For example, if the Miner folder is in `/home/user/projects`, then `{PathToMiner}` would be `/home/user/projects/Miner`.



### When in (venv):
Install pip modules, using:
```bash
$pip install -r requirements.txt
```
## Modules that should be installed:
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


----------------------------------------------------------------------------------------
<br>

# 2) Install tcpdump
<br>

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



