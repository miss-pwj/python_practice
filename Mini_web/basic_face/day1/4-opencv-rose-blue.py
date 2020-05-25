import numpy as np
import cv2

rose = cv2.imread('rose.jpg')

# 先高度，再宽度，像素
# rose = rose[-213:] # 高度方向，进行裁剪
# rose = rose[:,250:] # 宽度方向裁剪
# rose = rose[::-1] # 倒转

# 像素，操作一下
rose = rose[:,:,::-1] # 颜色倒转，蓝绿红 --->红绿蓝

print(rose.shape)

cv2.imshow("rose",rose)
cv2.waitKey(0)
cv2.destroyAllWindows()
