from flask_wtf import FlaskForm
from wtforms import StringField, NumberField, SubmitField,TextAreaField, SelectField
from wtforms.validators import DataRequired


class RatingForm(FlaskForm):
    rid = SelectField('Rid', choices=[], coerce=int)
    uid = SelectField('Uid', choices=[], coerce=int)
    comment = TextAreaField('Comment', validators=[DataRequired()])
    date_post = StringField('Date_post', validators=[DataRequired()])
    stars = NumberField('Stars', validators=[DataRequired()])
    submit = SubmitField('Search')
    




