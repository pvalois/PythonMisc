#!/usr/bin/env python3

import sys
import language_tool_python
from rich.console import Console
from rich.table import Table

console = Console()

def main(fichier):
    tool = language_tool_python.LanguageTool('fr')

    with open(fichier, 'r', encoding='utf-8') as f:
        text = f.read()

    matches = tool.check(text)

    if not matches:
        console.print(f"[green]Aucune erreur détectée dans '{fichier}'.[/green]")
        return

    table = Table(title=f"Vérification orthographique et grammaticale : {fichier}")
    table.add_column("Position", justify="right", style="cyan")
    table.add_column("Texte Erroné", style="yellow")
    table.add_column("Message", style="magenta")

    for match in matches:
        start = match.offset
        length = match.errorLength
        error_text = text[start:start+length]
        message = match.message

        table.add_row(str(start), error_text, message)

    console.print(table)

if __name__ == "__main__":
    for name in sys.argv[1:]:
        main(name)
