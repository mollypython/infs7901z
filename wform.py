from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, SelectField
from wtforms.validators import DataRequired


class WishlistForm(FlaskForm): 
    uid = SelectField('Uid', choices=[], coerce=int)
    wishid = StringField('Wishid', validators=[DataRequired()])
    submit = SubmitField('Check')




