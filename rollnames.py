#!/usr/bin/env python3

import sys
import os
from getopt import *

try:
  opts, remainder = gnu_getopt(sys.argv[1:], "nr", ["dry-run","reverse"])
except GetoptError as err:
  print(err)
  print ("usage : %s (-n,--dryrun) (-r,--reverse))")
  sys.exit(2)

do_move=True
do_reverse=False

for opt, optarg in opts:
  if opt in ("-n","--dry-run"): do_move=False
  if opt in ("-r","--reverse"): do_reverse=True

if (len(remainder)==0): exit(0)

if (do_reverse): remainder=list(reversed(remainder))
tillers=zip(["loOooOoppeeeer"]+remainder,remainder+["loOooOoppeeeer"])

for a,b in tillers:
  if (do_move): os.rename(b,a)
  else: print ("mv \"%s\" \"%s\"" %(b,a))

