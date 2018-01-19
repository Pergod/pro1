# -*- encoding=UTF-8 -*-

from pro1 import app,db,mail
from flask import render_template
from models import User,Image,Comment,CJsonEncoder
from flask import redirect,request,flash,get_flashed_messages
from flask_login import login_user,logout_user,login_required,current_user
from flask_mail import Message
from flask import send_from_directory
#from qiniu import qiniu_upload_file
import uuid,os
import random,hashlib,json


#首页
@app.route('/')
def index():
    paginate = Image.query.paginate(page=1,per_page=5,error_out=False)
    images = paginate.items
    return render_template('index.html',images=paginate.items,has_next = paginate.has_next)

#更多-首页
@app.route('/<int:page>/<int:per_page>/')
def get_more_images(page, per_page):
    paginate = Image.query.paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next':paginate.has_next}
    images = []
    for image in paginate.items:
        comments = []
        for comment in image.comments:
            commentVo ={
                'content':comment.content,
                'comment_user_name':comment.user.name,
                ' ':comment.user.id
            }
            comments.append(commentVo)
        imgVo = {'image_id':image.id,
                 'image_url':image.url,
                 'comment_count':len(image.comments),
                 'user_id':image.user.id,
                 'head_url':image.user.head_url,
                 'create_time':image.create_time,
                 'comments':comments,
                 'user_name':image.user.name}
        images.append(imgVo)
        # print ('images',images)
    map['images'] = images
    json_data = json.dumps(map,cls=CJsonEncoder)
    print('json',json_data)
    return json_data

@app.route('/edit/comment/')
def edit_comment():

    return ""

#用户详情页
@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id = user.id).paginate(page=1,per_page=3,error_out=False)
    return render_template('profile.html', user = user,images = paginate.items,has_next = paginate.has_next)

#更多-用户详情页
@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def get_user_more_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    map = {'has_next':paginate.has_next}
    images = []
    for image in paginate.items:
        imgVo = {'id':image.id,'image_url':image.url,'comment_count':len(image.comments)}
        images.append(imgVo)
    map['images'] = images
    return json.dumps(map)

#获取用户登录注册页
@app.route('/loginAndRegPage/')
def loginAndRegPage():
    msg = ''
    for m in get_flashed_messages(with_categories=False,category_filter='login'):
        msg = msg + m
    return render_template('login.html',msg=msg,next=request.values.get('next'))

def redirect_with_msg(dst,msg,category):
    if msg!=None:
        flash(msg,category=category)
    return redirect(dst)

#发送邮件--测试
@app.route('/send_email/', methods=['GET', 'POST'])
def send_email():
    msg = Message("Welcome register nowcoder!", recipients=["m2822583132@qq.com"])
    mail.send(msg)
    return redirect('/')

#注册用户
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # request.args  url字符串
    # request.form 表单提交
    name = request.values.get('name').strip()
    password  = request.values.get('password').strip()
    email = request.values.get('email').strip()
    role = request.values.get('role').strip()
    user = User.query.filter_by(name=name).first()
    if name =='' or password == '':
        return redirect_with_msg(dst='/loginAndRegPage/', msg=u'用户名密码不能为空', category='login')
    if user!=None:
        return redirect_with_msg(dst='/loginAndRegPage/', msg=u'用户已存在', category='login')
    #加盐  防止破解
    salt ='.'.join(random.sample('0123456789ABCDabcdefghijk',10))

    m = hashlib.md5()
    m.update(password + salt)
    password = m.hexdigest()

    user = User(name=name,password=password,role=role,salt=salt)
    db.session.add(user)
    db.session.commit()
    #注册用户后直接登录
    login_user(user)
    msg = Message("Welcome register nowcoder!", recipients=[email])
    mail.send(msg)
    next = request.values.get('next')
    if next != None and next.startswith('/'):
        return redirect(next)
    return redirect('/')

#登出
@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')

#登录
@app.route('/login/',methods=['GET', 'POST'])
def login():
    name = request.values.get('name').strip()
    password = request.values.get('password').strip()
    if name =='' or password=='':
        return redirect_with_msg(dst='/loginAndRegPage/',msg=u'用户名和密码不能为空', category='login')

    user = User.query.filter_by(name=name).first()
    if user == None:
        return redirect_with_msg(dst='/loginAndRegPage/', msg=u'用户名不存在', category='login')

    m = hashlib.md5()
    m.update(password + user.salt)

    if m.hexdigest() != user.password:
        return redirect_with_msg(dst='/loginAndRegPage/', msg=u'密码不正确', category='login')
    login_user(user)
    next = request.values.get('next')
    print 'next',next
    if next != None and next.startswith('/'):
        return redirect(next)
    return redirect('/')

@app.route('/upload/',methods=['POST'])
def uploadFile():
    print 1,'request.files',request.files
    file = request.files['file']
    print 'file = ',dir(file)
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.',1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_FILE']:
        file_name = str(uuid.uuid1()).replace('-','') + '.' + file_ext
        url = save_to_local(file,file_name)
        # url = qiniu_upload_file(file,file_name)
        if url != None:
            db.session.add(Image(url,current_user.id))
            db.session.commit()
    return redirect('/profile/%d' % current_user.id)

@app.route('/delete/<int:image_id>/',methods=['GET', 'POST'])
def deleteImage(image_id):
    image = Image.query.get(image_id)
    db.session.delete(image)
    db.session.commit()
    return redirect('/')

def save_to_local(file,file_name):
    save_dir = app.config['UPLOAD_PATH']
    # os.path = /
    file.save(os.path.join(save_dir,file_name))
    return '/image/' + file_name

@app.route('/image/<image_name>')
def show_image(image_name):
    return send_from_directory(app.config['UPLOAD_PATH'] ,image_name)

@app.route('/image/<int:image_id>/')
def page_detail(image_id):
    image =  Image.query.get(image_id)
    if image == None:
        return redirect('/')
    comments = Comment.query.filter_by(image_id=image_id).order_by(db.desc(Comment.id)).limit(20).all()
    return render_template('pageDetail.html',image = image,comments = comments)

@app.route('/addcomment/', methods=['POST'])
@login_required
def add_comment():
    image_id = int(request.values['image_id'])
    content = request.values['content']
    comment = Comment(content, image_id, current_user.id)
    if current_user == None:
        json_data = json.dumps({
                        "code": 1,
                        "msg": "未登录，无法评论"
                        })
        return json_data
    db.session.add(comment)
    db.session.commit()
    image = Image.query.get(image_id)
    # 获取评论条数
    comment_count = len(image.comments)
    json_data  = json.dumps({"code":0, "id":comment.id,
                       "content":comment.content,
                       "username":comment.user.name,
                       "comment_count":comment_count,
                       "user_id":comment.user_id})
    print('json',json_data);
    return json_data

