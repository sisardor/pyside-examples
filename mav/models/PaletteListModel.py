from PySide import QtCore, QtGui

class PaletteListModel(QtCore.QAbstractListModel):
    """docstring for PaletteListModel."""
    def __init__(self, colors=[], parent=None):
        super(PaletteListModel, self).__init__(parent)

        self. colors = colors
    def rowCount(self, parent):
        return len(self.colors)

    def test(self):
        return self.colors[0]

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled| QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            color = QtGui.QColor(value)
            if color.isValid():
                self.colors[row] = color
                self.dataChanged.emit(index, index)
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString("Palette")
            else:
                return QtCore.QString("Color %1").arg(section)
    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.colors.insert(position, QtGui.QColor("#000000"))

        self.endInsertRows()
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
            return self.colors[index.row()].name()
        if role == QtCore.Qt.ToolTipRole:
            return "Hex code: " + self.colors[index.row()].name()
        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            value = self.colors[row]
            pixmap = QtGui.QPixmap(26,26)
            pixmap.fill(value)

            icon = QtGui.QIcon(pixmap)
            return icon

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.colors[row]
            return value.name()
