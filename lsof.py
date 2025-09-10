#!/usr/bin/env python3

import psutil
import sys
import argparse 
from colorama import Fore, Back, Style, init

init(autoreset=True)

parser = argparse.ArgumentParser(description="Liste des fichiers ouverts")
parser.add_argument('-p', '--processname', type=str, default="", help='Process name filter, comma separated')
parser.add_argument('-P', '--pid', type=str, default="", help='Pid filter, comma separated')
parser.add_argument('-w', '--words', type=str, default="", help='Word filter, comma separated')
parser.add_argument('-s', '--simple', default=False, action='store_true', help='Output simplifié')
args = parser.parse_args()

pids=args.pid.split(",")
processname=args.processname.split(",")
words=args.words.split(",")
decorum=not args.simple

def opened_file_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            files = proc.open_files()
            if files:
                yield {
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'files': files
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def filter_by_name(proc_iter, name_list):
    """Yield only processes whose name matches any string in name_list."""
    for proc in proc_iter:
        if any(name.lower() in proc['name'].lower() for name in name_list):
            yield proc

def filter_by_pid(proc_iter, pid_list):
    """Yield only processes whose PID is in pid_list (as int or str)."""
    for proc in proc_iter:
        if str(proc['pid']) in pid_list or proc['pid'] in pid_list:
            yield proc

def filter_by_path_keywords(proc_iter, keywords):
    """Yield only processes with at least one file path matching keywords."""
    for proc in proc_iter:
        matching_files = [f for f in proc['files'] if any(word.lower() in f.path.lower() for word in keywords)]
        if matching_files:
            proc['files'] = matching_files
            yield proc

all_procs = opened_file_processes()
filtered = filter_by_name(all_procs, pids)
filtered = filter_by_name(filtered, processname)
filtered = filter_by_path_keywords(filtered, words)

for proc in filtered:

  if decorum:
    print(f"{Fore.GREEN}{proc['name']} / {Fore.YELLOW}{proc['pid']}")

  for f in proc['files']:
    if decorum:
      print(f"  ⤷ {f.path.strip()} {Fore.CYAN}[{f.position}]")
    else:
        print(f"{proc['name']:15} {proc['pid']:10}   {f.path.strip()}")

  if decorum: print ("")
