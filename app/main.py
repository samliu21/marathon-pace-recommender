import sys

from flask import Flask 

from app.predict import predict

app = Flask(__name__)

@app.route('/')
def index():
	print(predict([180.]))
	return 'Hello, world!'