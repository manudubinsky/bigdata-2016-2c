import pymongo

from pymongo import MongoClient

client = MongoClient()

db = client.test

#ORDENAMOS LENGUAJES POR CANTIDAD

cursor = db.map_reduce.find().sort([("value", pymongo.DESCENDING)])

for i in cursor:
    print "Lenguaje: " , i['_id'], " | Cantidad: ", i['value']
