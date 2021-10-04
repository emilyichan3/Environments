import os
import secrets
from PIL import Image #pip install Pillow
from flask import flash, redirect, render_template, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp_env import app, db, bcrypt
from flaskapp_env.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskapp_env.modules import User, Post

recipes = [
    {
        'recipe':'Baileys Cream Cheese Cake',
        'original':'Ireland',
        'level': 'Easy',
        'serves':4
    },
    {
        'recipe':'Roll Cake',
        'original':'Japan',
        'level': 'Easy',
        'serves':4
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=recipes)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You are now able to login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
             #argus is dictionary
             #為了確保如果在link上面沒有next字樣，若使用key去尋找時會出錯
             #所以使用get來搜尋，找不到next時就會回傳null
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Pleach check email and password!','danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    #使用 splitext區分檔案名稱和類型，最前面的_代表 "忽略回傳的第一個值"
    _, f_ext = os.path.splitext(form_picture.filename)
    #重新命名檔名為8字元的亂數，但維持相同的副檔名
    picture_fn = random_hex + f_ext 
    #新的檔案路徑
    picture_path = os.path.join(app.root_path, 'static\profile_pics', picture_fn)
    #re-size the picture (from Pillow package)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        # form.XXXX 指label，內容的話要.data
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
