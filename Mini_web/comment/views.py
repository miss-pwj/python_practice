
from flask import Blueprint
from flask import abort
from flask import request
from flask import redirect
from flask import session

from comment.models import Comment
from libs.db import db
from user.loginc import login_required

comment_bp = Blueprint('comment', import_name='comment')

# 发表评论  全部是跳转  因为是在某一条微博下
# 加登陆验证 登陆状态下
@comment_bp.route('/post', methods=('POST',))
@login_required
def post():
    uid = session['uid']
    wid = int(request.form.get('wid'))
    content = request.form.get('content')
    cmt = Comment(uid=uid, wid=wid, content=content)
    db.session.add(cmt)
    db.session.commit()
    return redirect('/weibo/show?wid=%s' % wid)


# 发表回复
@comment_bp.route('/reply', methods=('POST',))
@login_required
def reply():
    uid = session['uid']
    wid = int(request.form.get('wid'))
    cid = int(request.form.get('cid'))  # 主评论的id  加上
    rid = int(request.form.get('rid'))  # 回复的id
    content = request.form.get('content')
    cmt = Comment(uid=uid, wid=wid, cid=cid, rid=rid, content=content)
    db.session.add(cmt)
    db.session.commit()
    return redirect('/weibo/show?wid=%s' % wid)


# 删除评论
@comment_bp.route('/delete')
@login_required
def delete():
    cid = int(request.args.get('cid'))
    # 当前评论
    cmt = Comment.query.get(cid)
#     检查   是否在删除自己的微博的评论 或者连级评论
    if cmt.uid != session['uid']:
        abort(403)
    if cmt.cid == 0:
#         找到对应的回复  id
        Comment.query.filter_by(cid=cmt.id).delete()
    db.session.delete(cmt)
    db.session.commit()
    return redirect('/weibo/show?wid=%s' % cmt.wid)

# 数据库中的数据一般不会删除