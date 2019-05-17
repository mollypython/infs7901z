from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class BlogForm(FlaskForm):
    username = SelectField('Username', choices=[], coerce=int)
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class CarInfoForm(FlaskForm):
    username = SelectField('Username', choices=[], coerce=int)
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    carType = StringField('Car Type', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    manuYear = StringField('Manu Year', validators=[DataRequired()]) 
    specialist = SelectField('Specialist', choices=[], coerce=int)
    stars = StringField('Stars', choices=[], coerce=int)
    image = StringField('Image ID', validators=[DataRequired()]) 
    submit = SubmitField('Submit')

class RatingForm(FlaskForm):
    rid = SelectField('Rid', choices=[], coerce=int)
    uid = SelectField('Uid', choices=[], coerce=int)
    comment = TextAreaField('Comment', validators=[DataRequired()])
    date_post = StringField('Date_post', validators=[DataRequired()])
    stars = SelectField('Stars', validators=[DataRequired()])
    submit = SubmitField('Search')

   
class InspectionForm(FlaskForm):
    postid = SelectField('Postid', choices=[], coerce=int)
    inspectid = SelectField('Inpspectid', choices=[], coerce=int)
    date = StringField('Date', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    if_booked = BooleanField('Yes or Not')
    submit = SubmitField('Check')

class WishlistForm(FlaskForm): 
    uid = SelectField('Uid', choices=[], coerce=int)
    wishid = StringField('Wishid', validators=[DataRequired()])
    postid = SelectField('Postid', choices=[], coerce=int)
    submit = SubmitField('Check')

        
