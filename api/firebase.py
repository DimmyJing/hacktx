from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, auth
from pymongo import MongoClient
from dotenv import dotenv_values
from pydantic import BaseModel

# among us
config = dotenv_values(".env")
app = FastAPI()

cred = credentials.Certificate("./config/config.json")
firebase_admin.initialize_app(cred)


@ app.get("/")
def read_root():
    return {"Hello": "WBG wins"}


@ app.get("/{id_token}")
def verify_id(id_token: str):
    decoded_token = auth.verify_id_token(id_token)
    uuid = decoded_token['uid']
    # upsert to the database with the user info
    # update the last login time
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
    idToken: str
    friendUuid: str

@ app.post("/friends/add")
def add_friend(req: FriendsPostReq):
    uuid = verify_id(req.idToken)
    user = app.database.users.find_one({"uuid": uuid}, {'_id': 0})
    if req.friendUuid in user['friends']:
        return 0
    result = app.database.users.update_one({"uuid": uuid}, {"$push": {"friends": req.friendUuid}})
    return result.modified_count

@ app.post("/friends/remove")
def remove_friend(req: FriendsPostReq):
    uuid = verify_id(req.idToken)
    result = app.database.users.update_one({"uuid": uuid}, {"$pull": {"friends": req.friendUuid}})
    return result.modified_count

@ app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!!")

@ app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
