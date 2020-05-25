import cv2
if __name__ == '__main__':
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    v = cv2.VideoCapture(0) # 摄像头，设置权限，程序调用摄像头，允许
    num = 1
    isWrite = False# 标志，告诉代码，是否存储
    while True:
        flag,frame = v.read()
        if flag == False:
            break
        gray = cv2.cvtColor(frame,code = cv2.COLOR_BGR2GRAY)
        face_zones = face_detector.detectMultiScale(gray,
                                                    scaleFactor=1.3,
                                                    minNeighbors=10)
        for x,y,w,h in face_zones:
            if isWrite:
                face = frame[y:y+h,x:x+w]
                # 保存人脸,% Python语言字符串格式化%d 代表数字
                face = cv2.resize(face,dsize = (64,64))
                cv2.imwrite('./lfk_faces/%d.jpg'%(num),face)
                num +=1
            if num ==31:
                break
            cv2.rectangle(frame,pt1 = (x,y),pt2 = (x+w,y+h),color=[0,0,255],thickness=2)
        if num == 31:
            break
        cv2.imshow('face',frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
        if key == ord('w'):#指令，告诉计算机，开始写入
            isWrite = True
    cv2.destroyAllWindows()
    v.release()