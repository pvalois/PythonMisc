#!/usr/bin/env python3
import sys
import zipfile
import re
from rich.table import Table, box
from rich.console import Console

TAG_RE = re.compile(r"<[^>]+>")

def strip_tags(text):
  return TAG_RE.sub("", text)

def search_in_epub(epub_file, search_term):
  try:
    z = zipfile.ZipFile(epub_file, 'r')
    files = [n for n in z.namelist() if n.endswith(('.html', '.xhtml', '.xml', '.txt', '.htm'))]
    for name in files:
      with z.open(name) as f:
        for i, line in enumerate(f, 1):
          line_decoded = line.decode("utf-8", errors="ignore")
          line_clean = strip_tags(line_decoded)
          if search_term.lower() in line_clean.lower(): yield(epub_file,name,i,line_clean.strip())
  except:
    pass

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} MOT epub1.epub [epub2.epub ...]")
    sys.exit(1)

  occurs=[]
  search_term = sys.argv[1]
  for epub in sys.argv[2:]:
    occurs+=list(search_in_epub(epub, search_term))

  table=Table(box=box.MINIMAL_HEAVY_HEAD,show_lines=True)
  table.add_column("Filename")
  table.add_column("Path")
  table.add_column("Line")
  table.add_column("Content")
 
  for epub,filename,line,content in occurs:
    table.add_row(epub,filename,str(line),content)

  console=Console()
  console.print(table)


