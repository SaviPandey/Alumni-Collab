from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from firebase_admin import auth

from ait import db_fire
from ait.models import User

from datetime import date
class RegistrationForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        try:
            user = auth.get_user_by_email(email.data)
        except Exception as e:
            user = False
        
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

        if '@' in email.data:
            apsit = email.data.split('@')[1]
        else: 
            raise ValidationError('Enter valid email.')
        
        # if '_' not in email.data.split('@')[0] or len(email.data.split('@')[0].split('_')[1])!=5:
        #     raise ValidationError('Enter valid email.')

        if apsit != 'apsit.edu.in':
            raise ValidationError('Only @apsit.edu.in email address allowed.')
        
        
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    
    def validate_email(self, email):
        if '@' in email.data:
            apsit = email.data.split('@')[1]
        else: 
            raise ValidationError('Enter valid email.')
        
        # if '_' not in email.data.split('@')[0] or len(email.data.split('@')[0].split('_')[1])!=5:
        #     raise ValidationError('Enter valid email.')

        if apsit != 'apsit.edu.in':
            raise ValidationError('Only @apsit.edu.in email address allowed.')
        
    submit = SubmitField('Login')

class PasswordRestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    def validate_email(self, email):
        if '@' in email.data:
            apsit = email.data.split('@')[1]
        else: 
            raise ValidationError('Enter valid email.')
        
        # if '_' not in email.data.split('@')[0] or len(email.data.split('@')[0].split('_')[1])!=5:
        #     raise ValidationError('Enter valid email.')

        if apsit != 'apsit.edu.in':
            raise ValidationError('Only @apsit.edu.in email address allowed.')
    
    submit = SubmitField('Reset')
    
class EmailVerificationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    def validate_email(self, email):
        if '@' in email.data:
            apsit = email.data.split('@')[1]
        else: 
            raise ValidationError('Enter valid email.')
        

        if apsit != 'apsit.edu.in':
            raise ValidationError('Only @apsit.edu.in email address allowed.')
        
        # if '_' not in email.data.split('@')[0] or len(email.data.split('@')[0].split('_')[1])!=5:
        #     raise ValidationError('Enter valid email.')
        
    submit = SubmitField('Send')
    
class UpdateAccountForm(FlaskForm):
    name = StringField('Username')
    about = StringField('About')
    address = StringField('Address')
    phone = StringField('Phone')
    twitter = StringField('Twitter')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    linkedin = StringField('LinkedIn')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_phone(self, phone):
        if len(phone.data) != 10:
            raise ValidationError('Enter valid phone number.')
            
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    url = StringField('URL')
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Upload Media', validators=[FileAllowed(['jpg', 'png','mp4','jpeg','svg','webp'], 'Only media files are allowed.')])

    # New field for post type
    post_type = SelectField(
        'Post Type',
        choices=[('normal', 'Normal Post'), ('hiring', 'Hiring Post')],
        validators=[DataRequired()]
    )

    submit = SubmitField('Post')