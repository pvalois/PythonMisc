#!/usr/bin/env python3 

from pathlib import Path
import os, sys, re
import shutil
import uuid
import getopt 

p=Path('.')

# Default settings 
min_len=1
max_len=999
dry=False

alphabetic="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeric="0123456789"
space=" "

pattern=alphabetic

# Option parsing 
try:
  opts, args = getopt.getopt(sys.argv[1:], "mMNsX:n", ["min=", "max=", "numeric", "space", "extend=", "dry"])
except getopt.GetoptError:
  myname = os.path.basename(sys.argv[0])
  print(f'{myname}', end=' ')
  print('[-m/--min N] [-M/--max N]', end=' ')
  print('[-N/--numeric] [-s/--space] [-S/--special] [-X/extend <string>]', end=' ')
  print('[-n/--dry]')
  sys.exit(2)

for opt, arg in opts:
  if opt in ("-m", "--min"): min_len = int(arg)
  if opt in ("-M", "--max"): max_len = int(arg)
  if opt in ("-N", "--numerie"): pattern=pattern+numeric
  if opt in ("-s", "--space"): pattern=pattern+space
  if opt in ("-X", "--extend"): pattern=pattern+arg
  if opt in ("-n", "--dry"): 
    print ("++ DRY RUN")
    dry = True

# Initialisation of lists
liste=[]
candidates=[]

# Function to cut at first forbidden character
def clean_prefix(prefix, allowed_chars=alphabetic):
  i=0
  while (i<len(prefix) and prefix[i] in allowed_chars): 
    i+=1
  return prefix[:i]

# Collecting filenames and builting list of all possible prefixes
for filename in p.iterdir():

  if filename.is_dir(): 
    liste.append(str(filename))
    continue;

  fn=str(filename)
  L=len(fn)

  for x in range(min_len, min(max_len, L) + 1):
    raw = fn[0:x]
    cleaned = clean_prefix(raw, pattern)
    if (cleaned): liste.append(cleaned.strip())
   
  candidates.append(fn)

# Searching for each prefixes files matching
cases=sorted(liste,reverse=True)
for case in cases:
  compliants=[x for x in candidates if x.startswith(case)]
  if (len(compliants)>1):
    candidates=[x for x in candidates if x not in compliants]

    # Creating directory, and moving files
    temp_name = '.tmp_sort_'+str(uuid.uuid4())[:8]
    temp_path = Path(temp_name)
    if (not dry): temp_path.mkdir(exist_ok=False)

    for file in compliants:
      print (f"{file} -> [{case}]")
      if (not dry): shutil.move(file, temp_path)

    if (not dry): os.rename(temp_path,case)

