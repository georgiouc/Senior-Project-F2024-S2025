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
### Windows (WinDump)
#### Download from: https://www.winpcap.org/windump/

