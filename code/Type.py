import numpy as np

#将标签集的标签转换为OneOfK编码方式
def Type(filename):
    f = open(filename,'r')
    A = f.read()
    f.close()
    
    A = A.split('\n')
    K = ''
    for i in range(len(A)):
        K = K + A[i]
    #print(K,'\n',len(K))
    
    C = np.zeros((len(K),36))
    
    for i in range(len(K)):
        if ord(K[i]) in range(48,58):
            C[i][ord(K[i])-48] = 1
        else:
            try:
                C[i][ord(K[i])-97+10] = 1
            except IndexError as  e:
                print (str(i//4))
    
    np.savetxt('Type.txt',C)
    #KK = np.loadtxt('Type.txt')

#函数功能：将标签集的数据进行OneOfK编码
#'验证码标签集.txt'是验证码的字符标签
#输出：Type.txt是一个标签集的数字矩阵。每一行是一个标签，只有一个元素是1其余元素为0
if __name__ == '__main__':    
    Type('验证码标签集.txt')
