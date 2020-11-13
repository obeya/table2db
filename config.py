#!/usr/bin/python3
# -*- coding: utf-8 -*-

from os import getenv

# 当前用户 AppData
appdata = getenv("APPDATA")

# 排除的sheet
exclude_sheets = ['Sheet1', 'Sheet2']


# 数据库导出位置
# databaseExportLocation = appdata + r'\Autodesk\ApplicationPlugins\DICAD.bundle\Contents'
databaseExportLocation = '/home/lifeng/workspace'