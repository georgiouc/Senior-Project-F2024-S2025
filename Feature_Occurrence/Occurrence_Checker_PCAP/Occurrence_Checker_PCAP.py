from scapy.all import rdpcap

packets = rdpcap('../PCAP/example.pcap')
tcp_count = 0
http_count = 0
for pkt in packets:
    if pkt.haslayer('IP') and pkt.haslayer('TCP'): # Checks for TCP/IP
        tcp_count += 1
    if pkt.haslayer('HTTP'): # Checks for HTTP
        http_count += 1
print(f'TCP count: {tcp_count}, HTTP count: {http_count}')
