#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from os import path, remove
from traceback import format_exc


"""
数据库操作
"""
class Database:

    _conn = None

    def __init__(self, db_location):
        # 如果存在该文件则删除
        if path.exists(db_location):
            remove(db_location)
        # 如果文件不存在, 自动创建
        self._conn = sqlite3.connect(db_location)


    '''
    执行sql
    '''
    def exec(self, sql):
        cursor = self._conn.cursor()
        try:
            # print(sql)
            # 执行sql语句
            cursor.execute(sql)

            # 通过rowcount获得插入的行数:
            # print('行数: ', cursor.rowcount)
        except Exception as e:
            print('-------exec Error Start-------')
            print(e.args)
            print(format_exc())
            print('-------exec Error End-------')
        finally:
            cursor.close()
            # 提交到数据库执行
            self._conn.commit()

    '''
        执行sql
        '''

    def exec_script(self, sql):
        cursor = self._conn.cursor()
        try:
            # print(sql)
            cursor.executescript(sql)
        except Exception as e:
            print('-------exec_script Error Start-------')
            print(e.args)
            print(format_exc())
            print('-------exec_script Error End-------')
        finally:
            cursor.close()
            # 提交到数据库执行
            self._conn.commit()


    '''
    执行sql并返回rowid
    '''
    def exec_return_rowid(self, sql):
        cursor = self._conn.cursor()
        try:
            # print(sql)
            # 执行sql语句
            cursor.execute(sql)
            # 返回最后插入的主键
            return cursor.lastrowid
        except Exception as e:
            print('-------exec_return_rowid Error Start-------')
            print(e.args)
            print(format_exc())
            print('-------exec_return_rowid Error End-------')
        finally:
            cursor.close()
            self._conn.commit()

    '''
    查询表信息
    '''
    def table_info(self, table_name):
        sql = ' PRAGMA table_info(%s) '\
              % (table_name)
        cursor = self._conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        print('表信息:', records)

        # 声明数据库表字段
        fields = []

        # 提取表字段
        for record in records:
            field = record[1]
            fields.append(field)
            # print('列名称: %s' %(field))

        cursor.close()
        return fields

    '''
    关闭数据库连接
    '''
    def close_connection(self):
        self._conn.close()


