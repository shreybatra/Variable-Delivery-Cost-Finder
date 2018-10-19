import pymongo
from pymongo import MongoClient
import areaFinder as af
import pickle

client = MongoClient()
db = client.minor
boys = db.boys
reqdb = db.reqdb
boys.delete_many({})
reqdb.delete_many({})
pickle.dump(af.createSearchTree(),open('tree.pickle','wb'))
