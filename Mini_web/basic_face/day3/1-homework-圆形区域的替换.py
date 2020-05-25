import cv2
if __name__ == '__main__':
    # 人脸的检测器
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    cap = cv2.VideoCapture(0) # Ctrl + alt + v
    while True:
        flag,frame = cap.read()
        if flag == False:
            break
        gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)#黑白
        face_zones = face_detector.detectMultiScale(gray)#检测人脸
        for x,y,w,h in face_zones:#获取人脸坐标，宽度，高度
            wc = cv2.imread('./head.png')
            wc = cv2.resize(wc,dsize = (w,h))
            # frame[y:y+h,x:x+w] = wc # 这一行代码，进行了人脸的替换，全部替换
            # i是从0开始的，相对坐标系，就是人脸区域
            for i in range(w):#两层for循环，就是遍历图片中所有的像素
                for j in range(h):#图片既有高度，也有宽度
                    if ((i - w/2)**2)/1.5 + ((j  - h/2)**2)< ((w/2)**2)/1.5:#椭圆
                        frame[y+i,x+j] = wc[i,j] # 一个像素一个像素，进行替换
        cv2.imshow('wangcai',frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()