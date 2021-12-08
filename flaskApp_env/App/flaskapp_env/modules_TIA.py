from datetime import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskapp_env import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(member_id):
    return Member.query.get(int(member_id)) 

class Member(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Member_ID = db.Column(db.String(20), unique=True, nullable=False)
    Period = db.Column(db.String(6), nullable=False)
    Activate = db.Column(db.Integer, default=0)
    Name = db.Column(db.String(60), nullable=False)
    MainMemberId = db.Column(db.String(20), nullable=False)
    MembershipType = db.Column(db.Integer, default=0)
    Email1 = db.Column(db.String(120), nullable=False)
    Email2 = db.Column(db.String(120), nullable=False)
    Email3 = db.Column(db.String(120), nullable=False)
    Email4 = db.Column(db.String(120), nullable=False)
    Phone1 = db.Column(db.String(120), nullable=False)
    Phone2 = db.Column(db.String(120), nullable=False)
    Phone3 = db.Column(db.String(120), nullable=False)
    Phone4 = db.Column(db.String(120), nullable=False)
    ValidDateFm = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ValidDateTo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ValidCheckDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ValidDays = db.Column(db.Integer, default=0)   
    SendEmailDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    MembershipChangedPeriod = db.Column(db.String(6), nullable=False)
    Image_file = db.Column(db.String(50), nullable=False, default='default.jpg')
    Password = db.Column(db.String(50), nullable=False)
    NationalCode = db.Column(db.String(50), default='', nullable=False)
    StopContact = db.Column(db.Integer, default=0)   
    Comment = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
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
        return f"Member('{self.Member_ID}', '{self.Name}', '{self.Emil1}', '{self.Image_file}')"

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
    CountryCode = db.Column(db.String(3), primary_key=True)
    CountryName = db.Column(db.String(250), nullable=False)
    CountryNameEN = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Country('{self.CountryCode}', '{self.CountryName}')"

class Membership(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    MembershipCode = db.Column(db.String(20), nullable=False)
    MembershipName = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Country('{self.id}', '{self.MembershipName}')"

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Term = db.Column(db.String(6), nullable=False)
    Description = db.Column(db.String(200), nullable=False)
    Member_Pre = db.Column(db.String(6), nullable=False)
    Member_NextSeq = db.Column(db.Integer, default=1)
    ValidDateFm = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ValidDateTo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Term('{self.Term}', '{self.Description}')"