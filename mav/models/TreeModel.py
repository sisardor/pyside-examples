from PySide import QtCore, QtGui
import misc.icons
from Node import Node

class TreeModel(QtCore.QAbstractItemModel):
	"""docstring for TreeModel"""
	def __init__(self, root, parent=None):
		super(TreeModel, self).__init__(parent)
		self.rootNode = root
		

	def rowCount(self, parent):
		if not parent.isValid():
			parentNode = self.rootNode
		else: 
			parentNode = parent.internalPointer()

		return parentNode.childCount()

	def columnCount(self, parent):
		return 2

	def setColumnWidth(self, column, width):
		print 'setColumnWidth'
		pass


	def data(self, index, role):
		if not index.isValid():
			return None
		node = index.internalPointer()

		if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
			if index.column() == 0:
				return node.nameX()
			else:
				return node.typeInfo()

		

		if role == QtCore.Qt.DecorationRole:
			if index.column() == 0:
				typeInfo = node.typeInfo()
				if typeInfo == "LIGHT":
					return QtGui.QIcon(QtGui.QPixmap(":/Light.jpg"))

				if typeInfo == "TRANSFORM":
					return QtGui.QIcon(QtGui.QPixmap(":/Transform.jpg"))

				if typeInfo == "CAMERA":
					return QtGui.QIcon(QtGui.QPixmap(":/Camera.jpg"))

	def getNode(self, index):
		if index.isValid():	
			node = index.internalPointer()
			if node:
				return node
		return self.rootNode

	def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
		parentNode = self.getNode(parent)

		self.beginInsertRows(parent, position, position + rows -1)
		for row in range(rows):
			childCount = parentNode.childCount()
			childNode = Node("untitled" + str(childCount))
			success = parentNode.insertChild(position,childNode)
		self.endInsertRows()

		return success

	def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
		parentNode = self.getNode(parent)
		self.beginRemoveRows(parent, position, position + rows -1)
		for row in range(rows):
			success = parentNode.removeChild(position)

		self.endRemoveRows()
		return success

	def setData(self, index, value, role=QtCore.Qt.EditRole):
		if index.isValid():
			if role == QtCore.Qt.EditRole:
				node = index.internalPointer()
				node.setName(value)
				self.dataChanged.emit(index, index)
				return True
		return False
	def headerData(self, section, orientation, role):
		if role == QtCore.Qt.SizeHintRole:
			print section
			print "giving size hint %s"%role
			return QtCore.QSize(200,35)
		if role == QtCore.Qt.DisplayRole:
			if section == 0:
				return "FirstHead"
			else:
				return "TreeModel"

	def flags(self, index):
		return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

	def parent(self, index):
		node = self.getNode(index)
		parentNode = node.parentX()

		if parentNode == self.rootNode:
			return QtCore.QModelIndex()
		return self.createIndex(parentNode.row(), 0, parentNode)

	def index(self, row, column, parent):
		parentNode = self.getNode(parent)

		childItem = parentNode.child(row)

		if childItem:
			return self.createIndex(row, column, childItem)
		else:
			return QtCore.QModelIndex()
