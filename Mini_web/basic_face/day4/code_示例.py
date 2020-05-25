import numpy as np
from skimage import data
import cv2
import os

a = list('abcdeEFHIJ')
# print(a)
# for i in a:
#     print('-------------',i)
#
# # 枚举，会为列表a中的数据，进行编号，默认情况下从0开始编号，一次递增
# for i,data in enumerate(a):# 枚举
#     print('+++++++++++++',i,data)
#
# for i,data in enumerate(a,1024):# 枚举
#     print('*************',i,data)

# b = list('我爱北京天安门太阳升')
# print(a)
# print(b)
# for i,j in zip(a,b):
#     print('---------------------',i,j)

# moon = data.moon()
# moon2 = cv2.equalizeHist(moon)
# while True:
#     cv2.imshow('moon', moon)
#     key = cv2.waitKey(0)
#     if key == ord('q'):
#         break
#     cv2.imshow('moon', moon2)
#     cv2.waitKey(0)
# cv2.destroyWindow('moon')
# os.makedirs('./hello',exist_ok=True)
# num = len(os.listdir('./hello'))
# print(num)

for i in range(100):
    # %d 代表数字，占位符 digital 数字
    # print('Hello %d AI'%(i))
    if i%2 == 0:
        # %s代表着 str
        print('Hello %s AI'%('Python'))
    else:
        print('Hello %s AI'%('World'))