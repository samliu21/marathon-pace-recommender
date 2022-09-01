from flask import Flask, render_template

from app.predict import predict

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')