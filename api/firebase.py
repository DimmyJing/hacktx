from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, auth
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import dotenv_values
import datetime
# among us
config = dotenv_values(".env")
app = FastAPI()

cred = credentials.Certificate("./config/config.json")
firebase_admin.initialize_app(cred)


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

@ app.get("/{id_token}")
def verify_id(id_token: str):
    decoded_token = auth.verify_id_token(id_token)
    uuid = decoded_token['uid']
    return uuid

@ app.get("/user/{uuid}")
def get_user(uuid: str):
    user = app.database.users.find_one({"uuid": uuid}, {'_id': 0})
    return user

@ app.get("/friends/{uuid}")
def get_friends(uuid: str):
    user = app.database.users.find_one({"uuid": uuid}, {'_id': 0})
    return list(map(get_user, user['friends']))

class FriendsPostReq(BaseModel):
    uuid: str
    friendUuid: str

@ app.post("/friends/add")
def add_friend(req: FriendsPostReq):
    user = app.database.users.find_one({"uuid": req.uuid}, {'_id': 0})
    if req.friendUuid in user['friends']:
        return 0
    result = app.database.users.update_one({"uuid": req.uuid}, {"$push": {"friends": req.friendUuid}})
    return result.modified_count

@ app.post("/friends/remove")
def remove_friend(req: FriendsPostReq):
    result = app.database.users.update_one({"uuid": req.uuid}, {"$pull": {"friends": req.friendUuid}})
    return result.modified_count

# ============================

class Message(BaseModel):
    uuid_one: str
    uuid_two: str
    message: str

# uuid1 to uuid2
@ app.post("/send_message")
def post_chat(message: Message):
    
    uuid1 = message.uuid_one
    temp1, temp2 = sorted([message.uuid_one, message.uuid_two])
    message = message.message

    # from uuid1 to uuid2
    now = datetime.datetime.now()
    app.database.chats.update_one({"uuid1": temp1, "uuid2": temp2}, {"$push": {"log": [str(now), uuid1 == temp1, message]}}, upsert=True)
    return message

@ app.get("/get_chat/{uuid1}/{uuid2}")
def get_chat(uuid1: str, uuid2: str):
    temp1, temp2 = sorted([uuid1, uuid2])
    chat = app.database.chats.find_one({"uuid1": temp1, "uuid2": temp2}, {'_id': 0})
    if uuid1 != temp1:
        chat['log'] = list(map(lambda x: [x[0], not x[1], x[2]], chat['log']))
    return chat['log'] if chat else []
