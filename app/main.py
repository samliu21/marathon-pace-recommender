import os

from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for
import numpy as np

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
		fields = ['five', 'ten', 'fifteen', 'twenty', 'half', 'twentyfive', 'thirty', 'thirtyfive', 'fourty', 'full']

		has_elevation = all(request.form.get(x) for x in fields)
		if has_elevation:
			elevation = [request.form[x] for x in fields]
			print('Elevation obtained...')
		
		try:
			data = [float(request.form['hours']) * 60 + float(request.form['minutes'])]

			if has_elevation:
				elevation = list(map(int, elevation))
		except:
			print('Input is not integer...')
			return render_template('index.html', form=form)	

		paces = predict(data=data, elevation=(elevation if has_elevation else None))
		paces_str = ','.join(list(map(str, list(paces[0][0])))) + ';' + ','.join(list(map(str, list(paces[1][0]))))

		return redirect(url_for('pace', paces=paces_str))

	return render_template('index.html', form=form)

@app.route('/pace/<paces>')
def pace(paces):
	hrs, mins = paces.split(';')
	hrs = hrs.split(',')
	mins = mins.split(',')

	paces_t = [hrs[i] + ':' + (mins[i] if len(mins[i]) == 2 else '0' + mins[i]) for i in range(10)]

	return render_template(
		'pace.html', 
		paces=paces_t, 
		names=['5k', '10k', '15k', '20k', 'Half', '25k', '30k', '35k', '40k', 'Full',],
	)