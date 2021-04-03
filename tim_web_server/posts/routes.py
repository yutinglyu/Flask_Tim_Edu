from flask import Blueprint, redirect, url_for, flash, render_template, request, abort
from flask_login import current_user, login_required
from tim_web_server import db
from tim_web_server.models import Post
from tim_web_server.posts.forms import PostForm
from datetime import datetime

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("您的文章已成功发布！", "success")
        return redirect(url_for('main.index'))

    return render_template("create_post.html", title='写新文章', form=form, legend='写新文章')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_posted = datetime.utcnow()
        db.session.commit()
        flash("您的文章已成功修改！", "success")
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title='更新文章', form=form, legend='更新文章')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("您的文章已成功删除！", "success")
    return redirect(url_for('main.index'))
