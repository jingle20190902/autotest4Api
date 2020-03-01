# -*- coding:UTF-8 -*-

"""
@project： 自动化测试
@author：Sun
@file:compare.py
@time:2020-02-2020/2/7 11:26:11

"""
'''
定义对HTTP返回包数据过程
1、compare_param是对外的参数比较类
2、compare_code是关键参数值比较方法，compare_params_complete是参数完整性比较方法
3、get_compare_params是获得返回包数据去重后集合方法
4、recur_params递归操作方法，辅助去重使用
'''
import importlib

importlib.reload(sys)
import json, pymysql, os, logging
from public import config

operation_db = pymysql.OperationDbInterface()  # 实例化测试库操作类


class CompareParam(object):
    # 初始化数据
    def __init__(self, params_interface):
        self.params_interface = params_interface  # 接口入参
        self.id_case = params_interface['id']  # 测试用例用id
        self.result_list_response = []  # 定义用来存储参数集的空列表
        self.params_to_compare = params_interface['params_to_compare']  # 定义参数完整性预期结果

    #       定义关进参数值（code）比较
    def compare_code(self, result_interface):
        '''

        :param result_interface: Http返回包数据
        :return: 返回码code，返回信息message，数据data
        '''
        try:
            if result_interface.startwith('{') and isinstance(result_interface, str):
                temp_result_interface = json.loads(result_interface)  # 将字符类型转换为字典类型
                temp_code_to_compare = self.params_interface['code_to_compare']  # 获取待比较code名称
                if temp_code_to_compare in temp_result_interface.keys():
                    # if unicode(str(temp_result_interface[temp_code_to_compare]),"utf-8")==unicode(str(self.params_interface['code_expect']),"utf-8"):
                    if temp_result_interface[temp_code_to_compare] == self.params_interface['code_expect']:
                        result = {'code': '0000', 'message': '关键字参数值相同', 'data': []}
                        operation_db.op_sql(
                            "update case_interface set code_actual ='%s',result_code_compare=%s where id=%s" % (
                            temp_result_interface[temp_code_to_compare], 1, self.id_case))
                        # operation_db.Op_sql("update case_interface set code_actual=%s,result_code_compare=%s,result_interface='%s' where id=%s" %(temp_result_interface[temp_code_to_compare],0,result_interface,self.id_case))
                    elif unicode(str(temp_result_interface[temp_code_to_compare]), "utf-8") != unicode(
                            str(self.params_interface['code_expect']), "utf-8"):
                        result = {'code': '1003', 'message': '关键字参数值不同', 'data': []}
                        operation_db.op_sql(
                            "update case_interface set code_actual='%s',result_code_compare=%s where id=%s" % (
                            temp_result_interface[temp_code_to_compare], 3, self.id_case))
                    else:
                        result = {'code': '1002', 'message': '关键字参数值比较出错', 'data': []}
                        operation_db.op_sql(
                            "update case_interface set code_actual='%s',result_code_compare=%s where id=%s" % (
                            temp_result_interface[temp_code_to_compare], 3, self.id_case))
                    else:
                    result = {'code': '1001', 'message': '返回包数据无关键字参数', 'data': []}
                    operation_db.op_sql("update case_interface set code_actual='%s' where id=%s" % (2, self.id_case))
                else:
                    result = {'code': '1000', 'message': '返回包格式不合法', 'data': []}
                    operation_db.op_sql(
                        "update case_interface set reslut_code_compare=%s where id=%s" % (4, self.id_case))

    except Exception as error:  # 记录日志到log.txt文件
    result = {'code': '9999', 'message': '关键字参数值比较异常', 'data': []}
    operation_db.op_sql("update case_interface set result_code_compare=%s where id =%s" % (9, self.id_case))
    logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    logger = logging.getLogger(__name__)
    logger.exception(error)
    return result
#定义将接口返回数据中参数名写入列表中
def get_compare_params(self,result_interface):
    '''

    :param result_interface:HTTP 返回包数据
    :return:返回码code,返回信息message,数据data
    '''
    try:
        if result_interface.startwith('{') and isinstance(result_interface,str):
            temp_result_interface=json.loads(result_interface)
            self.result_list_response=temp_result_interface.keys()
            result={'code':'0000','message':'成功','data':self.result_list_response}
        else:
            result={'code':'1000','message':'返回包格式不合法','data':[]}
    except Expection as error:    #记录日志到log.txt文件
        result ={'code':'9999','message':'处理数据异常','data':[]}
        logging.basicConfig(filename=config.src_path + 'log/syserror.txt',level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        logger=logging.getLogger(__name__)
        logger.exception(error)
    return result
# 参数完整性比较方法，传参值与__recur_params方法返回结果比较


