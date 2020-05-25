# 算法，进行分类
# 标记，记号
import cv2
import os
import numpy as np # 数字化Python numeric Python：数组，提供很多便捷方法，功能强大！
# 1、进行数据处理,将图片（尺寸比较大）-------->缩放到合适的尺寸了
def prepare():
    num = 1
    dirs = os.listdir('./faces/zhj_faces') # os系统，列出当前文件夹下所有的文件
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    for file in dirs:
        img = cv2.imread('./faces/zhj_faces/'+file)
        face_zones = face_detector.detectMultiScale(img,scaleFactor=1.05,minNeighbors=1)
        for x,y,w,h in face_zones:
            face = img[y:y+h,x:x+w]
            face = cv2.resize(face,dsize=(64,64))
            cv2.imwrite('./faces/zhj2_faces/%d.jpg'%(num),face)
            num += 1
    cv2.destroyAllWindows()

# 2、进行数据的加载
def load_img():
    dirs = os.listdir('./faces')#每个人的人脸文件夹，获取到了
    X_color = [] # 原始数据，彩色数据
    X = [] # 数据
    y = [] # 目标值，图片对应哪个名字
    for dir in dirs:
        for i in range(1,31):#左闭右开
            img = cv2.imread('./faces/%s/%d.jpg'%(dir,i))
            # 黑白变换，数据量减少了2/3
            gray = cv2.cvtColor(img,code = cv2.COLOR_BGR2GRAY)
            X_color.append(img) # 原数据，彩色图片
            X.append(gray) # 黑白
            y.append(dir.split('_')[0])
    # np.asarray() 数据不变的，对象发生了变化，列表[] ----->numpy数组
    return np.asarray(X_color),np.asarray(X),np.asarray(y)

if __name__ == '__main__':
    # prepare() # 数据整理，图片规整 飘红，按万能键：Alt + Enter

    #为什么进行列表------->numpy数组的转换，因为：numpy数组功能强大！
    # l = [1,1,2,3,4,5,6]
    # print(l,type(l),l.sum())
    # nd = np.asarray(l)
    # print(nd,type(nd),nd.sum(),nd.mean(),nd.std())
    # 数据加载
    X_color,X,y = load_img()
    print(X_color.shape)
    print(X.shape)
    print(y.shape)
    for i,img in enumerate(X_color):
        cv2.putText(img,
                    y[i],  # 名字
                    (0, 12),  # 位置
                    cv2.FONT_HERSHEY_PLAIN,  # 字体
                    1.2,  # 字体缩放
                    [0, 0, 255],  # 字体颜色
                    2)  # 字体的粗细
        cv2.imshow('face',img)
        cv2.waitKey(100)
        print('--------------',i)
    cv2.destroyAllWindows()
