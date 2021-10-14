import os
import secrets
from PIL import Image #pip install Pillow
from flask import flash, redirect, render_template, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp_env import app, db, bcrypt, mail
from flaskapp_env.forms import (RegistrationForm, LoginForm, UpdateAccountForm
                        , PostForm, RequestResetForm, ResetPasswordForm)
from flaskapp_env.modules import Member, Post
from flask_mail import Message

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page',1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

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
        member = Member(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(member)
        db.session.commit()

        flash('Your account has been created! You are now able to login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, post_content=form.post_content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', 
                        form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.post_content = form.post_content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method =='GET':
        form.title.data = post.title
        form.post_content.data = post.post_content
    return render_template('create_post.html', title='Update Post', 
                        form=form, legend='Update Post')
 
@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
#refer. <form action="{{ url_for('delete_post', post_id=post.id) }}" method="POST">
def delete_post(post_id): 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page',1, type=int)
    member = Member.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=member)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page , per_page=5)
    return render_template('user_posts.html', posts=posts,user=member)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                sender='noreply@demo.com', 
                recipients=[user.email])
    msg.body = f'''To reset your password, click the following link:
{url_for('reset_token',token=token, _external=True)}

If you did not make this request then simply ignor this email and no changes will be made.
'''
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Member.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password',form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = Member.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired link', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password',form=form)
