from PIL import Image
import numpy as np
import sys
import os


#将图片转换成矩阵。imf是图片的名字，返回data是一个数字矩阵
def img2array(imf):
    im = Image.open(imf)
    row,col = im.size
    data = np.zeros((row,col))
    for i in range(row):
        for j in range(col):
            data[i,j] = im.getpixel((i,j))
    return data

#将代表图片的数字矩阵二值化，去噪。
def bnyprc(data,threhold):
    row,col = data.shape
    for i in range(row):
        for j in range(col):
            if data[i,j] < threhold:
                data[i,j] = 1
            else:
                data[i,j] = 0
    return data

#辅助函数，打印出像素矩阵
def show(a):
    row,col = a.shape
    for i in range(row):
        for j in range(col):
            print('%4d'%(a[i,j]),end='')
        print('')
   
#裁剪     
def cut(a):
    #去掉验证码首尾空白的地方。取一个阈值，然后将矩阵图片垂直投影，像素值小于阈值的判定为空白，否则为字符。
    prj = np.sum(a,1)
    beg = 0
    end = 0
    for i in range(len(prj)):
        if prj[i] > 3:
            beg = i
            #print(prj[i],' ',i)
            break
        
    for i in range(len(prj)-1,-1,-1):
        if prj[i] > 3:
            end = i
            break
    
    #均匀切割成四等分，分成两种情况：一.刚好可以四等分；二.不能四等分    
    l = end - beg + 1
    #print(beg,end)
    r = l%4
    #print('r={0}'.format(r))
    step = l//4
    #print('step={0}'.format(step))
    j = beg
    index = []
    if r == 0:
        for i in range(4):
            index.append((beg+step*i,beg+(i+1)*step))
    else:
        step += 1
        k = beg
        for i in range(4-r):
            index.append((k,k+step))
            k += (step-1)
        for i in range(r):
            index.append((k,k+step))
            k += step
    ret = [a[beg:end,:]]
    #print(index)
    for ind in index:
        ret.append(a[ind[0]:ind[1],:])
    return ret

#辅助函数，将数字矩阵转化为图片
def array2img(a):
    row,col = a.shape
    im = Image.new('P',a.shape)
    for i in range(row):
        for j in range(col):
            if a[i,j] == 1:
                im.putpixel((i,j),0)
            else:
                im.putpixel((i,j),255)
    return im

#将图片的维度统一
def Add(k):
    r,c = k.shape
    cha = 17-r
    if cha != 0:
        B = np.zeros((cha,c))
        k = np.concatenate((k,B))
    return k

#将验证码的四个字符分开并存储在矩阵中返回
def Main(f):
    a = img2array(f) #将图片转化成矩阵
    a = bnyprc(a,100) #将图片二值化

    k = cut(a) #切割图片，k有5个元素，后四个元素是切割好的图片的矩阵
    for i in range(1,5):
        k[i] = Add(k[i])
    #把一个验证码切割好后的每一个图片拉成一个向量，总共四个
    A = np.zeros((4,k[1].size))
    for i in range(1,5):
        A[i-1,:] = np.reshape(k[i],(1,k[i].size))
    return A
      

#程序功能：将验证码图片转化成数字矩阵，存储在Train_Image.txt文件中。
#'验证码数据集'是包含验证码图片的文件夹，运行代码时应将该文件夹与代码放在同一个目录
#输出:
#   Train_Image.txt文件存储图片矩阵，矩阵的每一行是一个单独的字符
#   输出数字矩阵的大小

if __name__ == '__main__':
    codepath = "验证码数据集/"
    for i in range(1,600+1):
        name = codepath + str(i)+'code.jpg'
        if i is 1:
            B = Main(name)
        else:
            A = Main(name)
            B = np.concatenate((B,A))

    np.savetxt('Train_Image.txt',B)
    AA = np.loadtxt('Train_Image.txt')
    print(AA.shape)
