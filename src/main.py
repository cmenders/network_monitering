from scapy.all import sniff, TCP, IP

def packet_callback(packet):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        if TCP in packet:
            tcp_sport = packet[TCP].sport
            tcp_dport = packet[TCP].dport
            print(f'IP {ip_src} -> {ip_dst} | TCP {tcp_sport} -> {tcp_dport}')
        else:
            print(f'IP {ip_src} -> {ip_dst}')

if __name__ == '__main__':
    print('Starting packet capture...')
    sniff(prn=packet_callback, store=0)  # store=0 avoids storing packets in memory