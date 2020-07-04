from pymongo import MongoClient
client = MongoClient(
    "mongodb+srv://naisir:mongo123@goodreads-user-zehuy.gcp.mongodb.net/goodreads?retryWrites=true&w=majority")
db = client["goodreads"]
user_collection = db["users"]
goodreads_coll = db["goodreads_user_obj"]
