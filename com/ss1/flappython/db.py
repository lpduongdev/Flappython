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


def save_result(score, username, level):
    username = username.lower()
    print(score, username, level)
    if score >= 0 and username:
        user = db['users'].find_one({'username_text': username})
        db['users'].update_one({'username_text': username}, {
            '$set': {
                level: score if user[level] < score else user[level],
                'count': user['count']+1
            }
        })    
        return True
    else:
        print("Invalid")
        return False

def get_top_five_easy():
    top_five = db['users'].find({}).sort({'easy_score': -1}).limit(5)
    return top_five

def get_top_five_medium():
    top_five = db['users'].find({}).sort({'medium_score': -1}).limit(5)
    return top_five

def get_top_five_hard():
    top_five = db['users'].find({}).sort({'hard_score': -1}).limit(5)
    return top_five

export = score_collection
