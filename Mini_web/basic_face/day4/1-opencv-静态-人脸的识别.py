# 提前将人脸保存好了，训练识别
#人脸检测（是不是人脸） 和人脸识别（人脸是谁）不是一回事儿
import cv2
import numpy as np
import os
def load_faces():
    # os这个库列出来faces（每个人名字命名的文件夹）文件夹下有哪些文件夹
    dirs = os.listdir('./faces')
    # 声明接收的对象，变量
    X_color = []
    X = []
    y = []
    target_names = {} #字典，数字和人名对应关系
    for label,name in enumerate(dirs):#枚举，Python中的一个方法
        for i in range(1,31):
            face = cv2.imread('./faces/%s/%d.jpg' % (name, i))
            X_color.append(face) # 彩色人脸
            gray = cv2.cvtColor(face,code = cv2.COLOR_BGR2GRAY)
            X.append(gray) # 黑白人脸
            y.append(label) # 目标值，用数字表示
        target_names[label] = name.split('_')[0] # 名字和标签、目标值对应，记录
    return np.asarray(X_color),np.asarray(X),np.asarray(y),target_names

# 这个方法，作用：拆分数据，两份（训练，验证、测试）
def split_data(X_color,X,y):# 参数传递，方法，收到‘鸡毛信’
    index = np.arange(240)
    np.random.shuffle(index)  # shuffle 洗牌的意思，打乱顺序
    train = index[:180]  # 前180个样本作为训练数据，现在是索引
    test = index[180:]  # 后60个样本作为验证数据，也是索引
    X_color_train, X_color_test = X_color[train], X_color[test]  # 彩色人脸的划分
    X_train, X_test = X[train], X[test]  # 黑白人脸
    y_train, y_test = y[train], y[test]  # 人脸的目标值，是谁
    return X_color_train,X_color_test,X_train,X_test,y_train,y_test


def create_model():
    # face_recognizer = cv2.face.EigenFaceRecognizer_create()
    # face_recognizer = cv2.face.FisherFaceRecognizer_create()
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    return face_recognizer

# 第二个进行了代码重构
if __name__ == '__main__':
    # 1、数据加载
    X_color,X,y,target_names = load_faces() # 样本量是240个
    # 2、拆分，一分为二：训练数据train，另一个测试数据test（验证数据，保留数据）
    X_color_train,X_color_test,X_train,X_test,y_train,y_test = \
        split_data(X_color,X,y) # 参数传递
    # 3、加载算法，人脸识别的算法，进行训练
    face_recognizer = create_model()
    # 4、训练算法
    # X_train是黑白图片的数据，y_train,目标值；train，训练
    # 算法找规律，其实就是数学运算！（强基计划）
    face_recognizer.train(X_train,y_train) # 找规律
    # 5、验证算法
    # 这段代码存在一定问题！！！
    # y_ = face_recognizer.predict(X_test) # 一次只能预测一张图片
    cv2.namedWindow('face',flags=cv2.WINDOW_NORMAL) # 创建了一般的窗口
    cv2.resizeWindow('face',192,192) # 窗口尺寸，放大了
    for face,face_color in zip(X_test,X_color_test):# for循环遍历取出人脸数据，黑白图片
        # label就是标签，confidence置信度（越小距离越近，越相似，越是同一个人）
        label,confidence = face_recognizer.predict(face)
        print('-----------------',label,target_names[label],confidence)
        cv2.putText(face_color,target_names[label],(0,15),
                    cv2.FONT_HERSHEY_PLAIN,1.0,
                    [0,0,255],2)
        cv2.imshow('face',face_color)
        q = cv2.waitKey(10000)
        if q == ord('q'):
            break
    cv2.destroyWindow('face')