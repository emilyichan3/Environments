from flask import flash, redirect, render_template, url_for, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskapp_env import db
from flaskapp_env.posts.forms import PostForm, SearchForm
from flaskapp_env.modules_TIA import Post

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, post_content=form.post_content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', 
                        form=form, legend='New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method =='GET':
        form.title.data = post.title
        form.post_content.data = post.post_content
    return render_template('create_post.html', title='Update Post', 
                        form=form, legend='Update Post')
 
@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
#refer. <form action="{{ url_for('delete_post', post_id=post.id) }}" method="POST">
def delete_post(post_id): 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('main.home'))

#PASS stuff to Navbar
@posts.app_context_processor
def base():
    form = SearchForm()
    return dict(form=form)
    
@posts.route('/search', methods=["POST"])
def search():
     form = SearchForm()
     posts = Post.query
     if form.validate_on_submit():
        page = request.args.get('page',1, type=int)
        post.searched = form.searched.data
        posts = posts.filter(Post.post_content.like('%' + post.searched + '%'))
        posts = posts.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
        
        return render_template("search.html", 
                form=form, 
                searched=post.searched,
                posts = posts)