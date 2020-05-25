import numpy as np
from sklearn.tree import DecisionTreeClassifier
# 可以将数据一分为二：训练和测试
from sklearn.model_selection import train_test_split
import cv2
from sklearn.metrics import accuracy_score # 见名知意，accuracy（准确率），score得分

def load_data():
    # 列表，自然索引：0,1,2,3,4,5,6,7
    target_names = ['hyw', 'lfk', 'lsh', 'wlk', 'xyk', 'zhj', 'zlp', 'zx']
    faces_color = np.load('./faces_color.npy')
    faces_gray = np.load('./faces_gray.npy')
    faces_label = np.load('./faces_label.npy')
    return faces_color, faces_gray, faces_label,target_names


if __name__ == '__main__':
    # 1、加载数据
    faces_color, faces_gray, faces_label,target_names = load_data()

    # 2、数据拆分，sklearn提供了方法，和之前数据拆分一样的
    # 拆分完之后，数据依然是一一对应
    faces_color_train,faces_color_test,\
    faces_gray_train,faces_gray_test,\
    faces_label_train,y_true = train_test_split(faces_color,faces_gray,faces_label,test_size=0.25)
    print(faces_color_train.shape)
    print(faces_gray_train.shape) # shape = (180,64,64) 三维的
    print(faces_label_train.shape)

    # 3、生成模型
    clf = DecisionTreeClassifier(max_depth=10)

    # 4、训练了，和昨天KNN使用方式完全一样的
    # sklearn中算法，对数据的结构有要求的，必须是二维的
    clf.fit(faces_gray_train.reshape(180,4096),faces_label_train)

    # 5、预测
    y_pred = clf.predict(faces_gray_test.reshape(60,-1))
    print('算法预测的结果：',y_pred)
    print('是数据保留结果: ',y_true) # 真实类别 label就是标签，标签是名字对应的类别
    print('第一种计算准确率方式：',(y_pred == y_true).mean())
    print('第二种准确率计算方式：',clf.score(faces_gray_test.reshape(-1,4096),y_true))
    print('第三种准确率计算方式：',accuracy_score(y_true,y_pred))

    # 6、可视化
    cv2.namedWindow('face',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('face',192,192)
    for i,face in enumerate(faces_color_test):
        if y_true[i] == y_pred[i]:
            cv2.putText(face,target_names[y_pred[i]],(0,30),cv2.FONT_ITALIC,1.0,[0,255,0],2)
        else:
            cv2.putText(face,target_names[y_pred[i]],(0,30),cv2.FONT_ITALIC,1.0,[0,0,255],2)
        cv2.imshow('face',face)
        key = cv2.waitKey(1000)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
