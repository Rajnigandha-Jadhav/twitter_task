from database.database import user

def insert(request_data):
    user.insert_one(request_data)

def insertMany(request_data):
    user.insert_many(request_data)

def update(request_data):
    user.update_one(request_data)

def delete(request_data):
    user.delete_one(request_data)

def get(request_data):
    user.find_one(request_data)

def getAll(request_data):
    user.find(request_data)
