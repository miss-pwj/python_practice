#人脸检测（是不是人脸） 和人脸识别（人脸是谁）不是一回事儿
import cv2
import numpy as np
import os
def load_faces():
    dirs = os.listdir('./faces')
    X_color = []
    X = []
    y = []
    target_names = {} #字典，数字和人名对应关系
    for label,name in enumerate(dirs):#枚举，Python中的一个方法
        for i in range(1,31):
            face = cv2.imread('./faces/%s/%d.jpg' % (name, i))
            X_color.append(face)# 彩色人脸
            gray = cv2.cvtColor(face,code = cv2.COLOR_BGR2GRAY)
            X.append(gray) # 黑白人脸
            y.append(label) # 目标值，用数字表示
        target_names[label] = name.split('_')[0]
    return np.asarray(X_color),np.asarray(X),np.asarray(y),target_names
if __name__ == '__main__':
    # 1、数据加载
    X_color,X,y,target_names = load_faces() # 样本量是240个
    # 2、拆分，一分为二：训练数据train，另一个测试数据test（验证数据，保留数据）
    index = np.arange(240)
    np.random.shuffle(index) # shuffle 洗牌的意思，打乱顺序
    train = index[:180] # 前180个样本作为训练数据，现在是索引
    test = index[180:] # 后60个样本作为验证数据，也是索引
    X_color_train,X_color_test = X_color[train],X_color[test] # 彩色人脸的划分
    X_train,X_test = X[train],X[test] # 黑白人脸
    y_train,y_test = y[train],y[test] # 人脸的目标值，是谁
    # 3、加载算法，人脸识别的算法，进行训练
    # face_recognizer = cv2.face.EigenFaceRecognizer_create()
    # face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # 4、训练算法
    # reshape 形状改变，数据不变，行传改变 [180,4096]
    face_recognizer.train(X_train,y_train) # X_train是黑白图片的数据，y_train,目标值
    # 5、验证算法
    # 这段代码存在一定问题！！！
    y_ = face_recognizer.predict(X_test)
    print(y_)