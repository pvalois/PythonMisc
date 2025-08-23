#!/usr/bin/env python3 

import re
import sys
from optparse import OptionParser
from pathlib import Path

parser = OptionParser()
parser.add_option("-p", "--path-only", action="store_true", dest="path", default=False, help="Pour n'afficher que le path")
parser.add_option("-r", "--root-diry", dest="rootdir", help="Starting Directory", metavar="PATH")
parser.add_option("-c", "--command", dest="command", help="Commande à exécuter sur chaque résultat", metavar="CMD")
(options, args) = parser.parse_args()

pattern=args[0] if (len(args) > 0) else ".*"
rootdir = options.rootdir if (options.rootdir) else "."
action = options.command if (options.command) else "{}"
pattern_re = re.compile(pattern)

scandir = Path(rootdir)
seenpath = set()

for path in scandir.rglob("*"):
  if path.is_file() and pattern_re.match(path.name):
    if options.path:
      if path.parent not in seenpath:
        result = action.replace("{}", f'"{path.parent}"')
        print(result)
        seenpath.add(path.parent)
    else:
      result = action.replace("{}", f'"{path}"')
      print(result)

  
