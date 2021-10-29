import os
import secrets
from PIL import Image #pip install Pillow
from flask_mail import Message
from flask import url_for, current_app, render_template
from flaskapp_env import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    #使用 splitext區分檔案名稱和類型，最前面的_代表 "忽略回傳的第一個值"
    _, f_ext = os.path.splitext(form_picture.filename)
    #重新命名檔名為8字元的亂數，但維持相同的副檔名
    picture_fn = random_hex + f_ext 
    #新的檔案路徑
    picture_path = os.path.join(current_app.root_path, 'static\profile_pics', picture_fn)
    #re-size the picture (from Pillow package)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()

    msg = Message('Password Reset Request', 
                sender='noreply@demo.com', 
                cc = [user.email],
                reply_to = 'emilyichan3@gmail.com')
#     msg.body = f'''To reset your password, click the following link:
# {url_for('users.reset_token',token=token, _external=True)}

# If you did not make this request then simply ignor this email and no changes will be made.
# '''
    msg.html = render_template('/mails/reset-password.html', username=user.username, token=token)
    
    with current_app.open_resource("Evidence_Detailed-relationship-history-timeline.pdf") as fp:  
        msg.attach("Evidence_Detailed-relationship-history-timeline.pdf", "application/pdf", fp.read())  

    mail.send(msg)

def send_account_verification(user):
    token = user.get_activate_token()
    msg = Message('Account verification Request', 
                sender='noreply@demo.com', 
                recipients=[user.email],
                cc = [user.email])
    msg.body = f'''If you want to activate account in CookLab.com, click the following link:
{url_for('users.activate_account',token=token, _external=True)}

If you did not make this request then simply ignor this email and no changes will be made.
'''
    mail.send(msg)