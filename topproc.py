#!/usr/bin/env python3
import psutil
import time
import argparse
from rich.table import Table, box
from rich.console import Console

console = Console()

parser = argparse.ArgumentParser(description="Top processes CPU / RAM / I/O instantané")
parser.add_argument("--sort", choices=["cpu", "mem", "io"], default="cpu", help="Clé de tri pour le top")
parser.add_argument("--limit", type=int, default=10, help="Nombre de processus à afficher")
parser.add_argument("--interval", type=float, default=1.0, help="Intervalle de mesure pour CPU et I/O (s)")
args = parser.parse_args()

for p in psutil.process_iter():
    try:
        p.cpu_percent(None)
    except Exception:
        continue

io_start = {}
for p in psutil.process_iter():
    try:
        io = p.io_counters()
        if io:
            io_start[p.pid] = io
    except Exception:
        continue

time.sleep(args.interval)

rows = []
for p in psutil.process_iter(["pid", "name"]):
    try:
        cpu = p.cpu_percent(None)
        mem = p.memory_info().rss / 1024 / 1024  # MB

        # I/O delta
        io = 0.0
        io_counters = p.io_counters()
        start_counters = io_start.get(p.pid)
        if io_counters and start_counters:
            io = ((io_counters.read_bytes - start_counters.read_bytes) +
                  (io_counters.write_bytes - start_counters.write_bytes)) / 1024 / 1024 / args.interval

        rows.append((p.pid, p.info["name"], cpu, mem, io))
    except Exception:
        continue

key_map = {"cpu": 2, "mem": 3, "io": 4}
rows.sort(key=lambda r: r[key_map[args.sort]], reverse=True)
rows = rows[:args.limit]

table = Table(box=box.SIMPLE_HEAVY)

table.add_column("PID", style="bright_cyan", justify="right")
table.add_column("Process", style="bright_white", justify="left")
table.add_column("CPU %", style="bright_green", justify="right")
table.add_column("RAM MB", style="purple", justify="right")
table.add_column("I/O MB/s", style="bright_yellow", justify="right")

for r in rows:
    table.add_row(
        str(r[0]),
        f'{r[1][:25]:25}',
        f"{r[2]:.1f}",
        f"{r[3]:.0f}",
        f"{r[4]:.2f}",
    )

console.print(table)
