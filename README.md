# Network Security Monitor

## Overview

A network monitoring tool that captures network packets and displays them on a real-time dashboard. This project uses Django for the backend, Channels for WebSocket support, and React for the frontend.

## Features

<!-- - **Packet Capturing:** Captures TCP, UDP, ICMP, DNS, HTTP/HTTPS, and ARP packets.
- **Traffic Analysis:** Detects port scanning, high volume traffic, and logs alerts.
- **Verbose Mode:** Option to print detailed information about all captured packets. -->
- Capture and display network packets in real-time
- Start and stop packet capture from the frontend
- Display a cumulative histogram of packet counts by destination port
- Display a timer that starts when packet capture begins

## Requirements

- Python 3.x
- Node.js 
- npm (Node Package Manager)

## Setup

### Backend (Django)

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

3. **Create and apply migrations:**
    ```bash
    python manage.py makemigrations monitor
    python manage.py migrate
    ```

4. **Start the Django server:**
    ```bash
    python manage.py runserver
    ```

### Frontend (React)

1. **Navigate to the frontend directory:**
    ```bash
    cd network-monitor-frontend
    ```

2. **Start the React development server:**
    ```bash
    npm start
    ```

## Usage

### Starting and Stopping Packet Capture:

#### Start Packet Capture:
- Navigate to the frontend in your browser (`http://localhost:3000).
- Click the "Start Capture" button to begin capturing packets.
- The packet capture will start, and the timer will display the elapsed time.

#### Stop Packet Capture:
- Click the "Stop Capture" button to stop capturing packets.
- The packet capture will stop, and the timer will freeze.

### Viewing Packets and Alerts

- The dashboard displays the latest captured packets and alerts.
- The histogram shows a cumulative count of packets by destination port.

### Endpoints

#### Start Capture
- URL: /api/start_capture/
- Method: GET
- Description: Starts the packet capture.

#### Stop Capture
- URL: /api/stop_capture/
- Method: GET
- Description: Stops the packet capture.

### Dependencies

#### Python Packages
- Django
- Django Channels
- Django REST Framework
- scapy

#### Node.js Packages
- react
- react-dom
- react-chartjs-2
- chart.js