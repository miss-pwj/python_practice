import cv2
if __name__ == '__main__':
    face = cv2.imread('jin.jpg')
    # 根据特征，进行识别的，人脸的特征，特征文件
    # haar抽取图片特征的方式
    # 给算法，什么样的特征，识别什么样的目标区域。对于计算机而言，没有’脸‘概念，只知道特征
    # 人脸检测器
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')# Cascade 级联、组合；classifier分类
    # 人脸检测器，检测出来的人脸区域
    face_zones = face_detector.detectMultiScale(face) # 多张，可以检测，人脸大，人脸小
    print('------------------',face_zones)
    # 把人脸进行标记
    for x,y,w,h in face_zones:
        # color 蓝绿红 [0,0,255] 大红色
        cv2.rectangle(face,pt1=(x,y),pt2=(x + w,y+h),
                      color = [0,0,255],
                      thickness=2)#矩形
    cv2.imshow('face',face)
    cv2.waitKey(0)
    cv2.destroyAllWindows()