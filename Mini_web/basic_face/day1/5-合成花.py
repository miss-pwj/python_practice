import cv2
if __name__ == '__main__':
    rose = cv2.imread('rose2.jpg') #玫瑰花，尺寸偏大
    rose = cv2.resize(rose,dsize = (480,600)) #作用：调整图片的尺寸
    print(rose.shape)
    xi = cv2.imread('xi.jpg')
    print(xi.shape)
    mix = cv2.addWeighted(xi,alpha = 0.8,src2 = rose,beta = 0.2,gamma=0.1) #组合两张图片
    cv2.imshow('xianhua',mix)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
