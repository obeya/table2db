#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import MainUi

from PyQt5.QtWidgets import QApplication, QMainWindow

# 启动界面
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = MainUi.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())