# -*- coding:UTF-8 -*-

"""
@project： 自动化测试
@author：Sun
@file:request.py
@time:2020-02-2020/2/5 20:48:17

"""

'''
封装HTTP请求
1.http_request 是主方法，直接供外部调用
2.__http_get、__http_post是实际底层分类调用的方法

'''
import requests,os,logging
from common import opmysql
from public import config
class RequestInterface(object):  #定义处理不同类型的求参数，包含字典、字符串、空值
    def __new_param(self,param):
        try:
            if isinstance(param,str) and param.startwith('{'):
                new_param = eval(param)
            elif param==None:
                new_param=''
            else:
                new_param=param
        except Exception as error:
            new_param=''
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return new_param  #     post请求，参数在body中
    def __http_post(self,interface_url,headerdata,interface_param):
        '''

        :param interface_url: 接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :return: 字典形式结果
        '''
    try:
        if interface_url!='':
            temp_interface_param = self.__new_param(interface_param)
            response = requests.post(url=interface_url,headers=headerdata,data=temp_interface_param,verify=False,timeout=10)
            if response.status_code==200:
                durtime =(response.elapsed.microseconds)/1000                 # 发起请求和响应到达时间，单位ms
                result ={'data':'0000','message':'成功','data':response.text}
            else:
                result ={'data':'2004','message':'接口返回状态错误','data':[]}
        elif interface_url =='':
            result = {'data':'2002','message':'接口地址参数为空','data':[]}
        else:
            result={'data':'2003','message':'接口地址错误','data':[]}
    except Exception as error:
        result ={'data':'9999','message':'系统异常','data':[]}
        logging.basicConfig(filename= config.src_path + '/log/syserror.log',level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        logger =logging.getLogger(__name__)
        logger.exception(error)
    return result
# GET请求，参数在接口地址候面
    def __http_get(self,interface_url,headerdata,interface_param):
        '''

        :param interface_url: 请求 接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :return: 字典形式结果
        '''
        try:
            if interface_url !='':
                temp_interface_param = self.__new_param(interface_param)
                requrl = interface_url+temp_interface_param
                response = requests.get(url=requrl,headers=headerdata,verify=False,timeout=10)
                # print response
                if response.status_code==200:
                    durtime = (response.elapsed.microseconds)/1000
                    # 发起请求和相应到达的时间，单位为ms
                    result = {'code':'0000','message':'成功','data':response.text}
                else:
                    result ={'code':'3004','message':'接口返回状态错误','data':[]}
                elif interface_url =='':
                    result ={'code':'3002','message':'接口地址参数为空','data':[]}
            else:
                result={'code':'3003','message':'接口地址错误','data':[]}
        except Exception as error:
            result ={'code':'9999','message':'系统异常','data':[]}
            logging.basicConfig(filename=config.src_path + '/log/syserror.log',level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(loneno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(error)
        return result
#         统一处理http请求
    def http_request(self,interface_url,headerdata,interface_param,request_type):
        '''

        :param interface_url: 接口地址
        :param headerdata: 请求头文件
        :param interface_param: 接口请求参数
        :param request_type: 请求类型
        :return: 字典形式结果
        '''
        try:
            if request_type =='get' or request_type=='GET':
                result=self.__http_get(interface_url,headerdata,interface_param)
            elif request_type=='post' or request_type=='POST':
                result=self.__http_post(interface_url,headerdata,interface_param)
        else:
            result ={'code':'1000','message':'请求类型错误','data':request_type}
        except Exception as error:
        result={'code':'9999','message':'系统异常','data':[]}
        logging.basicConfig(filename=config.src_path + '/log/syserror.log',level=logging.DEBUG,format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)')
        logger = logging.getLogger(__name__)
        logger.exception(error)
    return result
if __name__ = "__main__":
    test_interface=RequestInterface()  #实例化http请求类
test_db = opmysql.OperationDbInterface(host_db='192.168.1.110',user_db='root',passwd_db='root',name_db='test_interface',port_db=3306,link_type=0)  #实例化mysql处理类
    sen_sql ="select exe_mode,url_interface,header_interface,params_interface from case_interface where name_interface='getIpInfo' and id=1"
    params_interface=test_db.select_one(sen_sql)
    if params_interface['code']=='0000':
        url_interface=params_interface['data']['url_interface']
        temp=params_interface['data']['header_interface']
        print(temp)

headerdata=eval(params_interface['data']['header_interface'])  #unicode 转换成字典
    params_interface=params_interface['data']['params_interface']
    type_interface=params_interface['data']['exe_mode']
    if url_interface!='' and headerdata!='' and params_interface!='' and type_interface!='':
        result=test_interface.http_request(interface_url=url_interface,headerdata=headerdata,interface_param=params_interface,request_type=type_interface)
        if result['code']=='0000':
            request_resp=result['data']
            print("处理http请求成功,返回数据是：%s" %request_resp)
        else:
            print("处理http请求失败")
    else:
        print("测试用例数据中有空值")
else:
    print("获取接口测试用例数据失败")