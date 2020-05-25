import numpy as np
import cv2
# 梯度提升树（一点点改善，效果），多颗树，构建的集成学习模型
# 三个臭皮匠赛过诸葛亮
from sklearn.ensemble import GradientBoostingClassifier
# model_selection 模型选择
from sklearn.model_selection import train_test_split # 拆分
target_names = ['hyw', 'lfk', 'lsh', 'wlk', 'xyk', 'zhj', 'zlp', 'zx']
def face_classifier():
    # 1、加载数据
    face_color,face_gray,face_label = np.load('./faces_color.npy'),np.load('./faces_gray.npy'),np.load('./faces_label.npy')

    # 2、实现数据切分
    # 进行训练的数据用X表示，和训练数据对应的目标值使用y表示，约定俗称的
    # 构建算法模型，其实算法模型就是 数学方程，公式
    face_color_train,face_color_test,X_train,X_test,y_train,y_true = \
        train_test_split(face_color,face_gray,face_label,test_size=0.2)
    print(face_gray.shape)
    print(X_train.shape)
    print(X_test.shape)

    # 3、创建模型，随机森林，包含多颗树，每棵树，都是上一个代码中DecesionTreeClassifier
    # 随机森林，指定，使用多少树
    # 每颗树互不相干，独立训练，预测返回结果：
    # 98返回值是类别1；1颗树返回类别2,1颗树返回类别5
    # 98 > 1，统计分析，类别选取多数。
    clf = GradientBoostingClassifier(n_estimators=100) # 包含100颗决策树，群策群力

    # 4、训练,sklearn中这些算法，都是fit训练，调用predict进行预测
    # sklearn中算法，对数据形式有要求二维：[[样本一特征],[样本二特征],[样本三特征],……]
    # 计算机，不能看，不能听，不能想，只能计算，统计分析，返回结果
    # 算法  == 数学 + 统计学
    clf.fit(X_train.reshape(192,-1),y_train) # X_train是黑白图片，y_train是图片标签

    # 5、使用模型，进行预测
    y_pred = clf.predict(X_test.reshape(48, -1))

    # 6、计算准确
    accuracy = (y_true == y_pred).mean()
    print('集成算法梯度提升树准确率：',accuracy)

    # 7、可视化，结果
    cv2.namedWindow('face',flags=cv2.WINDOW_NORMAL)
    cv2.resizeWindow('face',192,192)
    for i,face in enumerate(face_color_test):
        cv2.putText(face,target_names[y_pred[i]],(0,35),cv2.FONT_ITALIC,1.0,[0,0,255],1)
        cv2.imshow('face',face)
        cv2.waitKey(2000)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    #人脸的分类
    face_classifier()