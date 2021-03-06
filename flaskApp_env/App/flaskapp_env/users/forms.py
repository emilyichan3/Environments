from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, FormField
from wtforms.fields.core import IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskapp_env.modules_TIA import Member 

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                        validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                        validators=[DataRequired(), EqualTo('password')])
    country_code = SelectField('Nationality:', choices=[], validators=[DataRequired()], coerce=str)
    membership_type = SelectField('Membership Type:', choices=[], validators=[DataRequired()], coerce=int)
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        member = Member.query.filter_by(Name=username.data,Activate=1).first()
        if member:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        member = Member.query.filter_by(Email1=email.data,Activate=1).first()
        if member:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    memberid = StringField('Member ID', render_kw={'readonly': True} ,
                        validators=[DataRequired(), Length(min=8, max=20)])
    username = StringField('Name', 
                        validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField('Email', render_kw={'readonly': True} ,
                        validators=[DataRequired(), Email()])
    picture = FileField('Udate Profile Picture', validators=[FileAllowed(['jpg','png'])])
    country_code = SelectField('Nationality:', choices=[], validators=[DataRequired()], coerce=str)
    membership_type = SelectField('Membership Type:', choices=[], validators=[DataRequired()], coerce=int)
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.Name:
            member = Member.query.filter_by(Name=username.data).first()
            if member:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.Email1:
            member = Member.query.filter_by(Email1=email.data).first()
            if member:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        member = Member.query.filter_by(Email1=email.data).first()
        if member is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class AccountVerifiForm(FlaskForm):
    submit = SubmitField('Sumit Account Verification')

class UploadFileForm(FlaskForm):
    csvfile = FileField('Udate CSV File', validators=[FileAllowed(['csv'])])
    upload = SubmitField('Upload')

class UploadFileToDBForm(FlaskForm):
    submit = SubmitField('Uploading to DB')

class AdminForm(FlaskForm):
    submit = SubmitField('Sumit')

class MemberListForm(FlaskForm):
    submit = SubmitField('Sumit')

