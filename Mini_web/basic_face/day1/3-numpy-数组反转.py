import numpy as np
nd = np.arange(10)
print(nd)
print(nd[0:5])#切片
print(nd[::2]) #有间隔切片
print(nd[::3])
print('-------------',nd[::-2]) #:: 代表着，有间隔；-2 倒着操作
# 这样，数组，就进行了反转
print('+++++++++++++',nd[::-1]) #:: 代表着，有间隔：-1（挨个取） 倒着操作
