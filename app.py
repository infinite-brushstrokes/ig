from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymongo
import os
import time
import requests



# def cron():
#     time.sleep(600)
#     requests.get('https://ig-0shi.onrender.com/add/cron test')



app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
prodia_key = os.getenv("prodia_key")
client = pymongo.MongoClient(mongo_uri)
db = client['ig']
collection = db['imageIds']

@app.route('/')
def hello_world():
    return 'hello'

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

@app.route('/createigpost')
def create_ig_post():
    url = "https://api.prodia.com/v1/sdxl/generate"

    payload = {
        "model": "sd_xl_base_1.0.safetensors [be9edd61]",
        "prompt": "Create a vibrant and dynamic abstract art painting that embodies the essence of movement, emotion, and innovation. Utilize bold colors, fluid shapes, and unexpected textures to evoke a sense of wonder and intrigue. Let your imagination soar and explore the boundaries of creativity as you craft a masterpiece that captivates and inspires viewers",
        "negative_prompt": "lacks cohesion, creativity, and visual appeal. Emphasize dull colors, disjointed shapes, and uninspired compositions. Strive to create a piece that fails to evoke any emotional response or intrigue from the viewer. Avoid experimentation and instead rely on tired clichés and predictable motifs. Aim for a result that feels stagnant and devoid of any artistic merit or originality",
        "style_preset": "photographic",
        "steps": 50
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": prodia_key
    }

    response = requests.post(url, json=payload, headers=headers)

    jobId = json.loads(response.text)['job']


    data = {'id': jobId, 'caption': "#abstract" }
    collection.insert_one(data)
    return jsonify({'id': jobId, 'caption': "#abstract" })

# while True:
#     cron()
