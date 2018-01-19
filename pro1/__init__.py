# -*- encoding=UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_pyfile("app.conf")
db = SQLAlchemy(app)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.secret_key = 'nowcoder'
login_manager = LoginManager(app)
#配置未登录时跳转的页面
login_manager.login_view='/loginAndRegPage/'
mail = Mail(app)

from pro1 import views,models
