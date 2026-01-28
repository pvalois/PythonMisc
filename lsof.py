#!/usr/bin/env python3

import argparse
import psutil
from colorama import Fore, init

init(autoreset=True)

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--processname', type=str, default="",
                    help='Filtre nom de processus (virgule séparé)')
parser.add_argument('-P', '--pid', type=str, default="",
                    help='Filtre PID (virgule séparé)')
parser.add_argument('-w', '--words', type=str, default="",
                    help='Filtre mots-clés dans les chemins (virgule séparé)')
parser.add_argument('-s', '--simple', action='store_true',
                    help='Sortie simplifiée')
args = parser.parse_args()

pid_filter = set(args.pid.split(',')) if args.pid else set()
name_filter = [n.lower() for n in args.processname.split(',') if n] if args.processname else []
word_filter = [w.lower() for w in args.words.split(',') if w] if args.words else []

simple_output = args.simple

def get_open_files():
    """Yield les processus avec fichiers ouverts, en ignorant ceux inaccessibles."""
    for _proc in psutil.process_iter(['pid', 'name']):
        try:
            files = sorted(_proc.open_files())
            if files:
                yield {
                    'pid': _proc.info['pid'],
                    'name': _proc.info['name'],
                    'files': files
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def apply_filters(procs):
    """Applique les filtres PID, nom et mots-clés."""

    for _proc in procs:

        if pid_filter and str(_proc['pid']) not in pid_filter:
            continue

        if name_filter and not any(n in (_proc['name'] or '').lower() for n in name_filter):
            continue

        if word_filter:
            matching_files = [
                f for f in _proc['files']
                if any(w in f.path.lower() for w in word_filter)
            ]

            if not matching_files:
                continue

            _proc['files'] = matching_files

        yield _proc

def print_proc(_proc):
    """Affiche un processus avec ses fichiers selon le mode simple ou décoré."""
    if not simple_output:
        print(f"{Fore.GREEN}{_proc['name']} / {Fore.YELLOW}{_proc['pid']}")

    for f in _proc['files']:
        if simple_output:
            print(f"{_proc['name']:15} {_proc['pid']:10}   {f.path.strip()}")
        else:
            print(f"  ⤷ {f.path.strip()} {Fore.CYAN}[{f.position}]")
    if not simple_output:
        print("")

if __name__ == "__main__":
    for _proc in apply_filters(get_open_files()):
        print_proc(_proc)

