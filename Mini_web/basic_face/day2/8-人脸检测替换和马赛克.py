import cv2
if __name__ == '__main__':
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    cap = cv2.VideoCapture(0) # Ctrl + alt + v

    while True:
        flag,frame = cap.read()
        if flag == False:
            break
        face_zones = face_detector\
            .detectMultiScale(cv2.cvtColor(frame,
                                           code=cv2.COLOR_BGR2GRAY))
        for x,y,w,h in face_zones:
            wc = cv2.imread('./head.png')
            wc = cv2.resize(wc,dsize = (w,h))
            frame[y:y+h,x:x+w] = wc
            # face = frame[y:y+h,x:x+w]
            # step = 10
            # face = face[::step, ::step] # 每隔step个取一个数据，像素变少，图片模糊，马赛克图片
            # fh,fw = face.shape[:2]#压缩之后，人脸的高度和宽度
            # for i in range(fh):
            #     for j in range(fw):
            #         frame[y+i*step:y+(i+1)*step,
            #         x+j*step:x+(j+1)*step] = face[i, j]
        cv2.imshow('wangcai',frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    cap.release()