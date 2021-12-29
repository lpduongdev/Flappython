import pymongo

db = pymongo.MongoClient()["flappy-thon"]
score_collection = db['scores']
# data = {"score": 1, "username": "Tien Minh", "level": "hard"}
# x = score_collection.insert_one(data)

def hello():
    print("Hello Wolrd")

export = hello
export = score_collection
