#!/usr/bin/env python3 

import psutil
import os
import time
import argparse
import curses

def get_filtered_processes(uid_only):
    current_uid = os.getuid()
    procs = []

    for p in psutil.process_iter(['pid', 'name', 'username']):
        try:
            if uid_only:
                if not hasattr(p, 'uids') or p.uids().real != current_uid:
                    continue
            p.cpu_percent(interval=None)  # amorçage
        except Exception:
            continue

    time.sleep(1)

    for p in psutil.process_iter(['pid', 'name', 'username']):
        try:
            if uid_only and p.uids().real != current_uid:
                continue
            cpu = p.cpu_percent(interval=None)
            procs.append((p.pid, p.info['name'], cpu))
        except Exception:
            continue

    return sorted(procs, key=lambda x: x[2], reverse=True)

def draw_interface(stdscr, uid_only):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(2000)

    while True:
        stdscr.erase()
        stdscr.addstr(0, 2, "🩺 Top Processus (triés par CPU %) — UID-only: {}".format(uid_only), curses.A_BOLD)

        procs = get_filtered_processes(uid_only)

        for idx, (pid, name, cpu) in enumerate(procs[:15]):
            stdscr.addstr(idx + 2, 2, f"{pid:>10}  {name[:25]:<25}  {cpu:>6.1f}%")

        stdscr.addstr(18, 2, "Appuie sur 'q' pour quitter.")

        key = stdscr.getch()
        if key == ord('q'):
            break

def main():
    parser = argparse.ArgumentParser(description="Diagnostic CPU en curses")
    parser.add_argument("--uid-only", action="store_true", help="Limiter aux processus de l'utilisateur courant")
    args = parser.parse_args()

    curses.wrapper(draw_interface, args.uid_only)

if __name__ == "__main__":
    main()

