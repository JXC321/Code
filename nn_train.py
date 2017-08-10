# 神经网络算法实现验证码识别
#-----------------------------
#数据：
#   code/w.txt: 验证码图片数据
#   code/Type.txt: 验证码对应的标签
#-----------------------------
#输出：
#   识别错误率
#   clf.model: 神经网络算法模型，提供给nn_predict.py使用
#------------------------------

import numpy as np

# 将oneOfk变成0，1，2...
def getLabel(Y):
    r,c = Y.shape
    y = np.ravel(np.zeros((1,r)))
    for i in range(r):
        m = 0
        for j in range(c):
            if Y[i,j] == 1:
                m = j
                break
        y[i] = m
    return y
# 测试 非oneOfk形式
def test1(y,yp):
    err = 0
    l = len(y)
    for i in range(l):
        if y[i] != yp[i]:
            err += 1
    return err/l

if __name__ == '__main__':
    # load data
    X = np.loadtxt('code/Train_Image.txt')
    y = np.loadtxt('code/Type.txt')
    r,c = X.shape
    trn = 3500 #训练集数目
    
    #处理标签为非oneOfk形式
    k = getLabel(y)

    #检验合理性
    from sklearn.neural_network import MLPClassifier
    clf = MLPClassifier(alpha=1e-5, hidden_layer_sizes=(200,100,50), random_state=2)
    clf.fit(X[0:trn,:],k[0:trn])
    yp = clf.predict(X[trn:,:])
    print('训练数据为%d个,测试数据为%d个，错误率为%.2f%%'%(trn,r-trn,test1(k[trn:],yp)*100))

    #保存神经网络模型
    from sklearn.externals import joblib
    clf1 = MLPClassifier(alpha=1e-5, hidden_layer_sizes=(200,100,50), random_state=2)
    clf1.fit(X,k)
    joblib.dump(clf1,'clf.model')
    print('神经网络模型已经保存载clf.model文件了！')
