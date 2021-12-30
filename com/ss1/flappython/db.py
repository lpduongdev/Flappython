import pymongo

db = pymongo.MongoClient()["flappy-thon"]
score_collection = {}


# data = {"score": 1, "username": "Tien Minh", "level": "hard"}
# x = score_collection.insert_one(data)

def login(username, password):
    if (username and password):
        filter = {'username': username}
        user = db['users'].find_one(filter)
        if not user:
            return False
        if (user['password'] == password):
            return True
        else:
            return False
    else:
        return False


def signup(username, password):
    filter = {'username': username}
    if db['users'].find_one(filter):
        return False
    user_info = {"username": username, 'password': password};
    db['users'].insert_one(user_info)
    return True


export = score_collection
