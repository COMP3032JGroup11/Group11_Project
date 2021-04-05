from webapp import app

from flask_script import Manager

app = app
manage = Manager(app)


# @app.route("/")
# def first_index():
#     return "hello_world"
# python wigi.py runserver

"""


from flask import Flask
app = Flask(__name__)
 
# 首页
@app.route('/')  # 接口地址
def index():
    # 接口本身
    return 'home'
 
# 登录页
@app.route('/login')  #接口地址
def login():
    # 接口本身
    return 'login sucess'
 
# web 服务器
if __name__ == '__main__':




"""

if __name__ == '__main__':
    manage.run()
