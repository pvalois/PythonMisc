#!/usr/bin/env python3
import psutil
import argparse
from collections import defaultdict
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()

def parse_args():
    parser = argparse.ArgumentParser(description="Lister connexions réseau avec PID et cmd")
    parser.add_argument('--sport', help='Ports locaux (comma-separated)')
    parser.add_argument('--dport', help='Ports distants (comma-separated)')
    parser.add_argument('-s', '--saddr', help='IP locales (comma-separated)')
    parser.add_argument('-d', '--daddr', help='IP distantes (comma-separated)')
    parser.add_argument('-p', '--pname', action='append', help='Process Name')
    parser.add_argument('-P', '--pid', action='append', help='Process pid')
    parser.add_argument('-x', '--xname', action='append', help='Excluded Process Name')
    parser.add_argument('-q', '--quiet', action='store_true', help='Ne pas afficher la commande')
    return parser.parse_args()

def matches_filter(value, filter_str):
    if not filter_str:
        return True
    terms = [term.strip() for term in filter_str.split(',') if term.strip()]
    return str(value) in terms

def main():
    args = parse_args()
    conns = psutil.net_connections(kind='inet')

    grouped = defaultdict(list)

    for conn in conns:
        if not conn.laddr:
            continue
        sport = str(conn.laddr[1])
        saddr = conn.laddr[0]
        dport = str(conn.raddr[1]) if conn.raddr else None
        daddr = conn.raddr[0] if conn.raddr else None

        if not matches_filter(sport, args.sport): continue
        if not matches_filter(dport, args.dport): continue
        if not matches_filter(saddr, args.saddr): continue
        if not matches_filter(daddr, args.daddr): continue

        pid = conn.pid
        cmd = ''
        if pid:
            try:
                p = psutil.Process(pid)
                cmd = ' '.join(p.cmdline())

                if args.pname and not any(p in cmd for p in args.pname): continue
                if args.pid and not any(int(p)==int(pid) for p in args.pid): continue
                if args.xname and any(x in cmd for x in args.xname): continue

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                cmd = ''

        grouped[pid].append({
            'saddr': saddr,
            'sport': sport,
            'daddr': daddr or '-',
            'dport': dport or '-',
            'cmd': cmd
        })

    for pid, entries in sorted((p, e) for p, e in grouped.items() if p is not None):
        cmd = entries[0]['cmd']

        if cmd and not args.quiet:
            console.rule("")
            print(f"[cyan]{pid}[/cyan] - [green]{cmd}[/green]")
            console.rule("")

        table = Table(show_header=False, box=None)
        table.add_column("Local Address", justify="right")
        table.add_column("Remote Address")

        for e in entries:
            local = f"{e['saddr']:>30}:{e['sport']}"
            remote = f"{e['daddr']}:{e['dport']}"
            table.add_row(local, " →   " + remote)

        console.print(table)
        print()

if __name__ == '__main__':
    main()

