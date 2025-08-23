#!/usr/bin/env python3

import sys
import re
import argparse
import subprocess
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

CONFIG_PATHS = [
    Path.home() / ".config" / "ping-metrics" / "targets.json",
    Path("/etc/ping-metrics.json"),
]

def load_targets_from_config():
    for path in CONFIG_PATHS:
        if path.is_file():
            try:
                with open(path) as f:
                    data = json.load(f)
                targets = data.get("targets", [])
                if isinstance(targets, list) and targets:
                    return targets
            except Exception as e:
                print(f"Warning: failed to load config {path}: {e}", file=sys.stderr)
    # fallback default
    return ["google.com"]

def ping_once(host, count):
    result = subprocess.run(
        ['ping', '-n', '-c', str(count), '-w', '2', host],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    output = result.stdout

    loss_match = re.search(r'(\d+)% packet loss', output)
    lost = 0
    if loss_match:
        loss_percent = int(loss_match.group(1))
        lost = int(round(loss_percent / 100 * count))

    avg_match = re.search(r'=\s*[\d\.]+/([\d\.]+)/', output)
    if avg_match:
        avg = float(avg_match.group(1))
    else:
        avg = -1.0

    return host, lost, avg

def print_metrics(targets, output_file=None, count=2, max_workers=5):
    lines = []

    lines.append('# HELP icmp_lost Number of lost packets')
    lines.append('# TYPE icmp_lost gauge')

    lines.append('# HELP icmp_avg Average response time in ms')
    lines.append('# TYPE icmp_avg gauge')

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ping_once, target, count): target for target in targets}

        results = {}
        for future in as_completed(futures):
            host, lost, avg = future.result()
            results[host] = (lost, avg)

    for target in targets:
        lost, avg = results.get(target, (count, -1))
        lines.append(f'icmp_lost{{target="{target}"}} {lost}')
    for target in targets:
        _, avg = results.get(target, (count, -1))
        lines.append(f'icmp_avg{{target="{target}"}} {avg}')

    full_output = '\n'.join(lines)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(full_output + '\n')
    else:
        print(full_output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ping targets and output Prometheus-compatible metrics.")
    parser.add_argument("-c", "--count", type=int, default=2, help="Number of pings per target (default: 2)")
    parser.add_argument("-o", "--output", type=str, help="Optional output file for Prometheus metrics")
    parser.add_argument("-w", "--workers", type=int, default=5, help="Max parallel workers (default: 5)")
    parser.add_argument("targets", nargs="*", help="Ping targets list. Overrides config file if specified")

    args = parser.parse_args()

    targets = args.targets if args.targets else load_targets_from_config()

    print_metrics(targets, args.output, args.count, args.workers)
