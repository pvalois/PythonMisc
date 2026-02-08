#!/usr/bin/env python3

import sys
from pathlib import Path
from colorama import init, Fore, Style
from tabulate import tabulate

init(autoreset=True)

def collect(directory):
    data = {}
    for path in Path(directory).rglob("*"):
        if path.is_file():
            stat = path.stat()
            rel_path = str(path.relative_to(directory))
            data[rel_path] = stat.st_size
    return data

def diff_view(src, dst):
    src_data = collect(src)
    dst_data = collect(dst)

    all_keys = sorted(set(src_data) | set(dst_data))

    table=[]
    for key in all_keys:
        src_meta = src_data.get(key)
        dst_meta = dst_data.get(key)

        left = key if src_meta else ""
        right = key if dst_meta else ""

        if src_meta and not dst_meta:
            _src = f"{Fore.RED+Style.BRIGHT}{left}"
            _sep = f"{Fore.RED+Style.BRIGHT}-"
            _dst = ""
        elif dst_meta and not src_meta:
            _src = ""
            _sep = f"{Fore.GREEN+Style.BRIGHT}+"
            _dst = f"{Fore.GREEN+Style.BRIGHT}{right}"
        elif left != right: 
            _src = f"{Fore.YELLOW+Style.BRIGHT}{left}"
            _sep = f"{Fore.YELLOW+Style.BRIGHT}≠"
            _dst = f"{Fore.YELLOW+Style.BRIGHT}{right}"
        elif len(left)>0 :
            _src = f"{Fore.WHITE+Style.BRIGHT}{left}"
            _sep = f"{Fore.WHITE+Style.BRIGHT}|"
            _dst= f"{Fore.WHITE+Style.BRIGHT}{right}"

        table.append([_src,_sep,_dst])

    view = tabulate(table,tablefmt="plain")
    print(view)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: tree_diff.py <src_dir> <dst_dir>")
        sys.exit(1)

    diff_view(sys.argv[1], sys.argv[2])

