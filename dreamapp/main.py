from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import User, Post
import datetime


main = Blueprint('main', __name__)

@main.route('/')
def index():
    posts = Post.query.all()

    # if (current_user.is_authenticated):
    #     user = User.query.get(current_user.id).first()
    #     subscribed = user.subscribe
    # else:
    #     subscribed=false

    posts.reverse()

    return render_template('index.html', posts=posts, curr_user=current_user)


@main.route('/post', methods=['GET'])
@login_required
def post():
    return render_template('post.html', curr_user=current_user)


@main.route('/post', methods=['POST'])
@login_required
def post_post():
    title = request.form.get('title')
    contents = request.form.get('contents')
    user = current_user
    date = datetime.date.today()

    new_post = Post(title=title, contents=contents, user=user, date=date)

    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('main.index'))


@main.route('/delete', methods=['post'])
@login_required
def delete():
    id = request.form.get('id')
    post = Post.query.filter_by(id=id).first()
    
    if post is None:
        flash("Post does not exist")
        return redirect(url_for('main.index'))
    
    if post.user.id is not current_user.id:
        flash("You do not own that post")
        return redirect(url_for('main.index'))
        
    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('main.index'))
