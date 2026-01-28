#!/usr/bin/env python3 

import os
import sys
from fnmatch import fnmatch
import argparse

parser = argparse.ArgumentParser(description="Gestion des toggles")
parser.add_argument('-s', '--start', default=".", help='Liste de dossiers à scanner, séparés par des virgules')
parser.add_argument('-x', '--exclude', default="", help='Liste de dossiers à ignorer, séparés par des virgules')
parser.add_argument('-m', '--min', type=int, default=0, help='Print only entries with this minimum of files')
parser.add_argument('-M', '--max', type=int, default=10000000, help='Print only entries with this maximum of files')
parser.add_argument('-D', '--countdirs', default=False, action='store_true', help='Compte aussi les dossiers')
parser.add_argument('-S', '--short', default=False, action='store_true', help='Calcul simple sans total final')

args = parser.parse_args()

countdir=args.countdirs
starters=args.start.split(",")
exclude=args.exclude.split(",")

def not_in_list(excludelist, path):
  segments=path.split("/")
  for x in segments: 
    for pattern in excludelist: 
      if (fnmatch(x,pattern)): return (False)
  return (True)

def help():
  print (f"{sys.argv[0]} [-h] [-d] [-x pattern][paths]")
  print ("-h : this help")
  print ("-d : directory count only")
  print ("-x : pattern to exclude")
  print ("paths : space separated list of path to examine")
  sys.exit(0)

a={}

for start in starters: 
  for root,dirs,files in os.walk(start):
    gd=[x for x in dirs if not_in_list(exclude,x)] 
    gf=[x for x in files if not_in_list(exclude,x)]

    if (countdir): a[start]=len(gd)
    else: a[start]=len(gf)

    for dirp in dirs: 
      if (dirp==exclude): continue

      l=0
      d=0

      fullpath=os.path.join(start,dirp)
      for r1,d2,f2 in os.walk(fullpath):
        gd2=[x for x in d2 if not_in_list(exclude,x)] 
        gf2=[x for x in f2 if not_in_list(exclude,x)]
        d+=len(gd2)
        l+=len(gf2)

      if (countdir): a[fullpath]=d
      else: a[fullpath]=l
    break

total=0
for dirp in sorted(a):
  length=a[dirp]
  if (length>=args.min and length<=args.max):
    print (f'{length:10} | {dirp}')
  total+=length

if (not args.short): 
  print ("")
  print (f'{total:10} | total')
