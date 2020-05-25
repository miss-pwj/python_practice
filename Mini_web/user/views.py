from sqlite3 import InternalError

from flask import Blueprint
from flask import *
from pymysql import IntegrityError
import numpy as np
import os
import cv2
import time
from libs.db import db
from libs.untils import gen_password, check_password
from user.loginc import save_avatar
from user.models import User, Follow
import datetime

user_bp = Blueprint('user', import_name='user')
user_bp.template_folder = './templates'
user_bp.static_folder = './static'


# 视图函数
# 注册  头像的上传  给出不同的请求方式 判断请求方式
@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # 通过请求  将页面是接收的参数取出来  用户什么都没写
        # newline = ''   pandas  to_csv  dict字典
        # 装饰器封装方法  py基础中的  Java  String
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()
        gender = request.form.get('gender', '').strip()
        bio = request.form.get('bio', '').strip()
        city = request.form.get('city', '').strip()
        birthday = request.form.get('birthday', '').strip()
        avatar = request.files.get('avatar')
        # 头像的处理  注册操作 添加数据
        # 创建一个user对象   相当于一条sql语句添加这么多的数据
        user = User(
            nickname=nickname,
            # 对数据库中存储的密码进行加密
            password=gen_password(password),
            #     性别   lamda 类似
            gender=gender if gender in ['male', 'female'] else 'male',
            bio=bio,
            city=city,
            birthday=birthday,
            #     处理头像  绝对路径的正确规定
            avatar='/static/upload/%s' % nickname,
            # 显示当前时间
            create=datetime.datetime.now()
        )

        #    将对象添加到数据库中

        #     引入了数据库的事务的特征  事务回滚
        """
           1.明确处理每一个异常
           2.try和except之间的语句、代码 越少越好  
           3.不要隐藏异常，而应该进行定向的处理
           """
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            # 如果出错了  打印一个提示信息
            return render_template('register.html', errors='昵称被占用,换一个')

        # 返回到登陆页面
        save_avatar(nickname, avatar)
        return redirect('/user/login')

    else:
        return render_template('register.html')

    #     异常的处理  当添加的对象  没有按照数据表的规定进行添加的话  会报错  抓异常
    #    异常：抓取（抓取异常 ）  抛出（一种不负责  没有用处  bug进行处理）  各有千秋


# 登陆
@user_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()

        # 利用sqlalchemy的查询方式
        user = User.query.filter_by(nickname=nickname).first()
        # 判断是否可以拿到
        if user is None:
            return render_template('login.html', error='用户名有误，请重新输入')
        # 判断密码是否正确
        if check_password(password, user.password):
            # 如果密码正确，记录用户登录状态   退出登录  session记录用户的登陆情况
            session['uid'] = user.id
            # 根据用户的状态去显示用户信息
            return redirect('/user/info')
        else:
            return render_template('login.html', error='密码不正确')

    else:
        if 'uid' in session:
            return redirect('/user/info')
        else:
            return render_template('login.html')


# 退出登陆
@user_bp.route('/logout')
def logout():
    session.pop('uid')
    return redirect('/')


@user_bp.route('/update', methods=('GET', 'POST'))
def to_update():
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()
        gender = request.form.get('gender', '').strip()
        bio = request.form.get('bio', '').strip()
        city = request.form.get('city', '').strip()
        birthday = request.form.get('birthday', '').strip()
        # 头像的处理  注册操作 添加数据
        # 创建一个user对象   相当于一条sql语句添加这么多的数据
        user = User(
            nickname=nickname,
            # 对数据库中存储的密码进行加密
            password=gen_password(password),
            #     性别   lamda 类似
            gender=gender if gender in ['male', 'female'] else 'male',
            bio=bio,
            city=city,
            birthday=birthday,

            # 显示当前时间
            create=datetime.datetime.now()
        )
        # User.query(user.nickname ==nickname).update()
        user = User.query.filter(user.nickname == nickname).first()
        user.password =gen_password(password)
        user.gender = gender
        user.bio = bio
        user.city = city
        user.birthday=birthday
        db.session.commit()
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect('/user/info')
    else:
        uid = session.get('uid')
        if uid:
            user = User.query.get(uid)
        return render_template('update.html', user=user)

@user_bp.route("/changeImg1", methods=('GET', 'POST'))
def tochangeImg():
    user = User()
    user.id  =int( request.args.get('uid'))
    return render_template('changeImg.html', user=user)


@user_bp.route("/changeImg", methods=('GET', 'POST'))
def changeImg():
    if request.method == 'POST':

        nickname = request.form.get('nickname', '').strip()

        avatar = request.files.get('avatar')
        # 头像的处理  注册操作 添加数据
        # 创建一个user对象   相当于一条sql语句添加这么多的数据
        user = User(
            nickname=nickname,
            avatar='/static/upload/%s' % nickname,

        )
        user.avatar =avatar
        save_avatar(nickname, avatar)
        try:
            db.session.commit()
        except:
            db.session.rollback()

        save_avatar(nickname, avatar)
        return redirect('/user/info')

    else:
        return redirect('/user/info')


# 信息
@user_bp.route('/info')
def info():
    '''用户个人资料页'''
    uid = session.get('uid')
    fid = int(request.args.get('uid', 0))

    # 查看自己页面
    if uid == fid or fid == 0:
        user = User.query.get(uid)
        return render_template('info.html', user=user)

    # 查看其他人的页面  检查uid
    if fid and uid != fid:
        user = User.query.get(fid)
        is_exist = Follow.query.filter_by(uid=uid, fid=fid).exists()
        followed = db.session.query(is_exist).scalar()
        return render_template('info.html', user=user, followed=followed)

    return render_template('login.html', error='请先登录！')


@user_bp.route('/follow/<id>')
# 关注
def follow(id):
    uid = session.get('uid')
    guanzhu = Follow.query.filter_by(uid=uid).first()
    print(guanzhu)
    if guanzhu is None:
        follow = Follow(
            uid=uid,
            fid=id
        )
        db.session.add(follow)
        db.session.commit()
        return redirect('/user/info')

# 粉丝列表
@user_bp.route('/fans')
def fans():
    '''粉丝列表'''
    uid = session.get('uid')
    sql='select * from follow where uid=uid'
    followid=db.session.execute(sql)
    # 查看其他人的页面  检查uid
    user_list =[]
    fod_list={fid.fid for fid in followid}
    for fid in fod_list:
        user_list.append(User.query.get(fid))
    return render_template('fans.html', fans=user_list)


# 采集人脸
@user_bp.route('/take_face', methods=('GET', 'POST'))
def take_face():
    cap = cv2.VideoCapture(0)  # 打开摄像头
    face_detector = cv2.CascadeClassifier('user/haarcascade_frontalface_alt.xml')  # 识别人脸
    print(face_detector, "==============")
    isFace = False  # 告诉我们是否检测出了人脸
    while True:
        flag, frame = cap.read()
        gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
        face_zones = face_detector.detectMultiScale(gray,
                                                    scaleFactor=1.2,
                                                    minNeighbors=5,
                                                    minSize=(80, 80),
                                                    maxSize=(320, 320))
        for x, y, w, h in face_zones:
            isFace = True
            face = frame[y + 1:y + h, x + 1:x + w]  # 彩色人脸
            cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=[0, 0, 255], thickness=1)
        if isFace:
            cv2.imshow('face', face)  # 有人脸，显示人脸
        else:
            cv2.imshow('face', frame)  # 没有人脸，显示画面
        key = cv2.waitKey(1000 // 24)
        isFace = False
        if key == ord('q'):
            break
        elif key == ord('w'):  # 说明采集的人脸，自己比较满意， 保存一下
            os.makedirs('user/face_certification', exist_ok=True)
            filename = os.listdir('user/face_certification')
            num = len(filename)
            face = cv2.cvtColor(face, code=cv2.COLOR_BGR2GRAY)  # 灰度化处理
            face = cv2.resize(face, dsize=(128, 128))  # 尺寸调整
            face = cv2.equalizeHist(face)  # 均衡化
            cv2.imwrite('user/face_certification/%d.jpg' % (num), face)  # 保存图片
            user = User.query.get(session['uid'])
            print(user.id,"---",session['uid'])
            user.num = num
            db.session.commit()
            break
    cv2.destroyAllWindows()
    cap.release()

    if 'uid' in session:
        return redirect('/user/info')
    else:
        print("采集失败")


# 人脸登录
@user_bp.route('/face_login', methods=("GET", "POST"))
def face_login():

    cap = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier('user/haarcascade_frontalface_alt.xml')
    face_recognizer = cv2.face.LBPHFaceRecognizer_create(threshold=200)  # 训练
    faces = os.listdir('user/face_certification')  # 列表
    print(faces)
    if len(faces)==0 :
        return render_template('login.html',error ="没有采集头像，登录失败")
    X = np.asarray([cv2.imread('user/face_certification/' + face)[:, :, 0] for face in faces])
    y = np.asarray([int(face.split('.')[0]) for face in faces])
    face_recognizer.train(X, y)  # train，算法，知道哪个人脸可以登录
    count = 0
    isExit = False
    while True:
        flag, frame = cap.read()
        if flag == False:
            break
        gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
        face_zones = face_detector.detectMultiScale(gray, scaleFactor=1.2,
                                                    minNeighbors=5,
                                                    minSize=(80, 80),
                                                    maxSize=(320, 320))
        for x, y, w, h in face_zones:
            face = gray[y:y + h, x:x + w]
            face = cv2.resize(face, (128, 128))
            #均衡化
            face = cv2.equalizeHist(face)
            #预测，返回标签和置信度
            label, confidence = face_recognizer.predict(face)
            print('--------------', label, confidence)
            cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=[0, 0, 255], thickness=2)
            user = User.query.filter_by(num=label).first()
            if(user==None):
                break
            if label == -1.:  # 等于-1没有找到这个人
                print('----------------刷脸登陆登陆失败---------------------')
                time.sleep(2)
                count += 1

            elif label == user.num:  # 验证成功
                # print('+++++++++++++++++++++刷脸登陆++++++++++++++++++++++++')
                # v = cv2.VideoCapture('user/config/ttnk.mp4')
                # while True:
                #     flag, frame = v.read()
                #     if flag == False:
                #         isExit = True
                #         break
                #     cv2.imshow('face', frame)
                #     cv2.waitKey(1000 // 24)
                isExit = True
                break
            else :
                return render_template('login.html', error="登录失败")
        if count >= 3:
            break
        if isExit:
            break
        cv2.imshow('登录中...', frame)
        key = cv2.waitKey(1000 // 24)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    if(isExit==True):
        session['uid'] = user.id
        # 根据用户的状态去显示用户信息
        return redirect('/user/info')
    else:
        return render_template('login.html',error="登录失败")


