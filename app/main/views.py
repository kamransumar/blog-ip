from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from . import main
from ..models import User, Blog, Comment
from .forms import *
from .. import db, photos
from datetime import datetime
# Views


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to The best Movie Review Website Online'
    blogs = Blog.query.all()

    return render_template('index.html', title=title, blogs=blogs)


@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username=name).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<name>/update', methods=['GET', 'POST'])
@login_required
def update_profile(name):
    user = User.query.filter_by(username=name).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.username = form.username.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', name=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<name>/update/pic', methods=['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username=name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.image = path
        db.session.commit()
    return redirect(url_for('main.profile', name=name))


@main.route('/blog/', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():

        content = form.content.data
        title = form.title.data
        # Updated review instance
        new_blog = Blog(
            content=content, title=title)
        db.session.add(new_blog)
        db.session.commit()

    return render_template('blog.html', blog_form=form)


@main.route('/blog/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_comment(id):
    '''
    view category that returns a form to create a new comment
    '''
    form = CommentForm()
    blog = Blog.query.filter_by(id=id).first()

    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data

        # comment instance
        new_comment = Comment(
            blog_id=blog.id, post_comment=comment, title=title, user=current_user)

        # save comment
        new_comment.save_comment()

        return redirect(url_for('.blogs', id=blog.id))

    title = f'{blog.title} comment'
    return render_template('newcomment.html', title=title, comment_form=form, blog=blog, )


@main.route('/allblogs')
def blog_list():

    blogs = Blog.query.all()

    return render_template('blog.html', blogs=blogs)


@main.route('/oneblog/<int:id>', methods=['GET', 'POST'])
def one_blog(id):

    blog = Blog.query.get(id)
    form = CommentForm()
    blog = Blog.query.filter_by(id=id).first()

    if form.validate_on_submit():
        # comment instance
        new_comment = Comment(
            ratings=0,
            like=0,
            dislike=0,
            content=form.content.data,
            time=datetime.utcnow(),
            blog=blog,
            author=current_user)

        # save comment
        db.session.add(new_comment)
        db.session.commit()

    comments = blog.comment_id

    return render_template('viewblog.html', blog=blog, comment_form=form, comments=comments)
