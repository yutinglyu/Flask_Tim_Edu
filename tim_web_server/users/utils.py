import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from tim_web_server import  mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(current_app.root_path, "static/user_profile_pics", picture_filename)
    # form_picture.save(picture_path)

    output_img_size = (100, 100)
    thumbnail_img = Image.open(form_picture)
    thumbnail_img.thumbnail(output_img_size)
    thumbnail_img.save(picture_path)

    return picture_filename

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('关于重置信息的邮件', sender='yutinglv1994@163.com', recipients=[user.email])
    msg.body = f'''请点击下列连接进行重置操作：
    【{url_for('users.reset_token', token=token, _external=True)}】
    ___________________如果你没有进行重置操作却受到这封邮件，您的信息可能已经泄露，请及时修改密码_______________
    '''
    mail.send(msg)


