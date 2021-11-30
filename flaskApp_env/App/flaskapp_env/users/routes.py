import pandas as pd
import csv
from datetime import date
from flask import flash, redirect, render_template, url_for, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.datastructures import UpdateDictMixin
from flaskapp_env import  db, bcrypt
from flaskapp_env.users.utils_db import get_usable_data
from flaskapp_env.modules_TIA import (Member, Post, Country, Membership)
from flaskapp_env.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm
                        , RequestResetForm, ResetPasswordForm, AccountVerifiForm, UploadFileForm
                        , UploadFileToDBForm)
from flaskapp_env.users.utils import (save_picture, send_reset_email, send_account_verification
                        , upload_csv_file, parseCSV)

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    countries=db.session.query(Country).all()
    form.country_code.choices = [(i.CountryCode, i.CountryNameEN) for i in countries]  
    membership_type=db.session.query(Membership).all()
    form.membership_type.choices = [(i.ID, i.MembershipName) for i in membership_type]  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        _memberid, _period = get_usable_data(4)
        member = Member(Member_ID=_memberid,
                        Period=_period,
                        Name=form.username.data,
                        MainMemberId='',
                        MembershipType=form.membership_type.data,
                        Email1=form.email.data, 
                        Email2='',
                        Email3='',
                        Email4='',
                        Phone1='',
                        Phone2='',
                        Phone3='',
                        Phone4='',
                        Password=hashed_password, 
                        NationalCode=form.country_code.data, 
                        MembershipChangedPeriod='',
                        Comment='')
        user = Member.query.filter_by(Email1=form.email.data).first()
        if user is None:
            db.session.add(member)
            db.session.commit()
        
        #Send Account Verification
        user = Member.query.filter_by(Email1=form.email.data).first()
        send_account_verification(user)
        flash('An email has been sent with account verification to activate your account.', 'info')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        member = Member.query.filter_by(Email1=form.email.data,Activate=1).first()
        if member and bcrypt.check_password_hash(member.Password, form.password.data):
            login_user(member, remember=form.remember.data)
             #argus is dictionary
             #為了確保如果在link上面沒有next字樣，若使用key去尋找時會出錯
             #所以使用get來搜尋，找不到next時就會回傳null
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Pleach check email and password!','danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    countries=db.session.query(Country).all()
    membership_type=db.session.query(Membership).all()
    form = UpdateAccountForm()
    form.country_code.choices = [(i.CountryCode, i.CountryName) for i in countries]
    form.membership_type.choices = [(i.ID, i.MembershipName) for i in membership_type]  

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.Image_file = picture_file
        current_user.Member_ID = form.memberid.data
        current_user.Name = form.username.data
        current_user.Email1 = form.email.data
        current_user.NationalCode = form.country_code.data
        current_user.MembershipType = form.membership_type.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.Name
        # form.XXXX 指label，內容的話要.data
        form.memberid.data = current_user.Member_ID
        form.email.data = current_user.Email1
        form.country_code.data = current_user.NationalCode
        form.membership_type.data = current_user.MembershipType
    image_file = url_for('static', filename='profile_pics/' + current_user.Image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page',1, type=int)
    member = Member.query.filter_by(Name=username).first_or_404()
    posts = Post.query.filter_by(author=member)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page , per_page=5)
    return render_template('user_posts.html', posts=posts,user=member)

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Member.query.filter_by(Email1=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password',form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Member.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired link', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.Password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password',form=form)

@users.route('/activate_account/<token>', methods=['GET', 'POST'])
def activate_account(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Member.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired link', 'warning')
        return redirect(url_for('users.login'))
    form = AccountVerifiForm()
    if form.validate_on_submit():
        user.Activate = 1
        db.session.commit()
        flash('Your account has been activated! You are now able to login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('activate_account.html', title='Submit Account Verification',form=form)


@users.route("/upload", methods=['GET', 'POST'])
def upload():
    form = UploadFileForm()
    if form.validate_on_submit():
        if form.csvfile.data:
            f = upload_csv_file(form.csvfile.data)
            data = parseCSV(f)  
        flash('Upload data', 'success')
        subform = UploadFileToDBForm()
        return render_template('data.html', data=data, form=subform)
    return render_template('csv_upload.html', form=form)
        


@users.route("/upload_data", methods=['GET', 'POST'])
def data():
    #   # get the uploaded file
    # uploaded_file = request.files['csvfile']
    # if request.method == 'POST':
    #     f = upload_csv_file(uploaded_file)
    #     data = parseCSV(f)  
    #     # with open(f) as file:
    #     #     csvfile = csv.reader(file)
    #     #     for row in csvfile:
    #     #         data.append(row)
    return render_template('data.html', data=data)

