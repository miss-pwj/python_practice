import cv2
if __name__ == '__main__':
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    v = cv2.VideoCapture(0)#如果给0，打开本机的摄像头
    while True:
        flag,frame = v.read()
        if flag == False:
            break
        gray = cv2.cvtColor(frame,code=cv2.COLOR_BGR2GRAY)
        face_zones = face_detector.detectMultiScale(gray)
        for x,y,w,h in face_zones:
            cv2.circle(frame,center=(x+w//2,y+h//2),
                       radius=h//2,
                       color=[0,0,255],
                       thickness=2)
        cv2.imshow('face',frame)
        q = cv2.waitKey(1000//24)
        if q == ord('q'):
            break
    cv2.destroyAllWindows()
    v.release()