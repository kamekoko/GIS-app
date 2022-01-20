from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def connect_to_mongodb():
    """ Connect to the MongoDB database server by pymongo """

    conn = None
    try:
        # params = config(section='mongodb')
        # conn = MongoClient(params['host'], int(params['port']))
        conn = MongoClient()
        conn.admin.command('ping')
    except:
        raise Exception('DB not found')

    return conn

def get_data_info(data_name):

    if data_name == "output":
        response = {"data_name": "output"}
    else:
        conn = connect_to_mongodb()
        db = conn.strage_info
        col = db.strage_info
        response = col.find_one({"data_name": data_name})

    return response
