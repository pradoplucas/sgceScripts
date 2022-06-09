import pymongo
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["certs"]

mycol_events = mydb["events"]
mycol_owners = mydb["owners"]

mycol_events.drop()
mycol_owners.drop()

events = json.loads(open('data/events.json').read())
owners = json.loads(open('data/owners.json').read())

mycol_events.insert_many(events)
mycol_owners.insert_many(owners)
