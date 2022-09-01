from flask_wtf import FlaskForm 
from wtforms import FloatField
from wtforms.validators import DataRequired, Optional

class Form(FlaskForm):
	hours = FloatField(validators=[DataRequired()])
	minutes = FloatField(validators=[DataRequired()])
	five = FloatField(label='0-5', validators=[Optional()])
	ten = FloatField(label='5-10', validators=[Optional()])
	fifteen = FloatField(label='10-15', validators=[Optional()])
	twenty = FloatField(label='15-20', validators=[Optional()])
	half = FloatField(label='20-H', validators=[Optional()])
	twentyfive = FloatField(label='H-25', validators=[Optional()])
	thirty = FloatField(label='25-30', validators=[Optional()])
	thirtyfive = FloatField(label='30-35', validators=[Optional()])
	fourty = FloatField(label='35-40', validators=[Optional()])
	full = FloatField(label='40-F', validators=[Optional()])
