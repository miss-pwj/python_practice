import numpy as np
import cv2
import os
import joblib
target_names = ['hyw', 'lfk', 'lsh', 'wlk', 'xyk', 'zhj', 'zlp', 'zx']
def recognize_face(knn):
    # 使用这个模型，进行预测
    faces = os.listdir('./faces')
    # 此时数据X是列表，方法不多
    X_color = [cv2.imread('./faces/' + face) for face in faces]
    X_gray = [cv2.cvtColor(face, code=cv2.COLOR_BGR2GRAY) for face in X_color]
    # 将列表转换成了，numpy数组，功能强大了
    X_gray = np.asarray(X_gray).reshape(4, -1)  # 负一倒着数
    y_ = knn.predict(X_gray)
    cv2.namedWindow('face', flags=cv2.WINDOW_NORMAL)
    cv2.resizeWindow('face', 192, 192)
    for face, i in zip(X_color, y_):
        cv2.putText(face, target_names[i], (0, 15), cv2.FONT_ITALIC, 0.8, [0, 0, 255], 1)
        cv2.imshow('face', face)
        cv2.waitKey(2000)
    cv2.destroyWindow('face')
def recognizer_face2(knn):
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    face = cv2.imread('./face3.jpg')
    gray = cv2.cvtColor(face, code=cv2.COLOR_BGR2GRAY)
    face_zones = face_detector.detectMultiScale(gray)
    for x, y, w, h in face_zones:
        face_color = face[y:y + h, x:x + w]
        face = gray[y:y + h, x:x + w]
        face = cv2.resize(face, (64, 64))  # 一个人脸，64*64
        y_ = knn.predict(face.reshape(1, 64 * 64))  # 预测返回值是列表
        cv2.putText(face_color, target_names[y_[0]], (0, 35), cv2.FONT_ITALIC, 1.5, [0, 0, 255], 2)
        cv2.imshow('face', face_color)
        cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    # 加载之前保留的模型
    knn = joblib.load('./face_recognizer')
    # recognize_face(knn)
    recognizer_face2(knn)