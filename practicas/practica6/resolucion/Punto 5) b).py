import pymongo

from pymongo import MongoClient

client = MongoClient()

db = client.test

cursor = db.tweets.find({"geo":{"$ne":None}},{"user.name":1, "coordinates":1})

for i in cursor:
    print "Nombre: ", i['user'], " | Coordenadas: ", i['coordinates']
    
