#!/usr/bin/env python3

import sys
import re

# Expression régulière pour les séquences ANSI (couleurs, etc.)
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def clean_ansi(input_stream):
    for line in input_stream:
        clean_line = ansi_escape.sub('', line)
        sys.stdout.write(clean_line)

if __name__ == "__main__":
    clean_ansi(sys.stdin)

