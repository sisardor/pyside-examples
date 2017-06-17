# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress.ui'
#
# Created: Fri Jun 16 10:01:05 2017
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from gen import Ui_MainWindow
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class MainView(QtGui.QMainWindow):
    def __init__(self, model, main_ctrl):
        super(MainView, self).__init__()
        self.model = model
        self.main_ctrl = main_ctrl
        self.build_ui()
        # register func with model for model update announcements
        self.model.subscribe_update_func(self.update_ui_from_model)
    #### properties for widget value ####
    @property
    def my_button(self):
        return self.ui.pushButton_my_button.isChecked()
    @my_button.setter
    def my_button(self, value):
        self.ui.pushButton_my_button.setChecked(value)

    #### properties for widget enabled state ####
    @property
    def my_button_enabled(self):
        return self.ui.pushButton_my_button.isEnabled()
    @my_button_enabled.setter
    def my_button_enabled(self, value):
        self.ui.pushButton_my_button.setEnabled(value)


    def test(self, model2):
        self.ui.listView = QtGui.QListView(self.ui.centralwidget)
        self.ui.listView.setGeometry(QtCore.QRect(20, 110, 141, 281))


        # self.ui.treeView = QtGui.QTreeView(self.ui.centralwidget)
        # self.ui.treeView.setGeometry(QtCore.QRect(180, 110, 141, 281))

        self.ui.tableView = QtGui.QTableView(self.ui.centralwidget)
        self.ui.tableView.setGeometry(QtCore.QRect(240, 110, 241, 281))

        self.ui.comboBox = QtGui.QComboBox(self.ui.centralwidget)
        self.ui.comboBox.setGeometry(QtCore.QRect(520, 110, 104, 26))



        self.ui.listView.setModel(model2)
        # self.ui.treeView.setModel(model2)
        self.ui.comboBox.setModel(model2)
        self.ui.tableView.setModel(model2)


    def build_ui(self):

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



        #### set Qt model for compatible widget types ####

        #### connect widget signals to event functions ####
        self.ui.pushButton_my_button.clicked.connect(self.on_my_button)

    def update_ui_from_model(self):
        print 'DEBUG: update_ui_from_model called'
        #### update widget values from model ####
        self.my_button = self.model.my_button

    #### widget signal event functions ####
    def on_my_button(self): self.main_ctrl.change_my_button(self.my_button)
