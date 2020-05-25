import numpy as np
from sklearn.model_selection import train_test_split

# Ctrl + alt + L:格式化
a = np.arange(30)  # 生成随机数

# b = [chr(i) for i in range(65,65+30)]
b = np.arange(-30, 0)
print(a)
print(b)
# 可以同时，拆分多个数组，拆分a和b的规则一样的！
# 拆分，一一对应的！
a_train, a_test, b_train, b_test = train_test_split(a, b, test_size=1 / 3)  # 训练数据保留10，那么训练数据自然就是20个
print('---------', a_train)
print('+++++++++', a_test)
print('--------', b_train)
print('++++++++', b_test)
