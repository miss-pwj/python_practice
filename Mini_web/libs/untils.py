#密码加密
"""

uuid
md5不是太流行  加密方式处理哈希值太短了  容易产生哈希碰撞  对md5进行攻击  彩虹表
shasum 多一些  一种算法
同一个包  hashilib   sha256算法   产生一个16进制转换的一个字符串
加盐  随即盐  利用随机数进行随机盐加入
密码转成bytes类型 通过16进制计算密码的哈希值
"""
from hashlib import sha256
import random
def gen_password(user_password):
    bin_password = user_password.encode('utf8')
    hashi_value = sha256(bin_password).hexdigest()
    salt = '%x' % random.randint(0x10000000,0xffffffff)
    safe_password = salt+hashi_value
    return safe_password


def check_password(user_passwrod,safe_password):
    bin_password = user_passwrod.encode('utf8')
    hashi_value = sha256(bin_password).hexdigest()
    return hashi_value == safe_password[8:]

# 'b2cccfad15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225'
