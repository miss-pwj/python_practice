import numpy as np
import os
import cv2
import time
def take_face():
    cap = cv2.VideoCapture(0) # 打开摄像头
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml') # 识别人脸
    isFace = False # 告诉我们是否检测出了人脸
    while True:
        flag,frame = cap.read()
        gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
        face_zones = face_detector.detectMultiScale(gray,
                                                    scaleFactor=1.2,
                                                    minNeighbors=5,
                                                    minSize=(80,80),
                                                    maxSize=(320,320))
        for x,y,w,h in face_zones:
            isFace = True
            face = frame[y+1:y+h,x+1:x+w] # 彩色人脸
            cv2.rectangle(frame,pt1 = (x,y),pt2 = (x+w,y+h),color = [0,0,255],thickness=1)
        if isFace:
            cv2.imshow('face',face)# 有人脸，显示人脸
        else:
            cv2.imshow('face',frame) # 没有人脸，显示画面
        key = cv2.waitKey(2000)
        isFace = False
        if key == ord('q'):
            break
        elif key == ord('w'):# 说明采集的人脸，自己比较满意， 保存一下
            os.makedirs('./face_certification',exist_ok=True)
            filename = os.listdir('./face_certification')
            num = len(filename)
            face = cv2.cvtColor(face,code = cv2.COLOR_BGR2GRAY) # 灰度化处理
            face = cv2.resize(face,dsize = (128,128)) # 尺寸调整
            face = cv2.equalizeHist(face) # 均衡化
            cv2.imwrite('./face_certification/%d.jpg'%(num),face) # 保存图片
            break
    cv2.destroyAllWindows()
    cap.release()
def login():
    cap = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    face_recognizer = cv2.face.LBPHFaceRecognizer_create(threshold = 200) # 训练
    faces = os.listdir('./face_certification') # 列表
    X = np.asarray([cv2.imread('./face_certification/'+face)[:,:,0] for face in faces])
    y = np.asarray([int(face.split('.')[0]) for face in faces])
    face_recognizer.train(X,y) # train，算法，知道哪个人脸可以登录
    count = 0
    isExit = False
    while True:
        flag,frame = cap.read()
        if flag == False:
            break
        gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
        face_zones = face_detector.detectMultiScale(gray, scaleFactor=1.2,
                                                    minNeighbors=5,
                                                    minSize=(80, 80),
                                                    maxSize=(320, 320))
        for x,y,w,h in face_zones:
            face = gray[y:y+h,x:x+w]
            face = cv2.resize(face,(128,128))
            face = cv2.equalizeHist(face)
            label,confidence = face_recognizer.predict(face)
            print('--------------',label,confidence)
            cv2.rectangle(frame,pt1=(x,y),pt2=(x+w,y+h),color = [0,0,255],thickness=2)
            if label == -1:# 等于-1没有找到这个人
                print('----------------刷脸登陆登陆失败---------------------')
                time.sleep(2)
                count +=1
            else:  # 验证成功
                print('+++++++++++++++++++++刷脸登陆++++++++++++++++++++++++')
                v = cv2.VideoCapture('./ttnk.mp4')
                while True:
                    flag, frame = v.read()
                    if flag == False:
                        isExit = True
                        break
                    cv2.imshow('face', frame)
                    cv2.waitKey(1000 // 24)
        if count >=3:
            break
        if isExit:
            break
        cv2.imshow('face',frame)
        key = cv2.waitKey(1000//24)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    # 采集人脸，手机刷脸登陆为例子（人脸登陆，采集人脸）
    # take_face()

    # 验证人脸通过，播放视频，opencv播放视频，无声的视频
    # 登陆，页面跳转，进入个人首页,登陆是动态登陆（调用了摄像头）
    login()