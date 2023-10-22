from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, auth
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import dotenv_values
import datetime
from bson.objectid import ObjectId

# among us
config = dotenv_values(".env")
app = FastAPI()

cred = credentials.Certificate("./config/config.json")
firebase_admin.initialize_app(cred)

def verify_id(id_token: str):
    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token['uid']
    return uid

@ app.get("/")
def read_root():
    return {"Hello": "WBG wins"}

@ app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!!")

@ app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

class CreateUserPostReq(BaseModel):
    uid: str
    name: str
    email: str
    avatar: str

@ app.post("/create-user")
def create_user(req: CreateUserPostReq):
    app.database.users.insert_one({
        "uid": req.uid,
        "lastLogin": datetime.datetime.now(),
        "name": req.name,
        "email": req.email,
        "avatar": req.avatar,
        "friends": []
    })
    return 1

def get_contributor(id: str):
    contributor = app.database.contributors.find_one({"_id": ObjectId(id)}, {'_id': 0})
    user = get_user(contributor['uid'])
    contributor['name'] = user['name']
    contributor['avatar'] = user['avatar']
    return contributor

def populate_contributors(building):
    building['contributors'] = list(map(get_contributor, building['contributors']))
    return building

@ app.get("/buildings")
def get_buildings():
    buildings = app.database.buildings.find({}, {'_id': 0})
    buildings = list(map(populate_contributors, buildings))
    return buildings

# @ app.get("/building/{id}")
# def get_building(id: str):
#     building = app.database.buildings.find_one({"_id": ObjectId(id)}, {'_id': 0})
#     building = populate_contributors(building)
#     return building

@ app.get("/user/{uid}")
def get_user(uid: str):
    user = app.database.users.find_one({"uid": uid}, {'_id': 0})
    return user

@ app.get("/friends/{token}")
def get_friends(token: str):
    uid = verify_id(token)
    user = app.database.users.find_one({"uid": uid}, {'_id': 0})
    return list(map(get_user, user['friends']))

class FriendsPostReq(BaseModel):
    token: str
    friendUid: str

@ app.post("/friends/add")
def add_friend(req: FriendsPostReq):
    uid = verify_id(req.token)
    user = app.database.users.find_one({"uid": uid}, {'_id': 0})
    if req.friendUid in user['friends']:
        return 0
    result = app.database.users.update_one({"uid": uid}, {"$push": {"friends": req.friendUid}})
    return result.modified_count

@ app.post("/friends/remove")
def remove_friend(req: FriendsPostReq):
    uid = verify_id(req.token)
    result = app.database.users.update_one({"uid": uid}, {"$pull": {"friends": req.friendUid}})
    return result.modified_count

# ============================

class Message(BaseModel):
    token1: str
    uid2: str
    message: str

# uid1 to uid2
@ app.post("/send_message")
def post_chat(message: Message):
    uid1 = verify_id(message.token1)
    temp1, temp2 = sorted([verify_id(message.token1), message.uid2])
    message = message.message

    # from uid1 to uid2
    now = datetime.datetime.now()
    app.database.chats.update_one({"uid1": temp1, "uid2": temp2}, {"$push": {"log": [str(now), uid1 == temp1, message]}}, upsert=True)
    return message

@ app.get("/get_chat/{token1}/{uid2}")
def get_chat(token1: str, uid2: str):
    uid1 = verify_id(token1)
    temp1, temp2 = sorted([verify_id(token1), uid2])
    print(temp1 + 'temp1')
    print(temp2 + 'temp2')
    chat = app.database.chats.find_one({"uid1": temp1, "uid2": temp2}, {'_id': 0})
    print(chat)
    if uid1 != temp1:
        chat['log'] = list(map(lambda x: [x[0], not x[1], x[2]], chat['log']))
    return chat['log'] if chat else []

