#!/usr/bin/env python3

from scapy.all import sniff, IP, TCP, UDP
import time
import threading
import os
from collections import defaultdict

if os.geteuid() != 0:
    print(f"Error: must use sudo")
    exit(1) 

interface = "eno1"
duration = 300  # 5 minutes

# Connexions : (src_ip, src_port, dst_ip, dst_port) => [bytes_sent, bytes_recv]
traffic = defaultdict(lambda: [0, 0])
lock = threading.Lock()

def clear():
   os.system('cls' if os.name == 'nt' else 'clear')

def format_bytes(bps):
    units = ['B/s', 'KB/s', 'MB/s']
    i = 0
    while bps >= 1024 and i < len(units) - 1:
        bps /= 1024.0
        i += 1
    return f"{bps:.2f} {units[i]}"

def packet_handler(pkt):
    if IP not in pkt:
        return

    proto = None
    sport = dport = None
    if TCP in pkt:
        proto = TCP
    elif UDP in pkt:
        proto = UDP
    else:
        return

    src = pkt[IP].src
    dst = pkt[IP].dst
    sport = pkt[proto].sport
    dport = pkt[proto].dport
    length = len(pkt)

    key_out = (src, sport, dst, dport)
    key_in = (dst, dport, src, sport)

    with lock:
        traffic[key_out][0] += length
        traffic[key_in][1] += 0  # ensure reverse key exists

def monitor():
    sniff(iface=interface, prn=packet_handler, store=0, timeout=duration)

def display():
    prev = {}
    for _ in range(duration):
        time.sleep(1)
        clear()
        print(f"{'Top 15 Active Connections on ' + interface:<45} {'Upload':>15} {'Download':>15}")
        print("-" * 80)

        rows = []

        with lock:
            for conn, (sent, recv) in traffic.items():
                prev_sent, prev_recv = prev.get(conn, [0, 0])
                delta_sent = sent - prev_sent
                delta_recv = recv - prev_recv
                prev[conn] = [sent, recv]

                total = delta_sent + delta_recv
                conn_str = f"{conn[0]}:{conn[1]} -> {conn[2]}:{conn[3]}"
                rows.append((total, conn_str, delta_sent, delta_recv))

        # Trier et limiter aux 15 plus gros débits
        top = sorted(rows, key=lambda x: x[0], reverse=True)[:15]

        for _, conn_str, delta_sent, delta_recv in top:
            print(f"{conn_str:<45} {format_bytes(delta_sent):>15} {format_bytes(delta_recv):>15}")

threading.Thread(target=monitor, daemon=True).start()
display()

