# -*- coding: utf-8 -*-

from functools import reduce

from PyQt5 import QtCore, QtGui, QtWidgets

from os import path, getenv, remove
from PyQt5.QtWidgets import (QWidget, QMessageBox, QFileDialog)
from PyQt5.Qt import (QThread, pyqtSignal)
from traceback import format_exc

from uuid import uuid4
import util
import config
from db_util import Database
from office_util import ExcelRead
from shutil import copy
import platform


class Ui_MainWindow(QWidget, object):
    # 版本号
    _version = ''

    def setupUi(self, mainWin):
        mainWin.setObjectName("mainWin")
        mainWin.resize(650, 400)
        mainWin.setMinimumSize(QtCore.QSize(650, 400))
        mainWin.setMaximumSize(QtCore.QSize(650, 400))
        font = QtGui.QFont()
        font.setFamily("黑体")
        mainWin.setFont(font)
        # mainWin.setAutoFillBackground(True)

        window_pale = QtGui.QPalette()
        window_pale.setBrush(self.backgroundRole(),QtGui.QBrush(QtGui.QPixmap("resource/bg.png")))
        mainWin.setPalette(window_pale)

        self.centralwidget = QtWidgets.QWidget(mainWin)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(140, 270, 431, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.tDbEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.tDbEdit.setEnabled(False)
        self.tDbEdit.setGeometry(QtCore.QRect(140, 80, 401, 20))
        self.tDbEdit.setObjectName("tDbEdit")
        self.btnChoseExcelFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnChoseExcelFile.setGeometry(QtCore.QRect(560, 160, 81, 23))
        self.btnChoseExcelFile.setObjectName("btnChoseExcelFile")
        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setGeometry(QtCore.QRect(550, 340, 81, 31))
        self.btnExit.setObjectName("btnExit")
        self.labDbFile = QtWidgets.QLabel(self.centralwidget)
        self.labDbFile.setGeometry(QtCore.QRect(30, 80, 101, 16))
        self.labDbFile.setObjectName("labDbFile")
        self.labExcelFile = QtWidgets.QLabel(self.centralwidget)
        self.labExcelFile.setGeometry(QtCore.QRect(30, 160, 101, 16))
        self.labExcelFile.setObjectName("labExcelFile")
        self.tExcelEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.tExcelEdit.setGeometry(QtCore.QRect(140, 160, 401, 71))
        self.tExcelEdit.setObjectName("tExcelEdit")
        self.btnClearFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnClearFile.setGeometry(QtCore.QRect(560, 190, 81, 23))
        self.btnClearFile.setObjectName("btnClearFile")
        self.btnChoseDbFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnChoseDbFile.setEnabled(False)
        self.btnChoseDbFile.setGeometry(QtCore.QRect(560, 80, 81, 23))
        self.btnChoseDbFile.setObjectName("btnChoseDbFile")
        self.btnExportDb = QtWidgets.QPushButton(self.centralwidget)
        self.btnExportDb.setGeometry(QtCore.QRect(450, 340, 81, 31))
        self.btnExportDb.setObjectName("btnExportDb")
        self.labProcess = QtWidgets.QLabel(self.centralwidget)
        self.labProcess.setGeometry(QtCore.QRect(30, 270, 101, 16))
        self.labProcess.setObjectName("labProcess")
        mainWin.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWin)
        self.btnExit.clicked.connect(mainWin.close)
        self.btnClearFile.clicked.connect(self.tExcelEdit.clear)

        self.customFun()

        QtCore.QMetaObject.connectSlotsByName(mainWin)

    def retranslateUi(self, mainWin):
        _translate = QtCore.QCoreApplication.translate
        mainWin.setWindowTitle(_translate("mainWin", "table2sqlite %s" % (self._version,)))
        self.btnChoseExcelFile.setText(_translate("mainWin", "选择"))
        self.btnExit.setText(_translate("mainWin", "关闭"))
        self.labDbFile.setText(_translate("mainWin", "选择导出的位置:"))
        self.labExcelFile.setText(_translate("mainWin", "选择excel表格文件:"))
        self.btnClearFile.setText(_translate("mainWin", "清空"))
        self.btnChoseDbFile.setText(_translate("mainWin", "选择"))
        self.btnExportDb.setText(_translate("mainWin", "转换"))
        self.labProcess.setText(_translate("mainWin", "当前进度:"))

    def customFun(self):
        self.btnChoseExcelFile.clicked.connect(self.openFileNameDialog)
        self.btnChoseDbFile.clicked.connect(self.choseDbExportDir)
        self.btnExportDb.clicked.connect(self.convertExcel2DB)
        self.getDbDefaultPath()

    # 设置进度条
    def set_progressbar_value(self, value):
        self.progressBar.setValue(value)
        if value == 100:
            QMessageBox.information(self, '提示', '数据库转换完成!')
            self.btnExportDb.setEnabled(True)
            return

    # 获取默认数据库保存位置
    def getDbDefaultPath(self):
        db_default_path = path.join(path.expanduser("~"), u'Desktop')
        # db_default_path = path.join(path.expanduser("~"), u'AppData\Roaming\Autodesk\ApplicationPlugins\DICAD.bundle')
        self.tDbEdit.setText(db_default_path)

    # 选择数据库导出目录
    def choseDbExportDir(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
        self.tDbEdit.setText(directory)

    # 文件对话框
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, filetype = QFileDialog.getOpenFileName(self, "选择Excel", "./",
                                                         "*.xlsx", options=options)
        self.tExcelEdit.setText(fileName)

    # 执行导出数据库
    def convertExcel2DB(self):
        dbPath = self.tDbEdit.text() + '/di.sqlite'  # 数据库保存位置
        # 如果存在该文件则删除
        if path.exists(dbPath):
            remove(dbPath)

        excelFile = self.tExcelEdit.toPlainText()  # excel位置

        # 验证是否选择了文件
        if not dbPath:
            self.warningMsg('database', '请选择导出文件夹')
            return
        if not excelFile:
            self.warningMsg('excel', '请选择Excel源文件')
            return

        try:
            target = '%s/%s%s' % (getenv('Temp'), ''.join(str(uuid4()).split('-')), path.splitext(excelFile)[1])
            print('target: ', target)
            delFlag: bool = False

            if 'Windows' == platform.system() :
                # 0. 拷贝excel为副本, 因为excel在打开状态下, 程序闪退
                copy(excelFile, target)
                delFlag = True
            else:
                target = excelFile

            # 开启线程转换数据库
            self.threadConvert = ThreadConvertDB(dbPath, target, delFlag)
            self.threadConvert.convert_proess_signal.connect(self.set_progressbar_value)
            self.threadConvert.start()
            self.btnExportDb.setEnabled(False)
        except IOError as e:
            print("Unable to copy file. %s" % e)
            QMessageBox.warning(self, "Warning", self.tr("请先关闭文件'%s', 再导入数据!" % (excelFile,)), QMessageBox.Cancel,
                                QMessageBox.Cancel)
            return
        except Exception as e:
            print('-------def convertExcel2DB Error Start-------')
            print(e.args)
            print(format_exc())
            print('-------def convertExcel2DB Error End-------')
        finally:
            pass

    # 警告对话框
    def warningMsg(self, type, msg):
        button = QMessageBox.warning(self, "Warning",
                                     self.tr(msg),
                                     QMessageBox.Open | QMessageBox.Cancel,
                                     QMessageBox.Open)

        if button == QMessageBox.Open:
            if 'database' == type:
                self.choseDbExportDir()
            elif 'excel' == type:
                self.openFileNameDialog()
        elif button == QMessageBox.Cancel:
            pass
        else:
            return


# 转换数据库线程
class ThreadConvertDB(QThread):
    convert_proess_signal = pyqtSignal(int)  # 创建信号

    def __init__(self, dbPath, excelPath, delFlag):
        super().__init__()
        self.dbPath = dbPath
        self.excelPath = excelPath
        self.delFlag = delFlag

    def run(self):

        sqlite = Database(self.dbPath)
        office = ExcelRead(self.excelPath)

        try:
            # 处理excel表的数据
            table_info = self.process_table(office)

            if table_info:
                # 建立数据库表
                self.create_sqlite(table_info, sqlite)
                record_maximum = self.calc_record_maximum(table_info)

                row_count = 0
                # 插入数据
                for key in table_info.keys():
                    print('key: ', key)
                    # 该表转换完成的行数
                    row_count = self.process_data( key, table_info, sqlite) + row_count
                    # 已经转换完成的行数占总行数的比例数值
                    proess = self.calc_percentage(row_count, record_maximum)
                    # 为信号传值
                    self.convert_proess_signal.emit(int(proess))
                sqlite.close_connection()
            self.exit(0)
        except Exception as e:
            print('-------ThreadConvertDB Error Start-------')
            print(e.args)
            print(format_exc())
            print('-------ThreadConvertDB Error End-------')
        finally:
            if self.delFlag:
                remove(self.excelPath)
    
    # 统计元素个数（进度条）
    def count_element(self, arr):
        result = {}
        for i in set(arr):
            result[i] = arr.count(i)
        return result

    # 如有重名,自动重命名
    def rename_table_name(self, sheet_names):
        table_names = []
        for i in range(len(sheet_names)):
            table_name = util.replace(sheet_names[i])
            table_names.append(table_name)
        # 统计表名
        counts = self.count_element(table_names)
        print("counts: ", counts)
        for tbl in table_names:
            count = counts[tbl]

    # 处理excel表信息
    def process_table(self, office):
        sheet_names = office.get_sheet_names()
        # 删除排除的sheet表
        for exclude_sheet_name in config.exclude_sheets:
            # 删除所有排除的sheet表
            while exclude_sheet_name in sheet_names:
                sheet_names.remove(exclude_sheet_name)
        print('sheet_names: ', sheet_names)

        # 保存表名和表中的列
        table_info = {}
        table_names = []

        # 遍历表获取表列明并处理
        for i in range(len(sheet_names)):

            table_name = util.replace(sheet_names[i])
            if table_name in table_names:
                table_name = '%s%d' % (table_name, i)
                print(table_name)
            table_names.append(table_name)

            # print('table_name: ', table_name)
            # 获取sheet表中的数据
            sheet_dataframe = office.get_data_by_sheet_name(sheet_names[i])
            # print('sheet_dataframe: ', sheet_dataframe)
            # 获取sheet表中的列名
            columns = list(sheet_dataframe.loc[:, ~sheet_dataframe.columns.str.contains("^Unnamed")])
            print('columns: ', table_name, columns)
            # 替换列非法字符
            for j in range(len(columns)):
                columns[j] = util.replace4columns(columns[j])

            table_data = (columns, sheet_dataframe)

            table_info[table_name] = table_data

        return table_info

    # 初始化数据库表
    def create_sqlite(self, table_info, sqlite):

        # 创建表格属性表
        sqlite.exec(self.create_talbe_attribute())

        # 根据sheet创建表
        for key in table_info.keys():
            field_sql = []
            table_data = table_info[key]
            columns = table_data[0]  # 表格的列名
            for field in columns:
                field_sql.append(field + " TEXT DEFAULT '' ")

            # 转字符串
            field_sql_str = ','.join(field_sql)
            # 建表sql
            create_table = self.create_table_sql(key, field_sql_str)
            # 执行建表
            sqlite.exec(create_table)


    # 进度条计算最大数: 即excel中所有sheet表的总行数
    def calc_record_maximum(self, table_info):
        maximum = 0
        for key in table_info.keys():
            table_data = table_info[key]
            dataframe = table_data[1]
            row_col_count = dataframe.shape
            maximum: int = maximum + row_col_count[0]
        return maximum

    # 计算进度条百分比
    def calc_percentage2(self, minimum, maximum):
        return '%d%s' % (int(round(minimum / maximum, 2) * 100), '%')

    # 计算进度条百分比
    def calc_percentage(self, currNum, maximum):
        return int(round(currNum / maximum, 2) * 100)

    # 插入数据
    def process_data(self, key, table_info, sqlite):

        field_sql = []
        table_data = table_info[key]
        columns = table_data[0]  # 表格的列名
        # 插入数据
        dataframe = table_data[1]  # 表格中的数据
        row_col_count = dataframe.shape  # 数据的行列数量
        row_count: int = row_col_count[0]  # 总行数
        col_count: int = row_col_count[1]  # 总列数

        field_sql.clear()
        for field in columns:
            field_sql.append('`' + field + '`')

        break_falg: bool = False
        lists: list = []
        col_indexs: list = []

        # 遍历行,添加数据
        for i in range(row_count):
            # 一行的数据并转为list
            values = dataframe.iloc[i].tolist()
            # 存在没有列明的列, 所以要根据列的长度截取没有一行
            values = values[0:len(columns)]

            if 'nan' == str(values[0]) and 'nan' == str(values[1]):
                break_falg = True

            # 添加属性 Filter, Pointer
            if 0 == i and ('Filter' == str(values[0]) or 'Pointer' == str(values[0])):
                for j in range(len(values)):
                    col = columns[j]
                    attr = values[j]
                    val = "'%s', '%s', '%s', %d" % (key, col, attr, 0)
                    sqlite.exec(self.insert_attribute(val))

                continue

            # 结束当前sheet的数据添加
            if True == break_falg:
                break

            lists.clear()
            col_indexs.clear()

            # 带有分号进行组合
            for j in range(len(values)):
                if str(values[j]).find(';') >= 0:
                    vals = values[j].split(';')
                    lists.append(vals)
                    col_indexs.append(j)
            results = []

            if len(lists) > 0:
                results = reduce((lambda x, y: [i + ';' + j for i in x for j in y]), lists)

            if len(results) > 0:
                for index, result in enumerate(results):

                    if str(result).find(';') >= 0:
                        vals = result.split(';')
                        for jndex, col_index in enumerate(col_indexs):
                            values[col_index] = vals[jndex]
                    else:
                        values[col_indexs[0]] = result

                    value_str = ''
                    for val in values:
                        value_str += " '%s', " % (val,)
                    insert_sql = self.create_insert_sql(key, field_sql, value_str, i)
                    sqlite.exec(insert_sql)
            else:
                value_str = ''
                for val in values:
                    value_str += " '%s', " % (val,)
                insert_sql = self.create_insert_sql(key, field_sql, value_str, i)
                sqlite.exec(insert_sql)


        return row_count

    # 创建insert
    def create_insert_sql(self, table_name, field_sql, value_str, row_number):
        insert_sql = " INSERT INTO %s( " % (table_name,)
        insert_sql += ','.join(field_sql)  # field
        insert_sql += " , sheet_name, sheet_cursor ) "
        insert_sql += " VALUES( "
        insert_sql += value_str  # value
        insert_sql += " ,'%s' " % (table_name,)  # sheetname
        insert_sql += " ,'%s' " % ((row_number + 2),)  # sheet position
        insert_sql += " ) "
        # print('insert-sql: ', insert_sql)
        return insert_sql

    # 创建表
    def create_table_sql(self, table_name, field_sql):
        _sql = 'CREATE TABLE IF NOT EXISTS %s ( ' % (table_name,)
        _sql += 'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, '
        _sql += field_sql
        _sql += " , sheet_name TEXT DEFAULT '' "
        _sql += " , sheet_cursor TEXT DEFAULT '' "
        _sql += ')'
        return _sql

    # 创建属性表
    def create_talbe_attribute(self):
        sql = '''
                CREATE TABLE IF NOT EXISTS attribute (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    table_name TEXT DEFAULT 'nan',
                    column_name  TEXT DEFAULT 'nan',
                    column_type  TEXT DEFAULT 'nan',
                    sequence integer DEFAULT 0
                )
              '''
        return sql

    # 创建属性表sql数据插入
    def insert_attribute(self, value_str):
        sql = 'INSERT INTO attribute(table_name, column_name, column_type, sequence) VALUES(%s) ' % (
            value_str,)
        # print('sql: ', sql)
        return sql


    def read_sql_file(self, path, sqlite):
        """
        读取文件中的sql 脚本
        :param path:
        :return:
        """
        sql_file = open(path, 'r', encoding='UTF-8')
        contents = sql_file.read()
        sqlite.exec_script(contents)
