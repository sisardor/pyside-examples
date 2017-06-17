import sys
from PyQt4 import QtGui, QtCore
from models.Model import Model
from models.PaletteListModel import PaletteListModel
from models.PaletteTableModel import PaletteTableModel
from controllers.MainController import MainController
from views.MainView import MainView

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

        model2 = PaletteTableModel(tableData1, headers)
        self.main_ctrl = MainController(self.model)
        self.main_view = MainView(model=self.model, main_ctrl=self.main_ctrl)
        self.main_view.test(model2)
        self.main_view.show()

        # model2.insertRows(0, 5)
        # model2.insertColumns(0, 5)
        model2.removeColumns(1,1)

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
