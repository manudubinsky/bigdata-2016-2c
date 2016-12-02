import pymongo

from pymongo import MongoClient

client = MongoClient()

db = client.test

"""cursor = db.restaurants.find()

for document in cursor:
    print(document)

cursor = db.restaurants.find({"borough": "Manhattan"})

cursor = db.restaurants.find({"grades.score": {"$gt": 30}})

cursor = db.restaurants.find({"cuisine": "Italian", "address.zipcode": "10075"})

cursor = db.restaurants.find({"$or": [{"cuisine": "Italian"}, {"address.zipcode": "10075"}]})

cursor = db.restaurants.find().sort([("borough", pymongo.ASCENDING),("address.zipcode", pymongo.ASCENDING)])
"""

#BUSCAMOS EL USUARIO CON MAYOR CANTIDAD DE DOCUMENTOS SOBRE LA COLECCION QUE HICIMOS EN MONGO ("_id", "value")

cursor = db.map_reduce.find().sort([("value", pymongo.DESCENDING)])

#CURSOR[0] SERA EL USUARIO CON MAYOR DOCUMENTOS YA QUE ESTA ORDENADO
abc = cursor[0]['_id']
abc = abc.encode("utf-8")

print "Usuario: " , abc
print ("\n")

#SOBRE LA BASE ORIGINAL (TWEETS), TRAEMOS LOS DOCUMENTOS (TEXT) DE ESE USUARIO

cursor2 = db.tweets.find({"user.name":abc})

i = 1

for x in cursor2:
    print "Tweet numero: " , i
    print ("\n")
    print x['text']
    i += 1
