import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from tim_web_server import app, db, bcrypt, mail
from tim_web_server.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, \
    ResetPasswordForm
from tim_web_server.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_mail import Message


# posts = [
#     {
#         'author':'沧海一声笑',
#         'title':'发个帖试试看自己的ID是啥？',
#         'content':'哈哈哈哈，反正我也没啥事，发个帖自己看看ID是啥',
#         'date_posted':'2019年8月8日'
#     },
#     {
#         'author':'笑傲江湖我试试',
#         'title':'你连你是谁都不知道？',
#         'content':'哈哈哈哈，沧海一声笑，你连你是谁都不知道啊？',
#         'date_posted':'2019年9月9日'
#     },
#     {
#         'author':'笑傲江湖我试试',
#         'title':'你连你是谁都不知道？',
#         'content':'哈哈哈哈，沧海一声笑，你连你是谁都不知道啊？',
#         'date_posted':'2019年9月9日'
#     },
#     {
#         'author':'笑傲江湖我试试',
#         'title':'你连你是谁都不知道？',
#         'content':'哈哈哈哈，沧海一声笑，你连你是谁都不知道啊？',
#         'date_posted':'2019年9月9日'
#     }
# ]


@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("main.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html", title='关于我们')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # db.create_all()
        db.session.add(user)
        db.session.commit()
        flash(f'您的账号已经成功注册~欢迎【{form.username.data}】加入我们。', 'success')
        return redirect(url_for('index'))
    return render_template("register.html", title='注册界面', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("登录失败！", 'danger')
    return render_template("login.html", title='登录界面', form=form)


@app.route('/echo/<msg>')
def echo(msg):
    return '<h1>Hello I am a Echo Website I can echo everything :{}.</h1>'.format(msg)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, "static/user_profile_pics", picture_filename)
    # form_picture.save(picture_path)

    output_img_size = (100, 100)
    thumbnail_img = Image.open(form_picture)
    thumbnail_img.thumbnail(output_img_size)
    thumbnail_img.save(picture_path)

    return picture_filename


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
        flash("您的信息已经成功更新", "uccess")
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="user_profile_pics/" + current_user.image_file)
    return render_template("account.html", title='我的账户页面', image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("您的文章已成功发布！", "success")
        return redirect(url_for('index'))

    return render_template("create_post.html", title='写新文章', form=form, legend='写新文章')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title='更新文章', form=form, legend='更新文章')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("您的文章已成功删除！", "success")
    return redirect(url_for('index'))


@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=3)
    return render_template("user_posts.html", posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('关于重置信息的邮件', sender='yutinglv1994@163.com', recipients=[user.email])
    msg.body = f'''请点击下列连接进行重置操作：
    【{url_for('reset_token', token=token, _external=True)}】
    ___________________如果你没有进行重置操作却受到这封邮件，您的信息可能已经泄露，请及时修改密码_______________
    '''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('已经将重置密码邮件发送到您的邮箱', 'info')
        return redirect(url_for('login'))
    return render_template("reset_request.html", title='邮箱重置密码页面', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('不好意思，验证错误，请重试', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f'您的账号已经成功修改~欢迎', 'success')
        return redirect(url_for('login'))
    return render_template("reset_token.html", title='输入新密码页面', form=form)
