from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, auth
from pymongo import MongoClient
from dotenv import dotenv_values
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
    uid = decoded_token['uid']
    # upsert to the database with the user info
    # update the last login time
    return uid

@ app.get("/user/{uuid}")
def get_user(uuid: str):
    user = app.database.users.find_one({"uuid": uuid}, {'_id': 0})
    return user

@ app.get("/friends/{uuid}")
def get_friends(uuid: str):
    user = app.database.users.find_one({"uuid": uuid}, {'_id': 0})
    return list(map(get_user, user['friends']))



@ app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!!")

@ app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@ app.get("/")
