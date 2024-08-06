# Network Security Monitor

## Overview

This project captures and analyzes network packets to detect suspicious activities such as port scanning, high volume traffic (potential DoS/DDoS attacks), and other anomalies. It supports both verbose and non-verbose modes to either print all captured packets or only alerts.

## Features

- **Packet Capturing:** Captures TCP, UDP, ICMP, DNS, HTTP/HTTPS, and ARP packets.
- **Traffic Analysis:** Detects port scanning, high volume traffic, and logs alerts.
- **Verbose Mode:** Option to print detailed information about all captured packets.

## Requirements

- Python 3.x
- `scapy` library

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/cmenders/network_monitering
    cd network_monitering
    ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  
    pip install -r requirements.txt
    ```

## Usage

### Running the Packet Capture

To start capturing packets and analyzing traffic, run the `main.py` script. 

#### Normal Mode (Non-Verbose)

This mode prints only alerts:
```bash
python main.py
```

#### Verbose Mode

This mode prints all packets captured
```bash
python main.py -v
```

### Stopping the Packet Capture

To stop the packet capture, press `Ctrl+C`. Captured packets will be saved to `captured_packets.pcap` and alerts will be saved to `alert_log.txt`

