import cv2
if __name__ == '__main__':
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    eye_detector = cv2.CascadeClassifier('./haarcascade_eye_tree_eyeglasses.xml')
    v = cv2.VideoCapture(0)#如果给0，打开本机的摄像头
    while True:
        flag,frame = v.read()
        if flag == False:
            break
        gray = cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY)
        face_zones = face_detector.detectMultiScale(gray)

        for x,y,w,h in face_zones:#绘制成矩形，人脸
            cv2.rectangle(frame,pt1 = (x,y),pt2 = (x+w,y+h),
                          color = [0,0,255],thickness=2)
            eye_zones = eye_detector.detectMultiScale(gray[y:y+h,x:x+w])  # 整张图片，眼睛在人脸中
            for x1, y1, w1, h1 in eye_zones:
                cv2.circle(frame, center=(x + x1 + w1 // 2,y + y1 + h1 // 2),
                           radius=h1 // 2,
                           color=[0, 0, 255],
                           thickness=2)
        cv2.imshow('face',frame)
        q = cv2.waitKey(1000//24)
        if q == ord('q'):
            break
    cv2.destroyAllWindows()
    v.release()