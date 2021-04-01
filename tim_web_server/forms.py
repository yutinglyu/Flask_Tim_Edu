from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from tim_web_server.models import User


class RegistrationForm(FlaskForm):
    username = StringField("昵称",
                           validators=[DataRequired(message="请填写昵称"), Length(min=2, max=20, message="名称要2到20字符哦")])
    email = StringField("邮箱", validators=[DataRequired(message="请填写邮箱"), Email(message="邮箱格式不正确")])
    password = PasswordField("密码", validators=[DataRequired(message="请输入密码")])
    confirm_password = PasswordField("再次输入密码", validators=[DataRequired(message="请再次输入密码"),
                                                           EqualTo("password", message="两次输入密码不一样")])
    submit = SubmitField("点击注册")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("用户名已被注册")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("邮箱已被注册")


class UpdateAccountForm(FlaskForm):
    username = StringField("昵称",
                           validators=[DataRequired(message="请填写昵称"), Length(min=2, max=20, message="名称要2到20字符哦")])
    email = StringField("邮箱", validators=[DataRequired(message="请填写邮箱"), Email(message="邮箱格式不正确")])
    picture = FileField("点我上传头像", validators=[FileAllowed(["jpg", "png"], message="目前只支持jpg、png文件哦")])
    submit = SubmitField("点我更新个人信息")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("用户名已被注册")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("邮箱已被注册")


class LoginForm(FlaskForm):
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住密码")
    submit = SubmitField("点击登录")


class PostForm(FlaskForm):
    title = StringField("文章标题", validators=[DataRequired(message="请填写标题")])
    content = TextAreaField("文章内容", validators=[DataRequired(message="请填写内容")])
    submit = SubmitField("点我发表文章")


class RequestResetForm(FlaskForm):
    email = StringField("邮箱", validators=[DataRequired(message="请填写邮箱"), Email(message="邮箱格式不正确")])
    submit = SubmitField("点击邮箱验证")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("邮箱不存在")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("密码", validators=[DataRequired(message="请输入密码")])
    confirm_password = PasswordField("再次输入密码", validators=[DataRequired(message="请再次输入密码"),
                                                           EqualTo("password", message="两次输入密码不一样")])
    submit = SubmitField("点击重置密码")
