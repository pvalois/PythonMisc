#!/usr/bin/env python3

import threading
import subprocess
import sys
import itertools
from colorama import init, Fore, Style

# Initialiser colorama
init()

# Liste de couleurs cycliques
colors = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
    Fore.MAGENTA, Fore.CYAN, Fore.WHITE
]

def ping_host(host, color):
    # Lancement de ping en mode continu (-O pour une sortie lisible sous Linux)
    proc = subprocess.Popen(
        ['ping', '-n', host],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Affichage ligne par ligne
    for line in proc.stdout:
        sys.stdout.write(color + f"[{host}] {line}" + Style.RESET_ALL)

def main():
    # Liste des hôtes à pinger
    hosts = sys.argv[1:]
    if not hosts:
        print("Utilisation : python ping_multi.py host1 host2 ...")
        sys.exit(1)

    # Démarrage d'un thread par hôte
    for host, color in zip(hosts, itertools.cycle(colors)):
        thread = threading.Thread(target=ping_host, args=(host, color), daemon=True)
        thread.start()

    # Boucle infinie, attend Ctrl+C
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nArrêt demandé. Ctrl+C reçu.")
        sys.exit(0)

if __name__ == "__main__":
    main()

