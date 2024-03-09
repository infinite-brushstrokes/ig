from flask import Flask
import pymongo
import os


app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = pymongo.MongoClient(mongo_uri)
db = client['ig']
collection = db['imageIds']

@app.route('/')
def hello_world():
    return f'{mongo_uri}'

@app.route('/add/<id>')
def add_data(id, caption):
    data = {'id': id, 'caption': "#abstractart"}
    collection.insert_one(data)
    return jsonify({'id': id, 'caption': caption})

@app.route('/add/<id>/<caption>')
def add_data_caption(id, caption):
    data = {'id': id, 'caption': caption }
    collection.insert_one(data)
    return jsonify({'id': id, 'caption': caption})
