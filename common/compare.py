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
import json,pymysql,os,logging
from public import config
operation_db=pymysql.OperationDbInterface() #实例化测试库操作类
class CompareParam(object):
    # 初始化数据
