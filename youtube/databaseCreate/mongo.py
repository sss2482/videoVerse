import os
import pymongo
import json
import pprint

conn = pymongo.MongoClient('mongodb://localhost:27017')
# conn.admin.authenticate('admin','vodka')

db = conn.yt
coll = db.yt_videos
# coll=db.yt_video
file_names=[]
for file in os.listdir('test'):
    file_names.append(file)
for val in file_names:
    name='test/'+str(val)
    page = open(name,'r')
    parsed = json.loads(page.read())
    coll.insert_many([parsed])