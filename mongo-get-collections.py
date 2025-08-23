#!/usr/bin/env python3 

import pymongo
from pprint import pprint
import configparser
import os

config=configparser.ConfigParser()
config.read(os.path.expanduser('~/.mongodb.ini'))
ctx=config['kubedb1']

if 'username' in ctx : 
  client = pymongo.MongoClient(host=ctx['hostname'], port=int(ctx['port']), username=ctx['username'], password=ctx['password'], maxPoolSize=50)
else:
  client = pymongo.MongoClient(host=ctx['hostname'], port=int(ctx['port']), maxPoolSize=50)

print (client)
                                
try: 
  for db in client.list_database_names():
    print ("")
    print ("####",db)
    for coll in client[db].list_collection_names():
      print ("    ",coll)
except Exception as e: 
    print (f'{e}')


