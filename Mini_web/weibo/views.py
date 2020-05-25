import datetime
from math import ceil

from flask import Blueprint
from flask import *
from collections import OrderedDict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from comment.models import Comment
from libs.db import db
from user.loginc import login_required
from user.models import User, Follow
from weibo.models import Weibo, Like

weibo_bp = Blueprint('weibo', import_name='weibo')
weibo_bp.template_folder = './templates'

# 发布微博
# 利用装饰器检查用户是否登陆
@weibo_bp.route('/post', methods=('POST', 'GET'))
@login_required
def post():
    if request.method == 'POST':
        content = request.form.get('content').strip()
        # 内容不能为空
        if not content:
            return render_template('post.html', error='微博内容不允许为空！')
        else:
            weibo = Weibo(uid=session['uid'], content=content)
            weibo.updated = datetime.datetime.now()
            db.session.add(weibo)
            db.session.commit()
            # 提交之后返回到查看当前微博页面
            return redirect('/weibo/show?wid=%s' % weibo.id)
    else:
        return render_template('post.html')

# 查看发布的微博
@weibo_bp.route('/show')
def show():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    # 判断是否有微博
    if weibo is None:
        abort(404)
    else:
        user = User.query.get(weibo.uid)

        # 获取当前微博的所有评论
        # python 标准库中OrderedDict  有序字典  二维列表是可以转化为字典的  不能依赖字典的顺序
        # 字典和集合都是无序的
        comments = Comment.query.filter_by(wid=weibo.id).order_by(Comment.created.desc())
        all_uid = {c.uid for c in comments}  # 所有评论的作者的 ID
        cmt_users = dict(User.query.filter(User.id.in_(all_uid)).values('id', 'nickname'))
        comments = OrderedDict([[cmt.id, cmt] for cmt in comments])  # 将所有评论转成有序字典
        return render_template('show.html', weibo=weibo, user=user, cmt_users=cmt_users, comments=comments)


# 编辑微博    后端的检查不要依赖于前端  该有的检查不能少
#后端的检查不要依赖于前端
#对于前端传来的所有数据对后端来说都不可信
#所有的数据都必须检查
#后端开发能自己获取的数据不要依赖前端的
# #参数和返回值能少则少，不要一次传递太多数据
@weibo_bp.route('/edit', methods=('POST', 'GET'))
@login_required
def edit():
    if request.method == 'POST':
        wid = int(request.form.get('wid'))
        content = request.form.get('content').strip()
        if not content:
            return render_template('post.html', error='微博内容不允许为空！')
        else:
            weibo = Weibo.query.get(wid)
            # 取完微博id之后  做检查   我其他人能修改任何人的微博
            if weibo.uid != session['uid']:
                abort(403)
            weibo.content = content
            weibo.updated = datetime.datetime.now()
            db.session.add(weibo)
            db.session.commit()
            return redirect('/weibo/show?wid=%s' % weibo.id)
    else:
        wid = int(request.args.get('wid'))
        weibo = Weibo.query.get(wid)
        return render_template('edit.html', weibo=weibo)


# 删除微博
@weibo_bp.route('/delete')
@login_required
def delete():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    # 检查后端的id
    if weibo.uid != session['uid']:
        abort(403)
    else:
        db.session.delete(weibo)
        db.session.commit()
    return redirect('/')



@weibo_bp.route('/like')
@login_required
def like():
    wid = int(request.args.get('wid'))
    weibo = Weibo.query.get(wid)
    # 检查后端的id
    if session['uid'] == None:
        abort(403)
    else:
        # like = Like.query.filter(Like.uid == session['uid'] and Like.wid ==wid).all()
        # if like ==None:
        #     db.session.add(like)
        # w = Weibo.query.get(wid)
        weibo.n_like = weibo.n_like + 1
        db.session.commit()
        # wb_list = Weibo.query.all()
    return redirect('/')
    # return redirect('index.html',wb_list = wb_list)

@weibo_bp.route('/')
@weibo_bp.route('/index')
@weibo_bp.route('/top50')
def index():
    '''显示最新的前 50 条微博'''
    # 获取微博数据
    # 传入页码  根据页码  给出默认值
    page = int(request.args.get('page', 1))
    n_per_page = 10
    offset = (page - 1) * n_per_page
    # 当前页要显示的微博
    # select * from weibo order by updated desc limit 10 offset 20;
    wb_list = Weibo.query.order_by(Weibo.updated.desc()).limit(10).offset(offset)
    n_weibo = Weibo.query.count()  # 微博总数
    n_page = 5 if n_weibo >= 50 else ceil(n_weibo / n_per_page)  # 总页数

    # 获取微博对应的作者
    uid_list = {wb.uid for wb in wb_list}  # 取出微博对应的用户 ID
    # select id, nickname from user id in ...;
    # 取出之后是一个generator  里面是一个元组 转成字典
    users = dict(User.query.filter(User.id.in_(uid_list)).values('id', 'nickname'))
    return render_template('index.html', page=page, n_page=n_page, wb_list=wb_list,users=users)


#关注用户
@weibo_bp.route('/follow')
def follow():
    wid = int(request.args.get('wid'))
    web = Weibo.query.get(wid)
    uid=int(request.args.get('uid'))
    like=Like(uid=uid,wid=wid)
    follow=Follow(uid=web.uid,fid=uid)
    try:
        db.session.add(like)
        # 所有的数据处理准备好之后，执行commit才会提交到数据库！
        db.session.commit()
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        db.session.rollback()
    try:
        db.session.add(follow)
        db.session.commit()
    except Exception as e:
        # 加入数据库commit提交失败，必须回滚！！！
        db.session.rollback()

    return redirect('/')


#关注微博
@weibo_bp.route('/follow_weibo')
def follow_weibo():
    '''显示关注的微博'''
    try:
        page = int(request.args.get('page', 1))
        n_per_page = 10
        offset = (page - 1) * n_per_page
        # 当前页要显示的微博
        # select * from weibo order by updated desc limit 10 offset 20;
        wb_list = Weibo.query.order_by(Weibo.updated.desc()).limit(10).offset(offset)
        n_weibo = Weibo.query.count()  # 微博总数
        n_page = 5 if n_weibo >= 50 else ceil(n_weibo / n_per_page)  # 总页数

        # 获取微博对应的作者
        uid_list = {wb.uid for wb in wb_list}  # 取出微博对应的用户 ID
        # select id, nickname from user id in ...;
        # 取出之后是一个generator  里面是一个元组 转成字典
        users = dict(User.query.filter(User.id.in_(uid_list)).values('id', 'nickname'))
        return render_template('index.html', page=page, n_page=n_page, wb_list=wb_list, users=users)
    except:
        return redirect('/user/login')
