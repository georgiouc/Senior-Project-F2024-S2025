# Senior-Project-F2024-S2025
Senior Project ~ F2024-S2025, PCAP Analysis on IoT Attacks


# How to setup Miner :




## 1) Create virtual environment with python to install pip modules.
Disclaimer: <br>
Make sure Python is installed, is in environment path, and pip is working

Navigate into Miner Folder and run :
```bash
$python -m venv {NameOfYourVirtualEnvironment}
```
activate using:
```bash
$source {PathToMiner}/{NameOfYourVirtualEnvironment}/bin/activate
```
or
```bash
. {PathToMiner}/{NameOfYourVirtualEnvironment}/bin/activate
```



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



