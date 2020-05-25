#图片保存

import os

#根据昵称保存
from functools import wraps

from flask import session, render_template


def save_avatar(nickname,avatar_file):
    #规定头像的绝对路径
    base_dir=os.path.dirname(os.path.abspath(__name__))

    file_path=os.path.join(base_dir,'static','upload',nickname)
    avatar_file.save(file_path)


def login_required(view_func):
    '''登陆验证装饰器
    检查函数
    检查uid的会话参数
    否则就跳转到登录页
    不改变使用装饰器原有函数的结构(如__name__, __doc__)
    '''
    @wraps(view_func)
    def check(*args, **kwargs):
        if 'uid' in session:
            return view_func(*args, **kwargs)
        else:
            return render_template('login.html', error='请您先登录')
    return check