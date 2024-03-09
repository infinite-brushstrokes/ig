from flask import Flask, render_template, request, redirect, url_for, jsonify
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

@app.route('/delete/<id>')
def delete_data(id):
    data = collection.find_one({'id': id})
    if data:
        result = collection.delete_one({'id': id})
        if result.deleted_count == 1:
            return jsonify({ 'id' : data['id'], 'caption': data['caption']})
        else:
            return jsonify({})
    else:
        return jsonify({})

@app.route('/add/<id>')
def add_data(id):
    data = {'id': id, 'caption': "#abstractart"}
    collection.insert_one(data)
    return jsonify({'id': id, 'caption': "#abstractart" })

@app.route('/add/<id>/<caption>')
def add_data_caption(id, caption="#abstract"):
    data = {'id': id, 'caption': caption }
    collection.insert_one(data)
    return jsonify({'id': id, 'caption': caption})
