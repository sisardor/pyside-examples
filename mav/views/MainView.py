# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress.ui'
#
# Created: Fri Jun 16 10:01:05 2017
#      by: PySide UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide import QtGui, QtCore, QtNetwork
except Exception as e:
    from PyQt4 import QtGui, QtCore, QtNetwork

# from gen import Ui_MainWindow
from treeUI import Ui_MainWindow
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s



style = """


QTreeView QHeaderView::section {
     background-color: #2c2f30;
     color: #AAAAAA;
     padding-left: 10px;
     border: 1px solid #3e4041;
     border-left: 0px;
     border-right: 0px;
     font-weight: 700;
 }
QTreeView {
    background: #2c2f30;
    color: #AAAAAA;
}

 QTreeView::branch {
    border-bottom: 1px solid #3e4041;
 }
 QTreeView::branch:selected {
    background-color: #575858 !important;
    color: #fff !important;
    fill: white;
 }
 QTreeView::item:selected {
    background-color: #575858 !important;
    color: #fff !important;
 }
 QTreeView::item {
    height: 35px;
    width: 250px;
    border-bottom: 1px solid #3e4041;
 }
 QTreeView::branch {
    width: 175px;
 }

 QTreeView::branch:has-children:!has-siblings:closed,
 QTreeView::branch:closed:has-children:has-siblings {
         border-image: none;
         image: url(icon-chevronright.svg);
 }
 QTreeView::branch:open:has-children:!has-siblings,
 QTreeView::branch:open:has-children:has-siblings  {
         border-image: none;
         image: url(icon-chevrondown.svg);
 }
 QTreeView::branch:open

"""
# QTreeView {
#      alternate-background-color: yellow;
#  }
#  QTreeView {
#      show-decoration-selected: 1;
#  }
# QTreeView::item:hover {
#      background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
#      border: 1px solid #bfcde4;
#  }

#  QTreeView::item:selected {
#      border: 1px solid #567dbc;
#  }

#  QTreeView::item:selected:active{
#      background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
#  }

#  QTreeView::item:selected:!active {
#      background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
#  }
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


    def test(self, model2, tree):
        # self.ui.listView = QtGui.QListView(self.ui.centralwidget)
        # self.ui.listView.setGeometry(QtCore.QRect(20, 110, 141, 281))


        # self.ui.treeView = QtGui.QTreeView(self.ui.centralwidget)
        # self.ui.treeView.setGeometry(QtCore.QRect(20, 110, 650, 381))
        self.ui.treeView.setIconSize(QtCore.QSize(37, 23))
        self.filelHeader = self.ui.treeView.header()
        self.filelHeader.setDefaultSectionSize(175)



        # self.ui.tableView = QtGui.QTableView(self.ui.centralwidget)
        # self.ui.tableView.setGeometry(QtCore.QRect(470, 110, 160, 281))

        # self.ui.comboBox = QtGui.QComboBox(self.ui.centralwidget)
        # self.ui.comboBox.setGeometry(QtCore.QRect(580, 110, 104, 26))

        self.ui.treeView.setModel(tree)
        self.ui.treeView.setStyleSheet(style)
        # self.ui.listView.setModel(tree)
        # self.ui.comboBox.setModel(model2)
        # self.ui.tableView.setModel(tree)
        #
        url = 'http://pipsum.com/935x310.jpg'
        # download_url = QtCore.QUrl(url)
        # manager = QtNetwork.QNetworkAccessManager()
        # request = QtNetwork.QNetworkRequest(download_url)
        # self.reply = manager.get(request)
        # # print self.reply
        # # self.reply.finished.connect(self._populate_textarea)
        # self.connect(self.reply, QtCore.SIGNAL('finished()'), self._populate_textarea);
        # print "END"
        return
        self.manager = QtNetwork.QNetworkAccessManager()
        self.manager.finished.connect(self.reply_finished)
        print(QtNetwork.QNetworkSession(QtNetwork.QNetworkConfigurationManager().defaultConfiguration()).State())
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        print("Sending request")
        self.manager.get(request)



    def reply_finished(self, reply):
        print("Request finishde")
        print(reply)
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            print "No error"
            available = reply.bytesAvailable()
            print available
            if available > 0:
                data = QtCore.QByteArray(reply.readAll())
                imageProcessor = ImageProcessor(data);
                image = imageProcessor.start()
                self.ui.label.setPixmap(QtGui.QPixmap(image))
        else:
            print 'There is error'
            print reply.errorString()



        # print(reply.readData(500))

    def _populate_textarea(self, arg):
        print "_populate_textarea"
        print arg
        print self._reply.readAll()

        print "_populate_textarea END"
        # parse_html()
        # self._textarea.setPlainText(unicode(self._reply.readAll(), 'utf-8'))
    def build_ui(self):

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



        #### set Qt model for compatible widget types ####

        #### connect widget signals to event functions ####
        # self.ui.pushButton_my_button.clicked.connect(self.on_my_button)

    def update_ui_from_model(self):
        print 'DEBUG: update_ui_from_model called'
        #### update widget values from model ####
        self.my_button = self.model.my_button

    #### widget signal event functions ####
    def on_my_button(self): self.main_ctrl.change_my_button(self.my_button)


import time
class ImageProcessor(object):
    """docstring for ImageProcessor"""
    def __init__(self, imageData, parent=None):
        super(ImageProcessor, self).__init__()
        print 'ImageProcessor'
        self.m_data = imageData

    def start(self):
        image = QtGui.QImage()
        image.loadFromData(self.m_data)
        # image = image.scaled(768, 500, QtCore.KeepAspectRatioByExpanding())
        time.sleep(2)
        return image
