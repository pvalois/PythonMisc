#!/usr/bin/env python3 

import os,sys
from shlex import split,join
import shutil

for f in os.listdir("."): 
  words=split(f)
  ucf=[z.capitalize() for z in words]
  shutil.move(f,join(ucf))
  
  
