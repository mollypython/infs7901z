from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,SelectField
from wtforms.validators import DataRequired


class InspectionForm(FlaskForm):
    postid = SelectField('Postid', choices=[], coerce=int)
    inspectid = SelectField('Inpspectid', choices=[], coerce=int)
    date = StringField('Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    if_booked = BooleanField('Yes or Not')
    submit = SubmitField('Check')




