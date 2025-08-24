#!/usr/bin/env python3 

from pathlib import Path
import os, sys, re
import shutil
import uuid
import getopt 

import argparse
parser = argparse.ArgumentParser(description="Group files by prefix")

parser.add_argument('-d', '--device', type=str, default='primdev', help='Nom du device')
parser.add_argument( '-m', '--min', type=int, default=1, help='Taille minimale du préfixe')
parser.add_argument( '-M', '--max', type=int, default=9999, help='Taille maximale du préfixe')
parser.add_argument( '-N', '--numeric', action='store_true', default=False, help='Caractères numériques autorisés')
parser.add_argument( '-s', '--space', action='store_true', default=False, help='Espace autorisé')
parser.add_argument( '-X', '--extend', type=str, default='', help='Caractères additionnels permis')
parser.add_argument( '-n', '--dry-run', action='store_true', default=False, help='Dry run')
parser.add_argument('names', nargs='*', help="Liste de noms à traiter")

args=parser.parse_args()

p=Path('.')

alphabetic="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeric="0123456789"
space=" "

pattern=alphabetic

dry=args.dry_run
min_len = args.min
max_len = args.max
if (args.numeric):  pattern=pattern+numeric
if (args.space): pattern=pattern+space
pattern=pattern+args.extend

if (dry): print ("++ DRY RUN")

liste=[]
candidates=[]

def clean_prefix(prefix, allowed_chars=alphabetic):
  i=0
  while (i<len(prefix) and prefix[i] in allowed_chars): 
    i+=1
  return prefix[:i]

for filename in p.iterdir():

  if filename.is_dir(): 
    liste.append(str(filename))
    continue;

  fn=str(filename)
  L=len(fn)

  for x in range(min_len, min(max_len, L) + 1):
    raw = fn[0:x]
    cleaned = clean_prefix(raw, pattern).strip()
    if (cleaned==fn): continue
    if (cleaned in liste): continue
    if (cleaned): liste.append(cleaned)
   
  candidates.append(fn)

cases=sorted(liste,reverse=True)

for case in cases:
  compliants=[x for x in candidates if x.startswith(case)]
  if (len(compliants)>1):
    candidates=[x for x in candidates if x not in compliants]

    temp_name = '.tmp_sort_'+str(uuid.uuid4())[:8]
    temp_path = Path(temp_name)
    if (not dry): temp_path.mkdir(exist_ok=False)

    for file in compliants:
      print (f"{file} -> [{case}]")
      if (not dry): shutil.move(file, temp_path)

    if (not dry): os.rename(temp_path,case)

