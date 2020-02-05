# -*- coding:UTF-8 -*-

"""
@project： 自动化测试
@author：Sun
@file:opmysql.py
@time:2020-02-2020/2/3 14:19:29

"""
'''
定义对MySQL数据库基本操作的封装
1.包括基本的单条语句操作，删除，修改，更新
2.独立的查询单条，多条数据
3.独立的添加多条数据
'''

import logging, os, pymysql
from public import config


class OperationDbInterface(object):
    def __init__(self, host_db='192.168.0.106', user_db='root', passwd_db='root', name_db='test_interface',
                 port_db=3306, link_tpye=0):
        '''

        :param host_db: 数据库服务主机
        :param user_db:数据库用户名
        :param passwd_db:数据库密码
        :param name_db:数据库名称
        :param port_db:端口号，整型数字
        :param link_tpye:连接类型，用于输出的数据是元组还是字典，默认是字典，link_type = 0
        :return 游标
        '''
        try:
            self.conn = pymysql.connect(host=host_db, user=user_db, passwd=passwd_db, db=name_db, port=port_db,
                                        charset='utf8')
            # 创建数据连接
            if link_tpye == 0:
                self.cur = self.conn.cursor(cursorclass=pymysql.cursors.DictCursor)
                # 返回字典
            else:
                self.cur = self.conn.cursor()
                # 返回元组
        except pymysql.Error as e:
            print("创建数据库连接失败| Mysql Error %d: %s" % (e.args[0], e.args[1])
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
            logger = logging.getLogger(__name__)
            logger.exception(e)
            # 定义单条数据操作，增加、删除、修改

        def op_sql(self, condition):
            '''

            :param condition: sql 语句，该通用方法可以用来代替insertone,updateone,deleteon
            :return: 字典形式
            '''
            try:
                self.cur.execute(condition)
                # 执行sql语句
                self.conn.commit()
                # 提交游标数据
                result = {'code': '0000', 'message': '执行通用操作成功', 'data': []}
            except pymysql.Error as e:
                self.conn.rollback()
                # 执行回滚操作
                result = {'code': '9999', 'message': '执行通用操作异常', 'data': []}
                print("数据库错误|op_sql %d: %s" % (e.args[0], e.args[1]))
                logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                    format='%(asctime)s% (filename)s[line:%(lineno)d] %(levelname)s %(message)s')
                logger = logging.getLogger(__name__)
                logger.exception(e)
            return result

        # 查询表中单条数据
        def select_one(self, condition):
            '''

            :param condition: sql语句
            :return: 字典形式的单条查询结果
            '''
            try:
                rows_affect = self.cur.execute(conditon)
            if rows_affect > 0:
                results = self.cur.fetchone()
                result = {'code': '0000', 'message': u'执行单条查询操作成功', 'data': []}

            else:
                result = {'code': '0000', 'message': u'执行单条查询操作成功', 'data': results}
            except pymysql.Error as e:
            self.conn.rollback()
            result = {'code': '9999', 'message': u'执行单条查询操作异常', 'data': []}
            print("数据库错误|select_one %d: %s" % (e.args[0], e.args[1]))
            logging.basicConfig(filename=config.src_path + '/log/syserror.log', level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'')
                               logger = logging.getLogger(__name__)
            logger.exception(e)
            return result
#         查询表中多条数据
        def select_all(self,condition):
            '''

            :param condition: sql语句
            :return: 字典形式的批量查询结果
            '''
            try:
                rows_affect = self.cur.execute(condition)
                if rows_affect > 0:
                    self.cur.scroll(0,mode='absolute')
                    results = self.cur.fetchall()
                    result = {'code':'0000','message':'执行批量查询操作成功','data':results}
                else:
                    result = {'code':'0000','message':'执行批量查询操作成功','data':[]}
            except pymysql.Error as e:
                self.conn.rollback()
                result ={'code':'9999','message':'执行批量查询操作异常','data':[]}
                print("数据库错误|select_all %d: %s" % (e.args[0],e.args[1]))
                logging.basicConfig(filename= config.src_path + '/log/syserror.log',level=logging.DEBUG,format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
                logger = logging.getLogger(__name__)
                logger.exception(e)
                return result
#       定义表中插入多条数据
        def insert_more(self,condition,params):
            '''

            :param condition: insert 语句
            :param params:insert 数据，列表形式[('3','Tom','1 year 1 class','6'),('3','Jack','2 year 1 class','7'),]
            :return:字典形式的批量插入数据结果
            '''
            try:
                results=self.cur.executemany(condition,params)
                # 返回插入的数据条数
                self.conn.commit()
                result={'code':'0000','message':'执行批量查询操作成功','data':int(results)}
            except pymysql.Error as e:
                self.conn.rollback()
#           执行回滚操作
                result ={'code':'9999','message':'执行批量查询异常','data':[]}
                print("数据库错误|insert_more %d:%s" %(e.args[0],e.args[1]))
                logging.basicConfig(filename= config.src_path + '/log/syserror.log',level=logging.DEBUG,format='%(asctime)s %(filename)s[line:% (lineno)d] %(levelname)s %(message)s')
                logger = logging.getLogger(__name__)
                logger.exception(e)
                return result
#            数据库关闭
            def __del__(self):
                if self.cur !=None:
                    self.cur.close()
                if self.conn !=None:
                    self.conn.close()
    if __name__ == "__main__":
        test = OperationDbInterface()
#         实例化类
    result = test.select_all("select * from config where id =1")
#     result = test.insert_more("insert into config_total(key_config,value_config,status) values(%s,%s,%s)",[(1,1,1),(2,2,2)]
    if result['code']=='0000':
        print(result['data'])
    else:
        print(resut['message'])



