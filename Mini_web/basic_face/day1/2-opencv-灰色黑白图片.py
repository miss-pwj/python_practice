import cv2
import numpy as np

img = cv2.imread('liyong.jpg')

# 一维的数组
# nd = np.array([1,2,3,4,5,6,7,8,9,10])
# # print(nd)
# # print(nd[:]) # 默认切片所有，从头到尾
# # print(nd[0:3]) #根据索引，进行切片，左闭右开
# # print(nd[3:6]) #正着数 0,1,2,3……
# # print(nd[3:-2]) # -2意味着倒着数-1，-2，-3……

# 二维的数组,axis = 0,axis = 1;倒着数 axis = -1，axis=-2
# nd2 = np.array([[1,3,5,7,9],[2,4,6,8,10],[-1,-3,-5,-7,-9],[-2,-4,-6,-8,-10]])
# print(nd2)
# print(nd2[:2]) # 首先切割时，对行，进行了切片
# print(nd2[:,:2]) # 行没有变换，列，进行前两列切片
# print(nd2[:2,2:]) # 既进行行切片，又进行列切片
# print(nd2[-2:,-3:]) # 切片规则一样，带上负号，意味着，倒着数
# print('----------------',nd2.max(),nd2.min())
# print('++++++++++++++++',nd2.max(axis = 0))
# print('****************',nd2.max(axis = -1)) # -1倒着数，axis = 1

print(img.shape)# numpy数组提供的方法，用于查看形状
# 1、使用切片和索引（只要知道位置，可以取出来）
# :,:代表着切片，冒号的前面和后面都没有数字，默认（所有）
# :代表着行，不变；第二个：代表着列不变，第三个，直接取出来（给索引）
# img2 = img[:,:,2] #获取第三维（蓝0绿1红2）的第一个数值

# 2、进行了numpy计算：max、min
# 362 axis = 0；630 axis = 1；3 axis = 2
# axis = 2,计算最大值时，求解的是最后一维，颜色的最大值
#axis轴（X轴，Y轴，Z轴……），方向，维度
img2 = img.max(axis = 2) # 求最大值，图片风格，偏亮
img3 = img.min(axis = 2) # 最小值，图片风格，偏黑

# 3、opencv自身提供的方法 two ----> to 从哪里到哪里
img4 = cv2.cvtColor(img,code = cv2.COLOR_BGR2GRAY) # cvt convert转化 gray 灰色，黑白

img5 = cv2.cvtColor(img,code = cv2.COLOR_BGR2HSV)
print(img4)
cv2.imshow('yong',img4)
cv2.waitKey(0)
cv2.destroyAllWindows()