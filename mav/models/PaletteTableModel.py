try:
    from PySide import QtGui, QtCore
except Exception as e:
    from PyQt4 import QtGui, QtCore
try:
    from PySide.QtCore import QString
except ImportError:
    QString = str

class PaletteTableModel(QtCore.QAbstractTableModel):
    """docstring for PaletteTableModel."""
    def __init__(self, colors=[[]], headers=[], parent=None):
        super(PaletteTableModel, self).__init__(parent)

        self.colors = colors
        self.headers = headers
    def rowCount(self, parent):
        return len(self.colors)

    def columnCount(self, parent):
        return len(self.colors[0])

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled| QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        print "setData"
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            color = QtGui.QColor(value)
            if color.isValid():
                self.colors[row][column] = color
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self.headers):
                    return self.headers[section]
                else:
                    return "TEMP"
            else:
                return QString("Color %s")%(section)

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            defaultValues = [QtGui.QColor("#000000") for i in range(self.columnCount(None))]
            self.colors.insert(position, defaultValues)

        self.endInsertRows()
        return True

    def insertColumns(self, position, columns, parent = QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)
        rowCount = len(self.colors)

        for i in range(columns):
            for j in range(rowCount):
                self.colors[j].insert(position, QtGui.QColor("#000000"))

        self.endInsertColumns()
        return True

    def removeColumns(self, position, columns, parent = QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)
        rowCount = len(self.colors)

        for i in range(columns):
            for j in range(rowCount):
                value = self.colors[j][i]
                self.colors[j].remove(value)

        self.endRemoveColumns()
        return True
    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            value = self.colors[position]
            self.colors.remove(value)
        self.endRemoveRows()
        return True

    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            return self.colors[row][column].name()
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            column = index.column()
            return "Hex code: " + self.colors[row][column].name()
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            column = index.column()
            value = self.colors[row][column]
            pixmap = QtGui.QPixmap(26,26)
            pixmap.fill(value)

            icon = QtGui.QIcon(pixmap)
            return icon

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.colors[row][column]
            return value.name()
