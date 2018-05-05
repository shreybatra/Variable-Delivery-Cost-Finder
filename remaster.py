import pymongo
from pymongo import MongoClient
import areaFinder as af
import pickle

client = MongoClient()
db = client.minor
boys = db.boys
reqdb = db.reqdb
boys.remove()
reqdb.remove()
pickle.dump(af.createSearchTree(),open('tree.pickle','wb'))