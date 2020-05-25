import cv2
# 通过参数调整，将一张图片中，多张人脸检测出来
if __name__ == '__main__':
    img = cv2.imread('./img4.jpg') # 彩色图片占有内存大
    # 变成黑白，占有内存比较小,尺寸不变
    gray = cv2.cvtColor(img,code = cv2.COLOR_BGR2GRAY) # 6就对应这，bgr2gray
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    # 人脸区域，位置在彩色或者黑白位置固定的
    face_zones = face_detector.detectMultiScale(gray,
                                                scaleFactor = 1.05,
                                                minNeighbors=3)
    for x,y,w,h in face_zones: # w == h算法返回人脸区域正方形
        # cv2.rectangle(img,pt1=(x,y),pt2=(x+w,y+h),color = [0,0,255],thickness=2)
        cv2.circle(img,center = (x+w//2,y +h//2),radius=w//2,color = [0,0,255],thickness=2)
    cv2.imshow('face',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()