from datetime import datetime

from libs.db import db

class Weibo(db.Model):
    __tablename__ = 'weibo'
    # 作者和微博的关系  一对多关系   不一定使用外键  只是约束关系
    #外键的缺点：慢  效率低  对于大型数据  在查询的时候  A链接B  会关联性的扫描
   #数据库中有自带索引的
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)   #用户id
    # show databases;   use weibo;  show tables;  show indexes in user; show  indexes in user \G;
    # 加索引的情况  Btree(二三树（更具效率）B父节点保存数据   B+树  没有父节点数据 由子节点关联在一起)  二叉树 (父节点  两条线)
    content = db.Column(db.Text)  #创建时间
    created = db.Column(db.DateTime, default=datetime.now)  # 发布时间
    updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 最后修改的时间
    n_like = db.Column(db.Integer, default=0)  # 当前微博的点赞数量
#
#
class Like(db.Model):
    __tablename__ = 'like'

    uid = db.Column(db.Integer, primary_key=True)
    wid = db.Column(db.Integer, primary_key=True)