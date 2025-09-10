#!/usr/bin/env python3

import psutil
import os
from collections import defaultdict
from rich.console import Console
from rich.table import Table,box

def list_listening_ports_grouped():
    conns = psutil.net_connections(kind="inet")
    conns = [c for c in conns if c.status == psutil.CONN_LISTEN]

    grouped = defaultdict(list)

    for conn in conns:
       laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
       pid = conn.pid
       pname = psutil.Process(conn.pid).name()
       grouped[(pid, pname)].append(laddr)
    return grouped

if __name__ == "__main__":
    grouped_ports = list_listening_ports_grouped()

    table = Table(box=box.MINIMAL)
    table.add_column("Ports", style="cyan")
    table.add_column("PID", style="magenta")
    table.add_column("Process", style="green")

    for (pid, pname), addrs in sorted(grouped_ports.items(), key=lambda x: x[0][1]):
        ports_str = "\n".join(sorted(addrs))+"\n"
        table.add_row(ports_str, str(pid), pname)

    console = Console()
    console.print(table)

    if (os.getuid()!=0):
      print ("Sans sudo, ces informations peuvent être incomplètes")

