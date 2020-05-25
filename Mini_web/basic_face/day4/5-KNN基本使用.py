import numpy as np
# sklearn中叫:KNeighborsClassifier 分类器，分类
# opencv中叫:CascadeClassifier
# 他俩的作用,都是分类
from sklearn.neighbors import KNeighborsClassifier
import cv2
import os
from sklearn.externals import joblib # job工作、算法，lib图书馆
def load_faces():
    faces = os.listdir('./faces')
    X_color = []
    X_gray = []
    y = []
    target_names = {} # Python一种基本数据类型
    for i,name in enumerate(faces):
        for j in range(1,31):
            face = cv2.imread('./faces/%s/%d.jpg'%(name,j))
            X_color.append(face)
            gray = cv2.cvtColor(face, code=cv2.COLOR_BGR2GRAY)
            X_gray.append(gray)
            y.append(i) # 标签，目标值，数字表示代替他
        target_names[i] = name.split('_')[0]
    return np.asarray(X_color),np.asarray(X_gray),np.asarray(y),target_names
def split_faces(X_color, X_gray, y):
    index = np.arange(240)
    np.random.shuffle(index)
    # 训练数据和测试数据的索引
    train = index[:200]
    test = index[-40:]
#     根据索引，取出特定的数据
    X_color_train,X_color_test = X_color[train],X_color[test] # 彩色人脸
    X_gray_train,X_gray_test = X_gray[train],X_gray[test] # 黑白人脸
    # 无论，彩色人脸还是黑白人脸，对应的目标值是同一个y
    y_train,y_test = y[train],y[test]
    return X_color_train,X_color_test,X_gray_train,X_gray_test,y_train,y_test
if __name__ == '__main__':
    # 1、第一步，加载数据，其中y就是目标值，也是真实值
    X_color,X_gray,y,target_names = load_faces()
    # 1.2、保存numpy数组
    np.save('./faces_color',X_color)
    np.save('./faces_gray',X_gray)
    np.save('./faces_label',y)
    # 2、拆分数据，一个部分是训练（200个），另一部分验证（40个）
    X_color_train,X_color_test,X_gray_train,X_gray_test,y_train,y_test =split_faces(X_color,X_gray,y)
    # 3、声明算法,knn,k个邻居，要给算法，数据找到k个邻居，k是多少呢？
    # 人为定义
    knn = KNeighborsClassifier(n_neighbors=5) # k 小于样本数量的开平方 200个开平方14~15
    # 4、训练算法
    print('---------------------------',X_gray_train.shape)
    knn.fit(X_gray_train.reshape(200,-1),y_train) # fit 健身

    # 4.2、将训练好的算法保存一下，算法 == 模型 == 估计（estimator） == 分类器
    joblib.dump(knn,filename='./face_recognizer')


    #5、算法预测，之所以使用y_约定俗成
    # 之前opencv中算法，一次只能预测一张人脸
    # KNN这个算法，批量的预测数据
    y_ = knn.predict(X_gray_test.reshape(40,-1))
    print('预测值：',y_) # 标签
    # 6、计算一下准确率
    # 真实值 y_test
    print('真实值：',y_test)
    accuracy = (y_test == y_).mean() # True = 1,False = 0
    print(accuracy)
    # 7、可视化
    cv2.namedWindow('face',flags=cv2.WINDOW_NORMAL)
    cv2.resizeWindow('face',192,192)
    for face,y1,y2 in zip(X_color_test,y_,y_test):#y_是，算法预测值
        if y1 == y2:#预测准确，颜色显示成绿色
            cv2.putText(face,# 图片
                        target_names[y1],# 文本
                        (0,15),#坐标
                        cv2.FONT_HERSHEY_PLAIN,#字体
                        1,#字体缩放
                        [0,255,0],#颜色
                        2)#字体粗细
        else:#预测失败
            cv2.putText(face,  # 图片
                        target_names[y1],  # 文本
                        (0, 15),  # 坐标
                        cv2.FONT_HERSHEY_PLAIN,  # 字体
                        1,  # 字体缩放
                        [0, 0, 255],  # 颜色
                        2)  # 字体粗细
        cv2.imshow('face',face)
        key = cv2.waitKey(1000)
        if key == ord('q'):
            break
    cv2.destroyWindow('face')