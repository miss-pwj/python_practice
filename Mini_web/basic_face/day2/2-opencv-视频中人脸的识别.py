import cv2
import numpy as np

def main():
    # 给VideoCapture路径，打开视频
    # 加载视频，视频比较大的，代码执行结束，释放资源
    v = cv2.VideoCapture('./die.mp4')
    w = int(v.get(propId=cv2.CAP_PROP_FRAME_WIDTH))#视频宽度
    h = int(v.get(propId=cv2.CAP_PROP_FRAME_HEIGHT)) #视频高度
    print(w,h)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # 必须要通过VideoWriter_fourcc来操作
    writer = cv2.VideoWriter(filename = './die3.mp4',
                    fourcc = fourcc,
                    fps = 24, # frame per second 每秒多少帧
                    frameSize = (640,360),isColor = True) # 尺寸必须合适
    face_detector = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
    while True:
        flag, img = v.read()  # 读取了第一张图片
        if flag == False:
            break
        img = cv2.resize(img,dsize = (640,360))#尺寸缩放
        gray = cv2.cvtColor(img,code = cv2.COLOR_BGR2GRAY)
        face_zones = face_detector.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=10)
        for x,y,w,h in face_zones:#二维列表进行了遍历
            cv2.circle(img,center=(x + w//2,y + h//2),
                       radius=w//2,
                       color = [0,0,255],
                       thickness=2)
        # 存之前将img变成黑白，搞定了，黑白图片是二维的
        img_gray = cv2.cvtColor(img,code=cv2.COLOR_BGR2GRAY)
        img_gray = np.c_[img_gray.reshape(360,640,1),
                         img_gray.reshape(360,640,1),
                         img_gray.reshape(360,640,1)]
        writer.write(img_gray) #一帧一帧的写入视频文件中
        cv2.imshow('die', img)  # 一直读取图片，到了最后，还有吗？
        # waitkey等待键盘输入，电脑会将q转换成assic码
        # 视频播放 一秒24帧 1000/24
        key = cv2.waitKey(1)  # 等待10毫秒，显示下一张图片了
        #     如果键盘上的输入是q退出
        if key == ord('q'):
            break #死循环就会打断
    cv2.destroyAllWindows()
    v.release()
    writer.release()#释放资源
if __name__ == '__main__':
    main()