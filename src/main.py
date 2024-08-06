import argparse
from scapy.all import sniff, TCP, UDP, ICMP, DNS, ARP, IP, wrpcap
from collections import defaultdict

# Store captured packets and tracking data
captured_packets = []
traffic_stats = defaultdict(lambda: defaultdict(int))
alert_thresholds = {
    'port_scan': 10,
    'high_volume': 100,
}
alert_log = []

# Ports to monitor
monitored_ports = {
    # Common service ports
    80, 443, #HTTP and HTTPS (web traffic)
    21, #FTP
    22, #SSH
    23, #Telnet
    25, #SMTP
    53, #DNS
    110, 143, #POP3 and IMAP (email retrieval protocols)
    3389, #RDP
    # High-Risk/Unusual Ports
    137, 138, 139, 445, #NetBIOS and SMB (file sharing)
    161, 162, #SNMP 
    1433, 1434 #SQL Server
}

# Detect port scanning - single source IP accessing many ports
def detect_port_scan(ip_src, tcp_dport):
    traffic_stats[ip_src][tcp_dport] += 1
    if len(traffic_stats[ip_src]) > alert_thresholds['port_scan']:
        alert_log.append(f'Port scanning detected from {ip_src}')
        print(f'Alert: Port scanning detected from {ip_src}')

# Detect high volume traffic (possible DoS/DDoS)
def detect_high_volume(ip_src):
    traffic_stats[ip_src]['packet_count'] += 1
    if traffic_stats[ip_src]['packet_count'] > alert_thresholds['high_volume']:
        alert_log.append(f'High volume traffic detected from {ip_src}')
        print(f'Alert: High volume traffic detected from {ip_src}')
    
# Packet processing callback
def packet_callback(packet, verbose):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst

        # Check for SYN (potential SYN flood DoS) and RST (unexpected resets) flags. 
        # Highlight activity on monitored ports.
        if TCP in packet: 
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport
            if tcp_dport in monitored_ports:
                detect_port_scan(ip_src, tcp_dport)
            if packet[TCP].flags == 'S':  # SYN packet
                print(f'SYN packet detected: {ip_src} -> {ip_dst}')
            elif packet[TCP].flags == 'R':  # RST packet
                print(f'RST packet detected: {ip_src} -> {ip_dst}')
            if verbose:
                print(f'IP {ip_src} -> {ip_dst} | TCP {tcp_sport} -> {tcp_dport}')

        # Detect high-volume traffic on monitored ports.
        elif UDP in packet: 
            udp_sport = packet[UDP].sport
            udp_dport = packet[UDP].dport
            if udp_dport in monitored_ports:
                if verbose:
                    print(f'IP {ip_src} -> {ip_dst} | UDP {udp_sport} -> {udp_dport}')

        # Log ICMP traffic to monitor for ping floods or reconnaissance.
        elif ICMP in packet: 
            if verbose:
                print(f'ICMP packet detected: {ip_src} -> {ip_dst}')

        # Monitor DNS queries and responses for unusual domain requests.
        elif DNS in packet:
            if packet[DNS].qr == 0:  # DNS query
                if verbose:
                    print(f'DNS query: {packet[DNS].qd.qname} from {ip_src}')
            else:  # DNS response
                if verbose:
                    print(f'DNS response: {packet[DNS].an.rrname} from {ip_src}')
        
        # Log ARP traffic to watch for spoofing attempts/
        elif ARP in packet:
            if verbose:
                print(f'ARP packet detected: {packet[ARP].psrc} -> {packet[ARP].pdst}')

        detect_high_volume(ip_src)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network Security Monitor')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    args = parser.parse_args()

    print('Starting packet capture...')
    try:
        # Filter to capture only specific types of packets
        sniff(filter="tcp or udp or icmp or arp or port 53 or port 80 or port 443", prn=lambda x: packet_callback(x, args.verbose), store=0)
    except KeyboardInterrupt:
        wrpcap('captured_packets.pcap', captured_packets)
        with open('alert_log.txt', 'w') as f:
            for alert in alert_log:
                f.write(f'{alert}\n')
        print('\nPackets saved to captured_packets.pcap')
        print('Alerts saved to alert_log.txt')