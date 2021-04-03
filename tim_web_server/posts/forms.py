from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("文章标题", validators=[DataRequired(message="请填写标题")])
    content = TextAreaField("文章内容", validators=[DataRequired(message="请填写内容")])
    submit = SubmitField("点我发表文章")


