#!/usr/bin/env python3

from pathlib import Path
from colorama import init, Fore, Style
import sys

init(autoreset=True)

def collect(directory):
    data = {}
    for path in Path(directory).rglob("*"):
        if path.is_file():
            stat = path.stat()
            rel_path = str(path.relative_to(directory))
            data[rel_path] = (stat.st_size, stat.st_uid, stat.st_gid)
    return data

def diff_view(src, dst):
    src_data = collect(src)
    dst_data = collect(dst)

    all_keys = sorted(set(src_data) | set(dst_data))

    # Détermination de la largeur maximale pour l'alignement
    max_len = max((len(k) for k in all_keys), default=0)

    for key in all_keys:
        src_meta = src_data.get(key)
        dst_meta = dst_data.get(key)

        left = key if src_meta else ""
        right = key if dst_meta else ""

        if src_meta and not dst_meta:
            sep = f"{Fore.RED}-"
            print(f"{Fore.RED}{left.ljust(max_len)} {sep} ")
        elif dst_meta and not src_meta:
            sep = f"{Fore.GREEN}+"
            print(f"{' ' * max_len} {sep} {Fore.GREEN}{right}")
        elif src_meta != dst_meta:
            sep = f"{Fore.YELLOW}≠"
            print(f"{Fore.YELLOW}{left.ljust(max_len)} {sep} {right}")
        else:
            sep = f"{Fore.WHITE}|"
            print(f"{Fore.WHITE}{left.ljust(max_len)} {sep} {right}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: tree_diff.py <src_dir> <dst_dir>")
        sys.exit(1)
    diff_view(sys.argv[1], sys.argv[2])

