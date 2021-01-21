from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
client = MongoClient({os.getenv('MONGO_URI')})
db = client.get_database('people')
collection = db.users
CORS(app)


@app.route('/getusers', methods=['GET'])
def getUsers():
    usersList = []
    for user in collection.find():
        user['_id'] = str(user['_id'])
        usersList.append(user)
    return jsonify(usersList)


@app.route('/getuser/<id>', methods=['GET'])
def getUser(id):
    user = collection.find_one({'_id': ObjectId(id)})
    user['_id'] = str(user['_id'])
    print(user)
    return jsonify(user)


@app.route('/deleteuser/<id>', methods=['DELETE'])
def deleteUser(id):
    query = {'_id': id}
    collection.delete_one({'_id': ObjectId(id)})
    return "user deleted"


@app.route('/edituser/<id>', methods=['PUT'])
def updateUsers(id):
    print(id)
    print(request.json)
    collection.update_one({'_id': ObjectId(id)}, {'$set': request.json})
    return "user updated"


@app.route('/users', methods=['POST'])
def createUser():
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        collection.insert_one({
            "username": username,
            "password": hashed_password,
            "email": email,
        })
        return 'user created'


if __name__ == '__main__':
    app.run(debug=True)
