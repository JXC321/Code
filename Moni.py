#应用训练出来的模型，进行数据的采集
import requests,time,getpass,sys,os,shutil
from PIL import Image
from nn_predict import *

url = 'http://jwc.scnu.edu.cn/' #登录界面
actionurl = 'http://jwc.scnu.edu.cn/default2.aspx' #提交页面
codeur = 'http://jwc.scnu.edu.cn/CheckCode.aspx' #验证码获取页面
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"} #伪装浏览器的头
vs = "dDwtNTE2MjI4MTQ7Oz5O1VSr99LahyNHrIGlotpJ441TCA=="

def Caiji(user,pwd,k):
    s = requests.Session()
    r = s.get(url)
    r = s.get(codeur)
    
    name = str(k+1001)+'code.jpg'

    with open(name,'wb') as f:
        f.write(r.content)
    
    print('识别出来的验证码图片为:')
    tsc = predict(name)

    data = {
            'txtUserName':user,
            'TextBox2':pwd,
            'txtSecretCode':tsc,
            '__VIEWSTATE':vs,
            'Button1':''
            }

    r = s.post(url,data = data,headers = headers)
    s.close() 
    #print(r.text)
    #print(len(r.text))
    return len(r.text),tsc,name

if __name__ == '__main__':
    K = int(sys.argv[1])
    user = input('请输入用户名:')
    pwd = getpass.getpass('请输入密码:')
    RN = 0 #记录正确分类的数据数目
    EN = 0 #记录错误分类的数据数目

    Mainpath = os.getcwd() #获得当前的主路径
    Dir1 = Mainpath + '/采集数据' #收集正确分类的数据
    Dir2 = Mainpath + '/错误分类' #收集错误分类的数据
    
    Ex1 = os.path.exists(Dir1)
    Ex2 = os.path.exists(Dir2)
    if not Ex1:
        os.mkdir(Dir1)
    if not Ex2:
        os.mkdir(Dir2)

    while(K!=RN+EN):
        os.chdir(Mainpath)
        Len,code,name = Caiji(user,pwd,RN+EN)
        
        if Len > 8000:
            RN += 1
            print('正确分类!'+'\n')
            os.rename(name,str(1000+RN)+'code.jpg')
            shutil.move(str(1000+RN)+'code.jpg',Dir1)
            with open('采集数据.txt','a') as f:
                f.write(code+'\n')
        else:
            EN += 1
            print('错误分类！'+'\n')
            os.rename(name,str(1000+EN)+'code.jpg')
            shutil.move(str(1000+EN)+'code.jpg',Dir2)
            with open('错误分类.txt','a') as f:
                f.write(code+'\n')

        time.sleep(2)
    err = EN/(K)
    print('err = '+str(err))
