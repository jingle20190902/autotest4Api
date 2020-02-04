# -*- coding:UTF-8 -*-

"""
@project： 自动化测试
@author：Sun
@file:request.py
@time:2020-02-2020/2/3 13:56:51

"""
'''
封装HTTP请求
1.http_request 是主方法，直接供外部调用
2.__http_get、__http_post是实际底层分类调用的方法

'''

import requests,os,logging

