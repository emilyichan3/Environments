from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskapp_env import db, login_manager
from flask_login import UserMixin, current_user

@login_manager.user_loader
def load_user(member_id):
    return Member.query.get(int(member_id)) 

class Member(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    activate = db.Column(db.Integer, default=0)
    country_code = db.Column(db.String(3), default='', nullable=False)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    membership_type = db.Column(db.Integer, default=0)

    def user_variables(self):
        user_details = {
            'User ID': ['id', current_user.id],
            'Username': ['username', current_user.username],
            'Email': ['email', current_user.email],
            'Image Profile': ['image_file', current_user.image_file],
            'Password': ['password', current_user.password],
            'Activate': ['activate', current_user.activate],
            'Nationality': ['country_code', current_user.country_code],
            'Date Registered': ['join_date', datetime.strftime(current_user.join_date, '%d/%m/%Y')],
            'Membership Type': ['membership_type', current_user.membership_type]
        }
        return user_details

    def get_reset_token(self, expires_sec=300): #5 mins
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    def get_activate_token(self, expires_sec=300): #5 mins
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Member.query.get(user_id)

    def __repr__(self):
        return f"Member('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_content = db.Column(db.Text, nullable=False)
    # ForeignKey('member.id')table名稱請一律"小寫"
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Country(db.Model):
    Code = db.Column(db.String(3), primary_key=True)
    Name = db.Column(db.String(25), nullable=False)
    NameEN = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Country('{self.Code}', '{self.Name}')"

class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Membership_Code = db.Column(db.String(20), nullable=False)
    Membership_Name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Country('{self.id}', '{self.Membership_Name}')"