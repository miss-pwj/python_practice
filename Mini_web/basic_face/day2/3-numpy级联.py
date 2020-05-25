import numpy as np

# a = np.array([1,2,3,4,5])
#
# b = np.array([-1,-2,-3,-4,-5])
#
# print(a)
# print(b)
#
# print(np.c_[a,b])

a = np.random.randint(0,100,size = 20)
b = np.random.randint(-50,50,size = (5,4))
# print(a.shape)
# c = np.c_[a.reshape(5,4,1),b.reshape(5,4,1)]
# print(c.shape)
print(a)
print(a.reshape(10,2))#形状改变
print(a.reshape(5,4,1,1,1)) #形状改变后，数据都没变