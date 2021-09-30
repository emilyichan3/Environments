from flask import flash, redirect, render_template, url_for, request
from flaskapp_env import app, db, bcrypt
from flaskapp_env.forms import RegistrationForm, LoginForm
from flaskapp_env.modules import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
