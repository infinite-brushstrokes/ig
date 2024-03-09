from flask import Flask
import os

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")

@app.route('/')
def hello_world():
    return f'{mongo_uri}'
