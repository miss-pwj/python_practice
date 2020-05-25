import numpy as np
import cv2
# SVM support vector machine 支持向量机
# 向量：具有大小和方向的量
from sklearn.svm import SVC
import matplotlib.pyplot as plt
# sklearn中数据集
import sklearn.datasets as datasets
if __name__ == '__main__':
    # X是数据，两个特征（横纵坐标表示），画图可以显示，
    # y是目标值，标签，结果，两类：0表示一类，1表示一类
    # random_state随机数装态，控制随机数，固定值，每次生成值，就是固定
    # cluster_std 标准差，越大，数据越离散
    X,y = datasets.make_blobs(n_samples=100,n_features=2,centers=2,cluster_std=2.5,
                              random_state=128)
    # 点：横纵坐标；描颜色，c = y(y类别，就两种类别，0、1:0代表一种颜色，1代表另一种颜色)

    # 'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'
    svc = SVC(kernel='linear')#kernel 核函数，将原始数据，进行某种处理

    svc.fit(X,y)

    # f = x*w1 + y*w2 + b
    # 0 = x*w1 + y*w2 + b
    # y*w2 = -w1*x - b
    # f(x) = y = -w1/w2*x - b/w2
    w_ = svc.coef_ # 系数，方程有系数，特征权重，特征两个x1，x2 可以表示x,y
    b_ = svc.intercept_ # 截距，方程有截距
    w = -w_[0,0]/w_[0,1]
    b = -b_[0]/w_[0,1]

    x = np.linspace(-3,3,100) # 等差数列
    plt.plot(x,x*w + b,color = 'red') # 绘制线

    print(w_,b_)

    # 算法中，提到支持向量，请问什么是支持向量？
    # 支持向量，支持，分类边界的划分
    # 支持向量，两类点最最边缘的点
    sv = svc.support_vectors_
    plt.scatter(X[:,0],X[:,1],c = y) # 散点图
    plt.scatter(sv[:,0],sv[:,1],s = 100,c = 'green')
    plt.show()