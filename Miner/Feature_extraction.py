import dpkt
import pandas as pd
import json
from scapy.all import *
from Communication_features import Communication_wifi, Communication_zigbee
from Connectivity_features import Connectivity_features_basic, Connectivity_features_time, \
    Connectivity_features_flags_bytes
from Dynamic_features import Dynamic_features
from Layered_features import L3, L4, L2, L1
from Supporting_functions import get_protocol_name, get_flow_info, get_flag_values, compare_flow_flags, \
    get_src_dst_packets, calculate_incoming_connections, \
    calculate_packets_counts_per_ips_proto, calculate_packets_count_per_ports_proto
    
from tqdm import tqdm
import time
import datetime 

class Feature_extraction():
    columns = ["ts","Header_Length","Protocol Type","Time_To_Live","Rate", 
                   "fin_flag_number","syn_flag_number","rst_flag_number"
                   ,"psh_flag_number","ack_flag_number","ece_flag_number","cwr_flag_number",
                   "ack_count", "syn_count", "fin_count","rst_count",           
                   "HTTP", "HTTPS", "DNS", "Telnet","SMTP", "SSH", "IRC", "TCP", "UDP", "DHCP","ARP", "ICMP", "IGMP", "IPv", "LLC",
                   "Tot sum", "Min", "Max", "AVG", "Std","Tot size", "IAT", "Number", "Variance", "Duration",
                   "Max_Flow_Duration", "Avg_Flow_Duration", "Flow_Count"]
    
    
    def pcap_evaluation(self,pcap_file,csv_file_name):
        global ethsize, src_ports, dst_ports, src_ips, dst_ips, ips , tcpflows, udpflows, src_packet_count, dst_packet_count, src_ip_byte, dst_ip_byte
        global protcols_count, tcp_flow_flgs, incoming_packets_src, incoming_packets_dst, packets_per_protocol, average_per_proto_src
        global average_per_proto_dst, average_per_proto_src_port, average_per_proto_dst_port
        columns = ["ts","Header_Length","Protocol Type","Time_To_Live","Rate", "fin_flag_number","syn_flag_number","rst_flag_number"
                   ,"psh_flag_number","ack_flag_number","ece_flag_number","cwr_flag_number",
                   "ack_count", "syn_count", "fin_count","rst_count",           
                   "HTTP", "HTTPS", "DNS", "Telnet","SMTP", "SSH", "IRC", "TCP", "UDP", "DHCP","ARP", "ICMP", "IGMP", "IPv", "LLC",
                   "Tot sum", "Min", "Max", "AVG", "Std","Tot size", "IAT", "Number", "Variance", "Duration",
                   "Max_Flow_Duration", "Avg_Flow_Duration", "Flow_Count"]
        base_row = {c:[] for c in columns}
        #print(base_row)
        start = time.time()
        ethsize = []
        src_ports = {}  # saving the number of source port used
        dst_ports = {}  # saving the number of destination port used
        tcpflows = {}  # saving the whole tcpflows
        udpflows = {}  # saving the whole udpflows 
        src_packet_count = {}  # saving the number of packets per source IP
        dst_packet_count = {}  # saving the number of packets per destination IP
        dst_port_packet_count = {}  # saving the number of packets per destinatio n port
        src_ip_byte, dst_ip_byte = {}, {}
        tcp_flow_flags = {}  # saving the number of flags for each flow
        packets_per_protocol = {}   # saving the number of packets per protocol
        average_per_proto_src = {}  # saving the number of packets per protocol and src_ip
        average_per_proto_dst = {}  # saving the number of packets per protocol and dst_ip
        average_per_proto_src_port, average_per_proto_dst_port = {}, {}    # saving the number of packets per protocol and src_port and dst_port
        ips = set()  # saving unique IPs
        number_of_packets_per_trabsaction = 0  # saving the number of packets per transaction
        rate, srate, drate = 0, 0, 0
        max_duration, min_duration, sum_duration, average_duration, std_duration = 0, 0, 0, 0, 0   # duration-related features of aggerated records
        total_du = 0 # total duration
        first_pac_time = 0
        last_pac_time = 0
        incoming_pack = []
        outgoing_pack = []
        f = open(pcap_file, 'rb')
        pcap = dpkt.pcap.Reader(f)
        ## Using SCAPY for Zigbee and blutooth ##
        scapy_pak = rdpcap(pcap_file)
        count = 0  # counting the packets
        count_rows = 0
        # Initialize flow tracking variables
        flows = {}  # Format: {
                    #   (src_ip, src_port, dst_ip, dst_port, protocol): {
                    #       'forward': {
                    #           'start_ts': timestamp,
                    #           'end_ts': timestamp,
                    #           'active': bool,
                    #           'packet_count': int,
                    #           'last_seen': timestamp,
                    #           'bytes': int,
                    #           'duration': float
                    #       },
                    #       'reverse': {
                    #           'start_ts': timestamp,
                    #           'end_ts': timestamp,
                    #           'active': bool,
                    #           'packet_count': int,
                    #           'last_seen': timestamp,
                    #           'bytes': int,
                    #           'duration': float
                    #       }
                    #   }
                    # }
        completed_flows = []  # Store completed flows for statistics
        max_flow_duration = 0.0  # Track the longest flow duration
        total_flow_duration = 0.0  # Track total duration of all flows
        unique_flows = set()  # Track unique flow keys
        flow_count = 0  # Track number of unique flows
        Duration = 0.0  # Will store the current flow's duration
        avg_flow_duration = 0.0  # Initialize average flow duration
        FLOW_TIMEOUT = 60.0  # Timeout in seconds for inactive flows
        
        # Initialize window tracking
        window_start_time = None
        window_completed_flows = []
        window_max_duration = 0.0
        window_total_duration = 0.0
        
        # Track first packet time for relative timestamps
        first_packet_time = None
        for ts, buf in (pcap):
            if type(scapy_pak[count]) == scapy.layers.bluetooth:
                pass
            elif type(scapy_pak[count]) == scapy.layers.zigbee.ZigbeeNWKCommandPayload:
                zigbee = Communication_zigbee(scapy_pak[count])
            try:
               eth = dpkt.ethernet.Ethernet(buf)
               count = count + 1
            except:
                count = count + 1
                continue  # If packet format is not readable by dpkt, discard the packet

            #my_src = socket.inet_ntoa(eth.data.src)
			# read the destination IP in dst
            #my_dst = socket.inet_ntoa(eth.data.dst)

            #print ('Timestamp: ', str(datetime.datetime.utcfromtimestamp(ts)))

            

			# Print the source and destination IP
            #print('Source: ' +my_src+ ' Destination: '  +my_dst)
            ethernet_frame_size = len(buf)
            
            #print('buf size : ', len(buf))
            
            #print('ethernet_frame_size : ', ethernet_frame_size)
            #print('size : ', len(eth.data))
            ethernet_frame_type = eth.type
            total_du = total_du + ts
            # initilization #
            src_port, src_ip, dst_port, time_to_live, header_len = 0, 0, 0, 0, 0
            dst_ip, proto_type, protocol_name = 0, 0, ""
            flow_duration, flow_byte = 0, 0
            src_byte_count, dst_byte_count = 0, 0
            src_pkts, dst_pkts = 0, 0
            connection_status = 0
            number = 0
            IAT = 0
            src_to_dst_pkt, dst_to_src_pkt = 0, 0  # count of packets from src to des and vice-versa
            src_to_dst_byte, dst_to_src_byte = 0, 0  # Total bytes of packets from src to dst and vice-versa
            # flags
            flag_valus = []  # numerical values of packet(TCP) flags
            ack_count, syn_count, fin_count, urg_count, rst_count = 0, 0, 0, 0, 0
            # Layered flags
            udp, tcp, http, https, arp, smtp, irc, ssh, dns, ipv, icmp, igmp, mqtt, coap = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            telnet, dhcp, llc, mac, rarp = 0, 0, 0, 0, 0
            sum_packets, min_packets, max_packets, mean_packets, std_packets = 0, 0, 0, 0, 0
            magnite, radius, correlation, covaraince, var_ratio, weight = 0, 0, 0, 0, 0, 0
            idle_time, active_time = 0, 0
            type_info, sub_type_info, ds_status, src_mac, dst_mac, sequence, pack_id, fragments, wifi_dur = 0, 0, 0, 0, 0, 0, 0, 0, 0
            # New feature -------------------------------------------------------------------------------------------------------------------------------  
            Duration = 0  # Reset duration for each packet

            if first_packet_time == None:
                first_packet_time = ts
            Duration = ts - first_packet_time

            if eth.type == dpkt.ethernet.ETH_TYPE_IP or eth.type == dpkt.ethernet.ETH_TYPE_ARP:
                ethsize.append(ethernet_frame_size)
                srcs = {}
                dsts = {}

                if last_pac_time == 0: 
                    last_pac_time = ts
                IAT = ts - last_pac_time
                last_pac_time = ts
                if len(ethsize) % 20 == 0:  
                    dy = Dynamic_features()    
                    #sum_packets, min_packets, max_packets, mean_packets, std_packets = dy.dynamic_calculation(ethsize)
                    #print('sum packets : ', sum_packets)
                    #magnite, radius, correlation, covaraince, var_ratio, weight = dy.dynamic_two_streams(incoming_pack,
                                                                                                      #   outgoing_pack) 
                    ethsize = []
                    srcs = {}
                    dsts = {}
                    incoming_pack = []
                    outgoing_pack = []
                    first_packet_time = 0 
                    #last_pac_time = ts
                    #IAT = last_pac_time - first_pac_time
                    #first_pac_time = last_pac_time
                else:
                    dy = Dynamic_features()
                    #sum_packets, min_packets, max_packets, mean_packets, std_packets = dy.dynamic_calculation(ethsize)
                    #print('sum packets : ', sum_packets)
                    #last_pac_time = ts
                    #IAT = last_pac_time - first_pac_time
                    #first_pac_time = last_pac_time
                    #con_basic = Connectivity_features_basic(eth.data)
                    #dst = con_basic.get_destination_ip()
                    #src = con_basic.get_destination_ip()
                    #src= con_basic.get_source_ip()  
                    #print('The destination is : ', dst)
                    #print('The source 1 is : ', src)
                    #print('The source 2 is : ', src2)

               
                   
                    '''if src in dsts:
                        outgoing_pack.append(ethernet_frame_size)
                    else:
                        dsts[src] = 1
                        outgoing_pack.append(ethernet_frame_size)

                    if dst in srcs:
                        incoming_pack.append(ethernet_frame_size)
                    else:
                        srcs[dst] = 1
                        incoming_pack.append(ethernet_frame_size)'''
                    #magnite, radius, correlation, covaraince, var_ratio, weight = dy.dynamic_two_streams(incoming_pack,
                                                                                                         #outgoing_pack)
                    # print("not 20 yet")
                if eth.type == dpkt.ethernet.ETH_TYPE_IP:     # IP packets
                    # print("IP packet")
                
                    
                    ipv = 1
                    ip = eth.data

                    if ip == dpkt.ip6.IP6:  # discard IPv6 packets
                        continue


                    con_basic = Connectivity_features_basic(ip)

                    #Dynamic_packets
                    dy = Dynamic_features()
                    # number = dy.dynamic_count(protcols_count) 


                    # Connectivity_basic_features
                    src_ip = con_basic.get_source_ip()

                    proto_type = con_basic.get_protocol_type()
                    #print("The protocol type is : " , proto_type)
                    dst_ip = con_basic.get_destination_ip()

                    ips.add(dst_ip)
                    ips.add(src_ip)

                    # Connectivity_time_features
                    con_time = Connectivity_features_time(ip)
                    time_to_live= con_time.time_to_live() # time_to_live of packet
                    potential_packet = ip.data
                    
                    # Update Duration based on flow information ------------------------------------------------------------------------------------------------
                    if flow_duration > Duration:
                        Duration = flow_duration

                    # Connectivity_features_flags_bytes
                    # Counts the src ips and dest ips
                    conn_flags_bytes = Connectivity_features_flags_bytes(ip)
                    src_byte_count, dst_byte_count = conn_flags_bytes.count(src_ip_byte, dst_ip_byte) 

                    # L_three_layered_features
                    l_three = L3(potential_packet)
                    udp = l_three.udp()
                    tcp = l_three.tcp()

                    protocol_name = get_protocol_name(proto_type)
                    if protocol_name == "ICMP":
                        icmp = 1
                    elif protocol_name == "IGMP":
                        igmp = 1
                    # L1_features
                    l_one = L1(potential_packet)
                    llc = l_one.LLC()
                    mac = l_one.MAC()


                    # Extra features of Bot-IoT and Ton-IoT

                    # Average rate features
                    calculate_packets_counts_per_ips_proto(average_per_proto_src, protocol_name, src_ip, average_per_proto_dst,
                                              dst_ip)
                    calculate_packets_count_per_ports_proto(average_per_proto_src_port, average_per_proto_dst_port,
                                                            protocol_name, src_port, dst_port)
                    #----end of Average rate features ---#

                    # if packets_per_protocol.get(protocol_name):
                    #     packets_per_protocol[protocol_name] = packets_per_protocol[protocol_name] + 1
                    # else:
                    #     packets_per_protocol[protocol_name] = 1

                    # if protocol_name in protcols_count.keys():
                    #     protcols_count[protocol_name] = protcols_count[protocol_name] + 1
                    # else:
                    #     protcols_count[protocol_name] = 1


                    
                    if src_ip not in src_packet_count.keys():
                        src_packet_count[src_ip] = 1
                    else:
                        src_packet_count[src_ip] = src_packet_count[src_ip] + 1


                    if dst_ip not in dst_packet_count.keys():
                        dst_packet_count[dst_ip] = 1
                    else:
                        dst_packet_count[dst_ip] = dst_packet_count[dst_ip] + 1

                    src_pkts, dst_pkts = src_packet_count[src_ip], dst_packet_count[dst_ip] # counts of source, and dest ips
                    l_four_both = L4(src_port, dst_port)
                    coap = l_four_both.coap()
                    smtp = l_four_both.smtp()
                    # Features related to UDP
                    if type(potential_packet) == dpkt.udp.UDP:
                        src_port = con_basic.get_source_port()
                        dst_port = con_basic.get_destination_port()
                        header_len = 8 #Header length is fixed in UDP 
                        # L4 features
                        l_four = L4(src_port, dst_port)
                        l_two = L2(src_port, dst_port)
                        dhcp = l_two.dhcp()
                        dns = l_four.dns()
                        if dst_port in dst_port_packet_count.keys():
                            dst_packet_count[dst_port] = dst_port_packet_count[dst_port] + 1
                        else:
                            dst_packet_count[dst_port] = 1

                        flow = sorted([(src_ip, src_port), (dst_ip, dst_port)])
                        flow = (flow[0], flow[1])
                        flow_data = {
                            'byte_count': len(eth),
                            'header_len' : header_len,
                            'ts': ts
                        }
                        if udpflows.get(flow):
                            udpflows[flow].append(flow_data)
                        else:
                            udpflows[flow] = [flow_data]
                        packets = udpflows[flow]
                        number_of_packets_per_trabsaction = len(packets)
                        flow_byte, flow_duration, max_duration, min_duration, sum_duration, average_duration, std_duration, idle_time,active_time = get_flow_info(udpflows,flow)
                        src_to_dst_pkt, dst_to_src_pkt, src_to_dst_byte, dst_to_src_byte = get_src_dst_packets(udpflows, flow)

                    # Features related to TCP
                    elif type(potential_packet) == dpkt.tcp.TCP:
                        src_port = con_basic.get_source_port()
                        dst_port = con_basic.get_destination_port()
                        header_len = con_basic.get_header_len()
                        #print('Header Length TCP : ', header_len)
                        if dst_port in dst_port_packet_count.keys():
                            dst_packet_count[dst_port] = dst_port_packet_count[dst_port] + 1
                        else:
                            dst_packet_count[dst_port] = 1

                        flag_valus = get_flag_values(ip.data)
                        # L4 features based on TCP
                        l_four = L4(src_port,dst_port)
                        http = l_four.http()
                        https = l_four.https()
                        ssh = l_four.ssh()
                        irc = l_four.IRC()
                        smtp = l_four.smtp()
                        mqtt = l_four.mqtt()
                        telnet = l_four.telnet()

                        try:
                            http_info = dpkt.http.Response(ip.data)
                            connection_status = http_info.status
                        except: 
                            # print("No status")
                            connection_status = 0

                        flow = sorted([(src_ip, src_port), (dst_ip, dst_port)])
                        flow = (flow[0], flow[1])
                        flow_data = {
                            'byte_count': len(eth),
                            'header_len': header_len,
                            'ts': ts
                        }
                        
                        ack_count,syn_count,fin_count,urg_count,rst_count = compare_flow_flags(flag_valus,ack_count,syn_count,fin_count,urg_count,rst_count)
                     
                        if tcpflows.get(flow):
                            tcpflows[flow].append(flow_data)
                            # comparing Flow state based on its flags
                            #ack_count, syn_count, fin_count, urg_count, rst_count = tcp_flow_flags[flow]
                            #ack_count,syn_count,fin_count,urg_count,rst_count = compare_flow_flags(flag_valus,ack_count,syn_count,fin_count,urg_count,rst_count)
                         
                            #tcp_flow_flags[flow] = [ack_count, syn_count, fin_count, urg_count, rst_count]
                        else:
                            tcpflows[flow] = [flow_data]
                            #ack_count,syn_count,fin_count,urg_count,rst_count = compare_flow_flags(flag_valus, ack_count, syn_count, fin_count, urg_count, rst_count)
        
                            #tcp_flow_flags[flow] = [ack_count,syn_count,fin_count,urg_count,rst_count]
                        packets = tcpflows[flow]
                        #Get the number of packets in that specific flow
                        number_of_packets_per_trabsaction = len(packets)
                        flow_byte, flow_duration,max_duration,min_duration,sum_duration,average_duration,std_duration,idle_time,active_time = get_flow_info(tcpflows, flow)
                        #Calculates the no of packets for each flow vice -versa, and the total no. of bytes
                        src_to_dst_pkt, dst_to_src_pkt, src_to_dst_byte, dst_to_src_byte = get_src_dst_packets(tcpflows, flow)
                        # calculate_incoming_connections(incoming_packets_src, incoming_packets_dst, src_port, dst_port, src_ip, dst_ip)    

                    # Unified flow duration tracking for both TCP and UDP
                    if type(potential_packet) == dpkt.tcp.TCP or type(potential_packet) == dpkt.udp.UDP:
                        # Create flow key with 5-tuple (src_ip, src_port, dst_ip, dst_port, protocol)
                        protocol = 'TCP' if type(potential_packet) == dpkt.tcp.TCP else 'UDP'
                        flow_key = (src_ip, src_port, dst_ip, dst_port, protocol)
                        reverse_flow_key = (dst_ip, dst_port, src_ip, src_port, protocol)
                        
                        # Determine flow direction
                        direction = 'forward'
                        if flow_key not in flows and reverse_flow_key in flows:
                            # This is a reverse flow
                            flow_key = reverse_flow_key
                            direction = 'reverse'
                        
                        # Initialize flow if new
                        if flow_key not in flows:
                            flows[flow_key] = {
                                'forward': {
                                    'start_ts': None,
                                    'end_ts': None,
                                    'active': False,
                                    'packet_count': 0,
                                    'last_seen': None,
                                    'bytes': 0,
                                    'duration': 0
                                },
                                'reverse': {
                                    'start_ts': None,
                                    'end_ts': None,
                                    'active': False,
                                    'packet_count': 0,
                                    'last_seen': None,
                                    'bytes': 0,
                                    'duration': 0
                                }
                            }
                            unique_flows.add(flow_key)
                            flow_count = len(unique_flows)  # Update flow count based on unique flows
                        
                        # Get current flow direction state
                        flow_dir = flows[flow_key][direction]
                        
                        # Update flow state
                        if flow_dir['start_ts'] is None:
                            flow_dir['start_ts'] = ts
                            flow_dir['active'] = True
                        
                        flow_dir['end_ts'] = ts
                        flow_dir['packet_count'] += 1
                        flow_dir['last_seen'] = ts
                        flow_dir['bytes'] += len(eth)
                        
                        # Check for flow end conditions
                        is_flow_end = False
                        if hasattr(potential_packet, 'flags'):
                            if (type(potential_packet) == dpkt.tcp.TCP and 
                                (potential_packet.flags & dpkt.tcp.TH_FIN or potential_packet.flags & dpkt.tcp.TH_RST)) or \
                               (type(potential_packet) == dpkt.udp.UDP and 
                                (potential_packet.flags & dpkt.udp.UDP_FIN or potential_packet.flags & dpkt.udp.UDP_RST)):
                                is_flow_end = True
                        
                        # Check for timeout
                        if ts - flow_dir['last_seen'] > FLOW_TIMEOUT:
                            is_flow_end = True
                        
                        if is_flow_end:
                            flow_dir['active'] = False
                            # Calculate duration in seconds and format to avoid scientific notation
                            duration = flow_dir['end_ts'] - flow_dir['start_ts']
                            flow_dir['duration'] = float(f"{duration:.6f}")
                            
                            # Store completed flow info
                            completed_flows.append({
                                'flow': flow_key,
                                'direction': direction,
                                'start': flow_dir['start_ts'],
                                'end': flow_dir['end_ts'],
                                'duration': flow_dir['duration'],
                                'packet_count': flow_dir['packet_count'],
                                'bytes': flow_dir['bytes']
                            })
                            
                            # Update window statistics
                            window_completed_flows.append({
                                'flow': flow_key,
                                'direction': direction,
                                'duration': flow_dir['duration']
                            })
                            
                            # Update max duration
                            if flow_dir['duration'] > max_flow_duration:
                                max_flow_duration = flow_dir['duration']
                            if flow_dir['duration'] > window_max_duration:
                                window_max_duration = flow_dir['duration']
                            
                            # Update average duration for window
                            if window_completed_flows:
                                window_total_duration = sum(flow['duration'] for flow in window_completed_flows)
                                avg_flow_duration = float(f"{(window_total_duration / len(window_completed_flows)):.6f}")
                        
                        # For active flows, calculate current duration
                        if flow_dir['active']:
                            Duration = float(f"{(ts - flow_dir['start_ts']):.6f}")
                        else:
                            Duration = flow_dir['duration']

                    if flow_duration != 0:
                        rate = number_of_packets_per_trabsaction / flow_duration
                        srate = src_to_dst_pkt / flow_duration
                        drate = dst_to_src_pkt / flow_duration

                    if dst_port_packet_count.get(dst_port):
                        dst_port_packet_count[dst_port] = dst_port_packet_count[dst_port] + 1
                    else:
                        dst_port_packet_count[dst_port] = 1

                elif eth.type == dpkt.ethernet.ETH_TYPE_ARP:   # ARP packets
                    # print("ARP packet")
                    protocol_name = "ARP"
                    arp = 1
                    if packets_per_protocol.get(protocol_name):
                        packets_per_protocol[protocol_name] = packets_per_protocol[protocol_name] + 1
                    else:
                        packets_per_protocol[protocol_name] = 1


                    calculate_packets_counts_per_ips_proto(average_per_proto_src, protocol_name, src_ip, average_per_proto_dst,
                                              dst_ip)

                elif eth.type == dpkt.ieee80211:   # Wifi packets
                    wifi_info = Communication_wifi(eth.data)
                    type_info, sub_type_info, ds_status, src_mac, dst_mac, sequence, pack_id, fragments,wifi_dur = wifi_info.calculating()
                    # print("Wifi related")
                elif eth.type == dpkt.ethernet.ETH_TYPE_REVARP:  # RARP packets
                    rarp = 1   # Reverce of ARP

                # Average rate features
                # for key in average_per_proto_src:
                #     AR_P_Proto_P_SrcIP[key] = average_per_proto_src[key] / total_du

                # for key in average_per_proto_dst:
                #     AR_P_Proto_P_Dst_IP[key] = average_per_proto_dst[key] / total_du

                # for key in average_per_proto_src_port:
                #     ar_p_proto_p_src_sport[key] = average_per_proto_src_port[key] / total_du

                # for key in average_per_proto_dst_port:
                #     ar_p_proto_p_dst_dport[key] = average_per_proto_dst_port[key] / total_du

                # end of average rate features
                if len(flag_valus) == 0:
                    for i in range(0,8):
                        flag_valus.append(0)
                
                new_row = {
                           'ts': ts,
                           "Header_Length": header_len,
                            "Protocol Type": proto_type, 
                           "Time_To_Live": time_to_live,        
                                  
                            "Rate": 0,  
                          
                          "fin_flag_number": flag_valus[0],     
                          "syn_flag_number":flag_valus[1],      
                          "rst_flag_number":flag_valus[2],      
                          "psh_flag_number": flag_valus[3],     
                          "ack_flag_number": flag_valus[4],     
                          "ece_flag_number":flag_valus[6],      
                          "cwr_flag_number":flag_valus[7],      
                        
                           "ack_count":ack_count,               
                           "syn_count":syn_count,               
                           "fin_count": fin_count,                           
                           "rst_count": rst_count,              
                
                           "HTTP": http,                           
                           "HTTPS": https,                         
                           "DNS": dns,                             
                           "Telnet":telnet,                        
                           "SMTP": smtp,                           
                           "SSH": ssh,                             
                           "IRC": irc,                             
                           "TCP": tcp,                             
                           "UDP": udp,                             
                           "DHCP": dhcp,                           
                           "ARP": arp,                             
                           "ICMP": icmp,                           
                           "IGMP": igmp,                           
                           "IPv": ipv,                             
                           "LLC": llc,                             

                           "Tot sum": 0,                           #This value will be reassigned when writing the csv by using the Tot Size attribute 
                           "Min": 0,                               
                           "Max": 0,                               
                           "AVG": 0,                               
                           "Std": 0,                               
                           "Tot size": ethernet_frame_size,         
                           "IAT": IAT, 
                           "Number": 1,                            #Number of packets
                           "Variance":0,   
                           "Duration": Duration,  # Current flow's duration in seconds
                           "Max_Flow_Duration": max_flow_duration,  # Longest flow duration in seconds
                           "Avg_Flow_Duration": avg_flow_duration,  # Average flow duration in seconds
                           "Flow_Count": flow_count  # Number of unique flows seen
                          }
                for c in base_row.keys():
                    base_row[c].append(new_row[c])
                    
                count_rows+=1
                
 
        processed_df = pd.DataFrame(base_row)
        # summary
        last_row = 0
        #if(len(processed_df)%2==0):
         #   n_rows = 10
        #else: 
         #   n_rows = 15
        n_rows = 10
        df_summary_list = []
        while last_row<len(processed_df):
            #Get the first n_processed rows
            sliced_df = processed_df[last_row:last_row+n_rows]
            #Get the mode of the protocol type
            sliced_df_protocol_type_mode = pd.DataFrame(sliced_df['Protocol Type'].mode())
            sum_of_ack_count = (sliced_df["ack_count"].sum())
            sum_of_syn_count = (sliced_df['syn_count'].sum())
            sum_of_fin_count = (sliced_df['fin_count'].sum())
            sum_of_rst_count = (sliced_df['rst_count'].sum())
            total_sum_of_lengths = (sliced_df['Tot size'].sum())
            min_packet_length = (sliced_df['Tot size'].min())
            max_packet_length = (sliced_df['Tot size'].max())
            mean_packet_length = (sliced_df['Tot size'].mean())
            std_packet_length = (sliced_df['Tot size'].std())
            variance_packet_lengths = (sliced_df['Tot size'].var())
            #covariance_packet_lenghts = (sliced_df['Tot size'].cov())
            num_of_packets = (sliced_df['Number'].sum())
            duration_time_interval = (sliced_df['ts'].max() - sliced_df['ts'].min())

            #print(sliced_df_protocol_type_mode)
            #Get the mean of the tables
            sliced_df = pd.DataFrame(sliced_df.mean()).T# mean
            #replace the columns
            sliced_df['Protocol Type'] = sliced_df_protocol_type_mode
            sliced_df['ack_count'] = sum_of_ack_count
            sliced_df['syn_count'] = sum_of_syn_count
            sliced_df['fin_count'] = sum_of_fin_count
            sliced_df['rst_count'] = sum_of_rst_count
            sliced_df['Tot sum'] = total_sum_of_lengths
            sliced_df['Min'] = min_packet_length
            sliced_df['Max'] = max_packet_length
            sliced_df['AVG'] = mean_packet_length
            sliced_df['Std'] = std_packet_length
            sliced_df['Number'] = num_of_packets
            sliced_df['Rate'] = num_of_packets/duration_time_interval
            sliced_df['Variance'] = variance_packet_lengths
            #sliced_df['Covariance'] = covariance_packet_lenghts
            
            # Add duration-related summary statistics
            sliced_df['Duration'] = duration_time_interval  # This is the time window duration
            sliced_df['Max_Flow_Duration'] = sliced_df['Max_Flow_Duration'].max()  # Max flow duration in this window
            sliced_df['Avg_Flow_Duration'] = sliced_df['Avg_Flow_Duration'].mean()  # Average flow duration in this window
            sliced_df['Flow_Count'] = sliced_df['Flow_Count'].sum()  # Total flows in this window
        

            df_summary_list.append(sliced_df)
            last_row += n_rows
        processed_df = pd.concat(df_summary_list).reset_index(drop=True)
        processed_df = processed_df.drop(columns = 'ts')
        
        # Format duration columns to avoid scientific notation
        duration_columns = ['Duration', 'Max_Flow_Duration', 'Avg_Flow_Duration']
        for col in duration_columns:
            if col in processed_df.columns:
                processed_df[col] = processed_df[col].apply(lambda x: f"{x:.6f}")
        
        # Write to CSV with float_format to prevent scientific notation
        processed_df.to_csv(csv_file_name+".csv", index=False, float_format='%.6f')
        # After processing all packets, flush any remaining active flows
        active_flows_count = 0
        for flow_key, flow_data in flows.items():
            for direction in ['forward', 'reverse']:
                if flow_data[direction]['active']:
                    flow_dir = flow_data[direction]
                    flow_dir['active'] = False
                    flow_dir['end_ts'] = ts  # Use last packet timestamp as end time
                    duration = flow_dir['end_ts'] - flow_dir['start_ts']
                    flow_dir['duration'] = float(f"{duration:.6f}")
                    completed_flows.append({
                        'flow': flow_key,
                        'direction': direction,
                        'start': flow_dir['start_ts'],
                        'end': flow_dir['end_ts'],
                        'duration': flow_dir['duration'],
                        'packet_count': flow_dir['packet_count'],
                        'bytes': flow_dir['bytes']
                    })
                    window_completed_flows.append({
                        'flow': flow_key,
                        'direction': direction,
                        'duration': flow_dir['duration']
                    })
                    active_flows_count += 1
                    
                    # Update max duration for flushed flows
                    if flow_dir['duration'] > max_flow_duration:
                        max_flow_duration = flow_dir['duration']
                    if flow_dir['duration'] > window_max_duration:
                        window_max_duration = flow_dir['duration']
        
        # Format the final statistics to avoid scientific notation
        if completed_flows:
            # Global statistics
            max_flow_duration = float(f"{max(flow['duration'] for flow in completed_flows):.6f}")
            total_flow_duration = float(f"{sum(flow['duration'] for flow in completed_flows):.6f}")
            avg_flow_duration = float(f"{(total_flow_duration / len(completed_flows)):.6f}")
            
            # Log detailed flow information
            #print("\nDetailed Flow Statistics:")
            #print(f"Total unique flows: {flow_count}")
            #print(f"Completed flows: {len(completed_flows)}")
            #print(f"Active flows flushed: {active_flows_count}")
            #print(f"Max flow duration: {max_flow_duration:.6f} seconds")
            #print(f"Average flow duration: {avg_flow_duration:.6f} seconds")
            #print(f"Total flow duration: {total_flow_duration:.6f} seconds")
            
            # Print some example flow durations
            #print("\nExample Flow Durations:")
            #for flow in completed_flows[:5]:  # Show first 5 flows
                #print(f"Flow {flow['flow']} ({flow['direction']}): {flow['duration']:.6f} seconds")
        #else:
            #print("No flows were completed or flushed")
        #return True

