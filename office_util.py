#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pandas import read_excel
from db_util import *

'''
excel read
'''


class ExcelRead:
    # DataFrame
    _dataframe = None

    def __init__(self, excel_path):
        self._dataframe = read_excel(excel_path, sheet_name=None)
        converter_columns = self.get_converter_column()
        self._dataframe = None
        self._dataframe = read_excel(excel_path, sheet_name=None, converters=converter_columns)
        self.sqlite = Database('')

    def get_converter_column(self):
        '''
        读取所有的列,设置转换类型:转换为字符串类型
        {u'OC_Rate': str}
        '''
        columns_dict = {}
        columns_set = set()
        sheet_names = list(self._dataframe.keys())
        for sheet_name in sheet_names:
            sheet_dataframe = self._dataframe.get(sheet_name)
            column_names = list(sheet_dataframe.columns)
            for column_name in column_names:
                columns_set.add(column_name)

        for col in columns_set:
            columns_dict[col] = str
        return columns_dict

    '''
    获取所有的sheet表名称
    '''

    def get_sheet_names(self):
        sheet_names = self._dataframe.keys()
        return list(sheet_names)

    '''
    sheet表的列名
    '''

    def get_columns(self, sheet_name):
        sheet_dataframe = self._dataframe.get(sheet_name)
        # 提取表头, 转为数组
        column_names = list(sheet_dataframe.columns)
        return column_names

    '''
    根据sheet名称获取dataframe
    '''

    def get_data_by_sheet_name(self, sheet_name):
        sheet_dataframe = self._dataframe.get(sheet_name)
        return sheet_dataframe
