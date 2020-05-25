import numpy as np
# SVC分类，定性（吃不吃）
from sklearn.svm import SVR # 定量（吃多少），回归算法，预测后面销量是多少
import matplotlib.pyplot as plt

if __name__ == '__main__':
    X = np.arange(2009,2020) # 左闭右开取不到2020 ,X的数值偏大，缩放
    # X - 2008
    X = X - 2008
    y = np.array([0.5,9.36,52,191,352,571,912,1207,1682,2135,2684])

    svr = SVR(kernel='poly',degree=3,coef0=1.0) # degree,几次幂

    svr.fit(X.reshape(-1,1),y)

    # 2020年销量 2020 - 2008 = 12
    sale_2020 = svr.predict([[12]])
    print('-----------------------天猫双十一2020销量是：',sale_2020)
    plt.scatter(X,y)
    plt.scatter(12,sale_2020,c = 'red')

    x = np.linspace(1,13,100).reshape(-1,1)
    y = svr.predict(x)
    plt.plot(x,y,color = 'green')
    plt.show()