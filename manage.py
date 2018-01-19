# -*- encoding=UTF-8 -*-

from pro1 import app,db
from flask_script import Manager
from pro1.models import User,Image,Comment
import random

manager = Manager(app)

def get_image_url():
    return 'http://images.nowcoder.com/head/'+str(random.randint(0,1000))+'m.png'

@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 20):
        db.session.add(User('user' + str(i + 1), '123','0'))
        for j in range(0, 5):
            db.session.add(Image(get_image_url(), i + 1))
            for k in range(0, 3):
                db.session.add(Comment('this is comment' + str(k), 1 + 3 * i + j, i + 1))
    db.session.commit()
    print 1,User.query.all()
    print 2,User.query.filter_by(name='user1').first()

if __name__ == '__main__':
    manager.run()