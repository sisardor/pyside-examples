import sys
# try:
#   from PySide2.QtCore import *
#   from PySide2.QtGui import *
#   from PySide2.QtWidgets import *
#   from PySide2 import __version__
#   from shiboken2 import wrapInstance
# except ImportError:
#   from PySide.QtCore import *
#   from PySide.QtGui import *
#   from PySide import __version__
#   from shiboken import wrapInstance

try:
    from PySide import QtGui, QtCore, QtNetwork
except Exception as e:
    from PyQt4 import QtGui, QtCore, QtNetwork
import sys, signal
import json
from collections import namedtuple
from models.Model import Model
from models.PaletteListModel import PaletteListModel
from models.PaletteTableModel import PaletteTableModel
from controllers.MainController import MainController
from views.MainView import MainView
import misc.icons
from models.TreeModel import TreeModel
from models.Node import Node, TransformNode, CameraNode, LightNode
#https://stackoverflow.com/questions/10024525/howto-draw-correct-css-border-in-header
# https://qt.developpez.com/doc/4.6/stylesheet-examples/#customizing-qtreeview

class XMLHighlighter(QtGui.QSyntaxHighlighter):

    #INIT THE STUFF
    def __init__(self, parent=None):
        super(XMLHighlighter, self).__init__(parent)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkMagenta)
        keywordFormat.setFontWeight(QtGui.QFont.Bold)

        keywordPatterns = ["\\b?xml\\b", "/>", ">", "<"]

        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        xmlElementFormat = QtGui.QTextCharFormat()
        xmlElementFormat.setFontWeight(QtGui.QFont.Bold)
        xmlElementFormat.setForeground(QtCore.Qt.green)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=[\s/>])"), xmlElementFormat))

        xmlAttributeFormat = QtGui.QTextCharFormat()
        xmlAttributeFormat.setFontItalic(True)
        xmlAttributeFormat.setForeground(QtCore.Qt.blue)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\=)"), xmlAttributeFormat))

        self.valueFormat = QtGui.QTextCharFormat()
        self.valueFormat.setForeground(QtCore.Qt.red)

        self.valueStartExpression = QtCore.QRegExp("\"")
        self.valueEndExpression = QtCore.QRegExp("\"(?=[\s></])")

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.gray)
        self.highlightingRules.append((QtCore.QRegExp("<!--[^\n]*-->"), singleLineCommentFormat))

    #VIRTUAL FUNCTION WE OVERRIDE THAT DOES ALL THE COLLORING
    def highlightBlock(self, text):

        #for every pattern
        for pattern, format in self.highlightingRules:

            #Create a regular expression from the retrieved pattern
            expression = QtCore.QRegExp(pattern)

            #Check what index that expression occurs at with the ENTIRE text
            index = expression.indexIn(text)

            #While the index is greater than 0
            while index >= 0:

                #Get the length of how long the expression is true, set the format from the start to the length with the text format
                length = expression.matchedLength()
                self.setFormat(index, length, format)

                #Set index to where the expression ends in the text
                index = expression.indexIn(text, index + length)

        #HANDLE QUOTATION MARKS NOW.. WE WANT TO START WITH " AND END WITH ".. A THIRD " SHOULD NOT CAUSE THE WORDS INBETWEEN SECOND AND THIRD TO BE COLORED
        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.valueStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.valueEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.valueEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength, self.valueFormat)

            startIndex = self.valueStartExpression.indexIn(text, startIndex + commentLength);

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        # listView = QtGui.QListView()
        # listView.show
        red = QtGui.QColor(255, 0, 0)
        green = QtGui.QColor(0, 255, 0)
        blue = QtGui.QColor(0, 0, 255)
        rowCount = 4
        columnCount = 2
        tableData1 = [ [ QtGui.QColor("#FFFF00") for i in range(columnCount)] for j in range(rowCount)]
        headers = ["Pallet0", "Colors"]



        entity =  json2obj('{"category":"groups","path":"/mnt/x19/mavisdev/projects/geotest/sequence/afg_0025","name":"afg_0025","description":"AFG_0025 sequence","fileImportPath":"","isGlobal":false,"project":"geotest","fields":{"priority":"medium","status":"idle"},"createdBy":"trevor","createdAt":"2016-09-13T20:28:04.745Z","updatedAt":"2017-05-31T21:38:19.935Z","id":"57d861546fef3a0001c87954","type":"sequence","mediaIds":[],"isTest":false}')
        entity1 = json2obj('{"category":"assets","path":"/mnt/x19/mavisdev/projects/geotest/globals/assets/wood_log","name":"wood_log","description":"a log that is wooden","fileImportPath":"","isGlobal":false,"project":"geotest","fields":{"priority":"medium","status":"review","grouping":"char","comp_status":"Ready","prod_status":"HIGH"},"createdBy":"dexplorer","createdAt":"2017-06-12T20:07:21.739Z","updatedAt":"2017-06-12T20:07:21.798Z","id":"593ef47973d9f40001cf898b","type":"assets","mediaIds":[],"isTest":false}')
        entity2 = json2obj('{"category":"assets","path":"/mnt/x19/mavisdev/projects/geotest/sequence/afg_0025/shots/afg_0025_0020/plates/plate_afg-0025__0020","name":"plate_afg-0025__0020","description":"plate asse for afg_0025_0020","latest":"583dc9eebc843d0001905bde","fileImportPath":"/mnt/x1/mavisdev/client_imports/geotest/afg_0025_0020/AFG_0025_0020_bg01_v001_LIN.exr","isGlobal":true,"project":"geotest","fields":{"priority":"low","status":"approved","startFrame":10,"endFrame":100,"pxAspect":1,"colorspace":"linear","fileType":"exr","width":1920,"height":1080,"lut":"","ccc":"","head":8,"tail":8,"handle":8},"createdBy":"trevor","createdAt":"2016-11-29T18:31:59.429Z","updatedAt":"2017-05-23T21:17:43.390Z","id":"583dc99fbc843d0001905bd9","type":"plates","mediaIds":[],"parentId":"57d861546fef3a0001c87960","isTest":false}')
        entity3 = json2obj('{"category":"tasks","path":"/mnt/x19/mavisdev/projects/geotest/globals/assets/wood_log/texture/tex_log","name":"tex_log","description":"texture the wood log","latest":"5941b18073d9f40001cf8a6c","fileImportPath":"","isGlobal":false,"project":"geotest","fields":{"priority":"urgent","status":"revised","grouping":"mtpg","comp_status":"In-Progress","prod_status":"HIGH"},"createdBy":"dexplorer","createdAt":"2017-06-12T20:08:10.814Z","updatedAt":"2017-06-14T21:58:24.772Z","id":"593ef4aa73d9f40001cf8992","type":"texture","mediaIds":[],"isTest":false}')
        entity4 = json2obj('{"category":"tasks","path":"/mnt/x19/mavisdev/projects/geotest/sequence/mdm_0202/shots/mdm_0202_0100/assets/tuktuka/model/tuktuk_model","name":"tuktuk_model","description":"published plate 6310","latest":"58c6ffe6e925cc00016a6b58","fileImportPath":"","isGlobal":false,"project":"geotest","fields":{"priority":"high","status":"revised","grouping":"vehi","comp_status":"Waiting","prod_status":"MEDIUM"},"createdBy":"trevor","createdAt":"2017-04-13T22:08:33.983Z","updatedAt":"2017-04-18T20:35:28.557Z","id":"589b4f9dc599d10001375de9","type":"model","mediaIds":[],"parentId":"589b4f10c599d10001375de2","isTest":false}')

        rootNode = Node('Hips')
        childNode0 = TransformNode('LeftPirateleg', entity, rootNode)
        childNode1 = Node('RightLeg',entity1, rootNode)
        childNode2 = Node('RightFoot',entity2, childNode1)
        childNode3 = CameraNode('Xxxree',entity3, rootNode)
        childNode4 = LightNode('kldjskfds',entity4, childNode1)

        tree = TreeModel(rootNode)





        model2 = PaletteTableModel(tableData1, headers)
        self.main_ctrl = MainController(self.model)
        self.main_view = MainView(model=self.model, main_ctrl=self.main_ctrl)
        self.main_view.test(model2,tree=tree)
        self.main_view.show()

        # model2.insertRows(0, 5)
        # model2.insertColumns(0, 5)
        model2.removeColumns(1,1)
        # tree.insertRows(0, 1)
        #
        #
        # self.threadClass = ThreadClass()
        # self.connect(self.threadClass, QtCore.SIGNAL('CPU_VALUE'), self.done)
        # self.threadClass.start()
        self.manager = QtNetwork.QNetworkAccessManager()
        self.manager.finished.connect(self.reply_finished)
        print(QtNetwork.QNetworkSession(QtNetwork.QNetworkConfigurationManager().defaultConfiguration()).State())
        self.request = QtNetwork.QNetworkRequest(QtCore.QUrl('http://www.planwallpaper.com/static/images/1080p-HD-Wallpapers-9.jpg'))
        print("Sending request")
        self.manager.get(self.request)
        self.manager2 = QtNetwork.QNetworkAccessManager()
        self.manager2.finished.connect(self.reply_finished)
        print(QtNetwork.QNetworkSession(QtNetwork.QNetworkConfigurationManager().defaultConfiguration()).State())
        self.request = QtNetwork.QNetworkRequest(QtCore.QUrl('http://lorempixel.com/1800/1400/city/'))
        print("Sending request")
        self.manager2.get(self.request)

        self.manager2 = QtNetwork.QNetworkAccessManager()
        self.manager2.finished.connect(self.reply_finished)
        print(QtNetwork.QNetworkSession(QtNetwork.QNetworkConfigurationManager().defaultConfiguration()).State())
        self.request = QtNetwork.QNetworkRequest(QtCore.QUrl('http://lorempixel.com/1800/1400/city/'))
        print("Sending request")
        self.manager2.get(self.request)

        self.manager3 = QtNetwork.QNetworkAccessManager()
        self.manager3.finished.connect(self.reply_finished)
        print(QtNetwork.QNetworkSession(QtNetwork.QNetworkConfigurationManager().defaultConfiguration()).State())
        self.request = QtNetwork.QNetworkRequest(QtCore.QUrl('http://lorempixel.com/1800/1400/city/'))
        print("Sending request")
        self.manager3.get(self.request)

    def reply_finished(self, reply):
        print("Request finishde")
        print(reply)
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            print "No error"
            available = reply.bytesAvailable()
            print available
            if available > 0:
                data = QtCore.QByteArray(reply.readAll())

                # imageProcessor = ImageProcessor(data);
                # image = imageProcessor.start()
                # self.main_view.ui.label.setPixmap(QtGui.QPixmap(image))

                self.imageProcessor = ThreadClass(data)
                self.imageProcessor.start()
                self.connect(self.imageProcessor, QtCore.SIGNAL('CPU_VALUE'), self.done)

        else:
            print 'There is error'
            print reply.errorString()
    def done(self, image=None):
        print "Done"
        self.main_view.ui.label.setPixmap(QtGui.QPixmap(image))
        # print image
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
        # time.sleep(10)
        return image

class ThreadClass(QtCore.QThread):
    """docstring for ThreadClass."""
    def __init__(self, imageData, parent=None):
        super(ThreadClass, self).__init__(parent)
        self.m_data = imageData

    def run(self):
        image = QtGui.QImage()
        image.loadFromData(self.m_data)
        self.emit(QtCore.SIGNAL('CPU_VALUE'), image)
        # time.sleep(2)





def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    print "close"
    QtGui.QApplication.quit()

signal.signal(signal.SIGINT, sigint_handler)

# class Async(QtCore.QThread):
#     def run(self):
#         print 'start'
#         self.manager = QtNetwork.QNetworkAccessManager()
#         self.manager.finished.connect(self.downloadFinished)
#         self.request = QtNetwork.QNetworkRequest(self.url)
#         self.reply = self.manager.get(self.request)
#         self.reply.downloadProgress.connect(self.progressCallback)
#         print 'start 2'

#     def download(self, url):
#         print 'download'
#         self.url = QtCore.QUrl(url)
#         self.returnData = None
#         #self.moveToThread(self)        ### <------  Added line that fixes the problem!
#         self.start()


#     def progressCallback(self, done, total):
#         self.emit(QtCore.SIGNAL('progress(int, int)'), done, total)

#     def downloadFinished(self, reply):
#         print "finished"
#         self.redirect = reply.attribute(QtNetwork.QNetworkRequest.RedirectionTargetAttribute).toUrl()
#         if not self.redirect.isEmpty():
#             self.request = QtNetwork.QNetworkRequest(self.redirect)
#             self.reply = self.manager.get(self.request)
#             self.reply.downloadProgress.connect(self.progressCallback)
#         else:
#             print self.reply.readAll()
#             self.emit(QtCore.SIGNAL('finished(PyQt_PyObject)'), str(self.reply.readAll()))
#             self.quit()


if __name__ == '__main__':
    app = App(sys.argv)
    #Create a QTextEdit widget
    xmlviewer = QtGui.QTextEdit()

    #Create our XMLHighlighter derived from QSyntaxHighlighter
    highlighter = XMLHighlighter(xmlviewer.document())

    #Set some xml code by hand or with the use of the xml.dom.minidom.Document class
    xmlviewer.setPlainText("insert xml here")
    sys.exit(app.exec_())
