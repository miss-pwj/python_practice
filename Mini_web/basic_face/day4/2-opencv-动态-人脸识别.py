# 打开摄像头（实时采集人脸），识别这个人是谁
# 特别像，12306验票进站，办理身份证，相片留存在公安部
# 验票进站时，摄像头，采集人脸，比对，看看和你办理身份证时的照片是否一致
# 一致，放行
# 不一致，人工复检
# 智能家居
import numpy as np
import cv2
import os
def load_faces():
    dirs = os.listdir('./faces')
    X_color = [] # 存放彩色图片
    X_gray = [] # 存放黑白图片
    y = [] # 目标值
    target_names = {} # 人名和数字对应
    for j,name in enumerate(dirs):
        for i in range(1,2): # 每个人加载一张图片，相当于有一张图片进行比对！
            face = cv2.imread('./faces/%s/%d.jpg'%(name,i))
            X_color.append(face)
            gray = cv2.cvtColor(face,code = cv2.COLOR_BGR2GRAY)
            # 使用cv2中的操作，实现图片的均衡化，效果更好,图片明暗对比鲜明
            equal_gray = cv2.equalizeHist(gray)
            X_gray.append(equal_gray)
            y.append(j) # 数字代表目标值
        target_names[j] = name.split('_')[0] #字典代表名字和数字对应关系
    return np.asarray(X_color),np.asarray(X_gray),np.asarray(y),target_names
def recognize_face(face_recognizer, target_names):
    cap = cv2.VideoCapture(0)
    detector_face = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    while True:
        flag,frame = cap.read()
        if flag == False :
            break
        gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
        face_zones = detector_face.detectMultiScale(gray,scaleFactor=1.2,
                                                    minNeighbors=10) # 人脸检测
        for x, y, w, h in face_zones:
            face = gray[y:y+h,x:x+w] # 人脸切割
            face = cv2.resize(face,(64,64)) # 缩放
            face = cv2.equalizeHist(face) # 均衡化
            label, confidence = face_recognizer.predict(face) # 识别
            print('-----------置信度(表示距离，越小越好)：',confidence)
            name = target_names[label]
            cv2.rectangle(img = frame,pt1=(x,y),pt2=(x+w,y+h),
                          color = [0,0,255],thickness=2)
            if confidence > 130:
                # 不允许登陆，登陆事变
                # 密码登陆，密码不对，提示，失败
                cv2.putText(frame,'unknown',(x,y),cv2.FONT_HERSHEY_PLAIN,2.0,[0,0,255],2)
            else:
                # 登陆成功，跳转
                # 密码正确，登陆成功
                cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_PLAIN, 3.0, [0, 0, 255], 2)
        cv2.imshow('face',frame)
        key = cv2.waitKey(1000//24)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()
def main():
    # 1、实现数据加载
    X_color, X_gray, y, target_names = load_faces()
    # 动态识别人脸，所有，现在不需要拆分，将240张人脸全部拿来训练
    # 验证数据，打开摄像头，采集的人脸
    # 2、声明算法
    face_recognizer = cv2.face.LBPHFaceRecognizer_create() # 特征，纹理特征
    # face_recognizer = cv2.face.EigenFaceRecognizer_create() # 特征，PCA降维特征
    # face_recognizer = cv2.face.FisherFaceRecognizer_create() # 特征，LDA降维特征
    # 3、训练
    face_recognizer.train(X_gray, y)
    # 4、调用摄像头，检测人脸 + 识别人脸
    recognize_face(face_recognizer, target_names)
# 代码重构
if __name__ == '__main__':
    main()