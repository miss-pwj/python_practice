#模型
from libs.db import db


class User(db.Model):
    """
    用户表
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    # weibo的昵称 唯一  LOL昵称必须是不同  需求:
    nickname=db.Column(db.String(20),unique=True,nullable=False,index=True)
    password = db.Column(db.String(128),nullable=True)
    gender = db.Column(db.String(10),default='unkonw')
    bio =db.Column(db.String(255))
    city =db.Column(db.String(20),default='成都')
    avatar =db.Column(db.String(128))
    birthday=db.Column(db.Date,default='1970-01-01')
    create =db.Column(db.DateTime)
    num = db.Column(db.Integer)


class Follow(db.Model):
    '''关注表'''
    __tablename__ = 'follow'
    uid = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, primary_key=True)