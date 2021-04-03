from flask import Blueprint, request, render_template

from tim_web_server.models import Post

main = Blueprint('main', __name__)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("main.html", posts=posts)


@main.route('/about')
def about():
    return render_template("about.html", title='关于我们')


@main.route('/echo/<msg>')
def echo(msg):
    return '<h1>Hello I am a Echo Website I can echo everything :{}.</h1>'.format(msg)
