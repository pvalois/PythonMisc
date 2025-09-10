#!/usr/bin/env python3

import sys
import os
import argparse

parser = argparse.ArgumentParser(description="Filename Rotate")
parser.add_argument('-r', '--reverse', default=False, action='store_true', help='Rotate in reverse order')
parser.add_argument('-n', '--dry-run', default=False, action='store_true', help='Dry-run')
parser.add_argument('remainder', nargs="*", action='store_true', help='Dry-run')
args = parser.parse_args()

if (len(args.remainder)==0): exit(0)

if (args.reverse): remainder=list(reversed(args.remainder))
tillers=zip(["loOooOoppeeeer"]+remainder,remainder+["loOooOoppeeeer"])

for a,b in tillers:
  if (not args.dry_run): os.rename(b,a)
  else: print ("mv \"%s\" \"%s\"" %(b,a))

