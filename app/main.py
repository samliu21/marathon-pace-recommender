import os

from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect

from app.forms.form import Form
from app.predict import predict

load_dotenv()
SECRET_KEY = os.environ['SECRET_KEY']

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=['GET', 'POST',])
def index():
	form = Form(request.form)

	if request.method == 'POST' and form.validate():
		return redirect('/pace')

	print(form.errors)
	return render_template('index.html', form=form)

@app.route('/pace')
def pace():
	return render_template('pace.html')