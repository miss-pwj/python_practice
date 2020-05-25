import cv2
import numpy as np
import os
def load_faces():
    # 已经注册的人脸用户
    faces = os.listdir('./face_certification2')
    X = np.asarray([cv2.cvtColor(cv2.imread('./face_certification2/'+face),
                                 code = cv2.COLOR_BGR2GRAY)
                    for face in faces])
    y = np.asarray([int(face.split('.')[0]) for face in faces]) # 1,2,3,4
    return X,y
def load_face_login(): # 加载图片数据可以了，没必要获取类别y这个值。
    faces = os.listdir('./face_login')
    X = np.asarray([cv2.cvtColor(cv2.imread('./face_login/'+face),code=6) for face in faces])
    return X
if __name__ == '__main__':
    # 1、加载数据
    X,y = load_faces()
    # 2、训练模型
    face_recognizer = cv2.face.LBPHFaceRecognizer_create(threshold = 100)
    face_recognizer.train(X,y)
    # 3、模拟登陆，获取人脸图片，获取登陆的人脸
    faces = load_face_login()
    # 4、验证
    for face in faces:
        label,confidence = face_recognizer.predict(face)
        print('-----------------',label,confidence)
        cv2.imshow('certification',face)
        key = cv2.waitKey(0)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()