# 前面安装库，使用opencv-python
# 使用方式通过导包（这些都是别人写好的代码）
# import cv2
# opencv-python 库里面的Python接口的方法，都是在cv2中
# 所以导包时，导入cv2，就可以了
import cv2 # 亮色，导包，同时使用了，闪闪发光
import matplotlib.pyplot as plt # 灰色，没有使用，黯淡无光
# 聪明才智（脑壳中），无论你是否使用，都在。如果使用，开发，闪闪发光；不用，黯淡无光
# 无论什么样存在，必须使用，这个存在，才属于你！！！
img = cv2.imread('flower1.jpg') # jpg类型的图片，数值范围是0~255
print(type(img))
print(img.max())
print(img.min())
# print(img)
# img2 = plt.imread('./flower.png') # png类型数值范围：0~1.0
# print(img2)
# 显示图片
cv2.imshow('flower',img) #弹出一个窗口，一直显示，说明程序没有停下来
cv2.waitKey(delay=0)# 5000毫秒 ，0意味着无限等待，等待键盘的输入
cv2.destroyAllWindows()#销毁窗口，不显示，程序结束退出