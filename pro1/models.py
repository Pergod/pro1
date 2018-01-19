# -*- encoding=UTF-8 -*-

from pro1 import db
from datetime import datetime
from pro1 import login_manager
import random,json
from datetime import date

# json.dumps()不能解析日期date类型
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20),  nullable=False)
    salt = db.Column(db.String(32))
    password = db.Column(db.String(60),  nullable=False)
    head_url = db.Column(db.String(256), nullable=False)

    #角色 1=管理员，0=普通
    role = db.Column(db.String(1),default='0')
    images =  db.relationship('Image', backref='user', lazy=True)
    def __init__(self,name,password,role,salt=''):
        self.name = name
        self.password = password
        self.salt = salt
        self.role = role
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'

    def __repr__(self):
        return '[ User %d %s %s]' % (self.id, self.name,self.role)

    # Flask Login接口
    @property
    def is_authenticated(self):
        print 'is_authenticated'
        return True

    @property
    def is_active(self):
        print 'is_active'
        return True

    @property
    def is_anonymous(self):
        print 'is_anonymous'
        return False

    def get_id(self):
        print 'get_id'
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url  = db.Column(db.String(256), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments =  db.relationship('Comment')
    def __init__(self,url,user_id):
        self.url = url
        self.user_id = user_id
        self.create_time = datetime.now()

    def __repr__(self):
        return '<Image %d %s>' % (self.id, self.url)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    status = db.Column(db.Boolean,default = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))

    user = db.relationship('User')

    def __init__(self, content, image_id, user_id):
        self.content = content
        self.image_id = image_id
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %d %s>' % (self.id, self.content)
