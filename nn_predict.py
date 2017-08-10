# 识别验证码
#-----------------------------
# 执行要求：
#   1. 当前目录下需要有clf.model,即用神经网络训练好的模型
#   2. 当前目录有验证码图片
#-----------------------------
# 输出：
#   打印识别出来的验证码
#-----------------------------
import os
import numpy as np
from sklearn.externals import joblib
from Data import *
def predict(fn):
    # 处理图片
    tx = Main(fn)
    code = ''
    #print(os.getcwd())
    # load 训练好的神经网络模型
    #Mainpath = os.getcwd()
    nn_model = 'clf.model'
    clf = joblib.load(nn_model)
    # 识别

    yp = clf.predict(tx)
    # 转成字符
    for i in range(4):
        if yp[i] in range(0,10):
            code += chr(int(yp[i])+48)
        else:
            code += chr(int(yp[i])+87)
    print(code)
    return code


if __name__ == '__main__':
    
    # 验证码图片路径
    import sys
    fn = sys.argv[1]
    predict(fn)
