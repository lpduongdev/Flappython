import pymongo
from datetime import datetime

db = pymongo.MongoClient()["flappy-thon"]
score_collection = {}


def login(username, password):
    username = username.lower()
    if username and password:
        filter = {'username_text': username}
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
    username = username.lower()
    filter = {'username_text': username}
    if db['users'].find_one(filter):
        return False
    user_info = {"username_text": username,
                 'password': password,
                 'easy_score': 0,
                 'medium_score': 0,
                 'hard_score': 0,
                 'attempts': 0}
    db['users'].insert_one(user_info)
    return True


def save_result(score, username):
    username = username.lower()
    if score >= 0 and username:
        user = db['users'].find_one({'username_text': username})
        db['attempts'].insert_one({'username_text': username, 'score': score, 'created_at': datetime.now()})
        if user['highscore'] < score:
            db['users'].update_one({'username_text': username}, {
                '$set': {
                    'highscore': score
                }
            })
        return True
    else:
        print("Invalid")
        return False


export = score_collection
