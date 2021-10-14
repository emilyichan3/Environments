from flask import flash, redirect, render_template, url_for, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp_env import  db, bcrypt
from flaskapp_env.modules import Member, Post
from flaskapp_env.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm
                        , RequestResetForm, ResetPasswordForm)
from flaskapp_env.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        member = Member(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(member)
        db.session.commit()

        flash('Your account has been created! You are now able to login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        member = Member.query.filter_by(email=form.email.data).first()
        if member and bcrypt.check_password_hash(member.password, form.password.data):
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
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        # form.XXXX 指label，內容的話要.data
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page',1, type=int)
    member = Member.query.filter_by(username=username).first_or_404()
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
        user = Member.query.filter_by(email=form.email.data).first()
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
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password',form=form)

