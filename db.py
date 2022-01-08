import hashlib
import random
import string

import pymongo

username = 'max'
password = 'iloveyou>'
database_name = 'myFirstDatabase'
url = 'mongodb+srv://' + username + ':' + password + '@cluster0.pntcp.mongodb.net/' + database_name + '?retryWrites=true&w=majority'
db = pymongo.MongoClient(url).get_database("flappy_thon")
score_collection = {}


def login(username, password):
    username = username.lower()
    if username == 'guest':
        return False
    if username and password:
        user = db['users'].find_one({'username_text': username})
        if not user:
            return False
        if user['password'] == password:
            return True
        else:
            return False
    else:
        return False


def signup(username, password):
    username = username.lower()
    if username == 'guest':
        return False
    if db['users'].find_one({'username_text': username}):
        return False
    user_info = {"username_text": username,
                 'password': password,
                 'easy_score': 0,
                 'medium_score': 0,
                 'hard_score': 0,
                 'count': 0}
    db['users'].insert_one(user_info)
    return True


def save_result(score, username, level):
    username = username.lower()
    if score >= 0 and username:
        user = db['users'].find_one({'username_text': username})
        db['users'].update_one({'username_text': username}, {
            '$set': {
                level: score if user[level] < score else user[level],
                'count': user['count'] + 1
            }
        })
        return True
    else:
        print("Invalid")
        return False


def reset_password(username):
    username = username.lower()
    new_pass = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
    x = random.randint(0, len(new_pass))
    new_pass = new_pass[0:x] + '$' + new_pass[x:]
    hashed_password = hashlib.sha256(new_pass.encode('utf-8')).hexdigest()
    hashed_password = hashed_password[0:7] + '1ae5' + hashed_password[7:12] + '3ee1' + hashed_password[10:] + 'aHV5'
    if username:
        db['users'].find_one({'username_text': username})
        db['users'].update_one({'username_text': username}, {
            '$set': {
                'password': hashed_password
            }
        })
        return new_pass
    else:
        return -1


def get_top_five_easy():
    top_five = db['users'].find({}).sort('easy_score', -1).limit(5)
    result = list()
    for x in top_five:
        result.append({'name': x['username_text'] + "  [" + str(x['count']) + 'times' + "]",
                       'point': str(x['easy_score'])
                       })
    return result


def get_top_five_medium():
    top_five = db['users'].find({}).sort('medium_score', -1).limit(5)
    result = list()
    for x in top_five:
        result.append({'name': x['username_text'] + "  [" + str(x['count']) + 'times' + "]",
                       'point': str(x['medium_score'])
                       })
    return result


def get_top_five_hard():
    top_five = db['users'].find({}).sort('hard_score', -1).limit(5)
    result = list()
    for x in top_five:
        result.append({'name': x['username_text'] + "  [" + str(x['count']) + 'times' + "]",
                       'point': str(x['hard_score'])
                       })
    return result


def get_score(username):
    username = username.lower()
    user = db['users'].find_one({'username_text': username})
    return user['easy_score'], user['medium_score'], user['hard_score'], user['count']


export = score_collection
