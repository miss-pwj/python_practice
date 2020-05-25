import cv2

if __name__ == '__main__':
    v = cv2.VideoCapture('./ttnk.mp4')
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    num = 1
    while True:
        flag,frame = v.read()#frame帧，图片
        if flag == False:
            break
        gray = cv2.cvtColor(frame,code = cv2.COLOR_BGR2GRAY)
        # minSize 限制检索人脸的最小尺寸
        face_zones = face_detector.detectMultiScale(gray,
                                                    minSize = (80,80))
        for x,y,w,h in face_zones:
            face = frame[y:y+h,x:x+w]
            cv2.imwrite('./lfk_faces/%d.jpg'%(num),face)
            num += 1
            cv2.circle(frame,center = (x + w//2,y + w//2),radius=h//2,color = [0,0,255])
        cv2.imshow('face',frame)
        q = cv2.waitKey(10)
        if q == ord('q'):
            break
    cv2.destroyAllWindows()
    v.release()
