# import sys
try:
    from PySide import QtGui, QtCore
except Exception as e:
    from PyQt4 import QtGui, QtCore


# https://qt.developpez.com/doc/4.6/stylesheet-examples/#customizing-qtreeview


class Node(object):
	"""docstring for Node"""
	def __init__(self, name, entity=None, parent=None):
		# super(Node, self).__init__(parent)
		self.name = name
		self.entity = entity
		self.children = []
		self.parent = parent

		if parent is not None:
			parent.addChild(self)


	def typeInfo(self):
		return self.entity.type

	def addChild(self, child):
		self.children.append(child)

	def insertChild(self, position, child):
		if position < 0 or position > len(self.children):
			return False

		self.children.insert(position, child)
		child.parent = self
		return True

	def removeChild(self, position):
		if position < 0 or position > len(self.children):
			return False

		child = self.children.pop(position)
		child.parent = None
		return True

	def setName(self, name):
		self.name = name

	def nameX(self):
		return self.name

	def child(self, row):
		return self.children[row]

	def childCount(self):
		return len(self.children)

	def parentX(self):
		return self.parent

	def row(self):
		if self.parent is not None:
			return self.parent.children.index(self)

	def log(self, tabLevel = -1):
		output = ""
		tabLevel += 1
		for i in range(tabLevel):
			output += '\t'

		output += "|------" + self.name + '\n'

		for child in self.children:
			output +=child.log(tabLevel)

		tabLevel -= 1
		output += '\n'
		return output

	def __repr__(self):
		return self.log()



class TransformNode(Node):
	"""docstring for TransformNode"""
	def __init__(self, name, entity, parent=None):
		super(TransformNode, self).__init__(name, entity, parent)

	def typeInfo(self):
		return self.entity.type

class CameraNode(Node):
	"""docstring for CameraNode"""
	def __init__(self, name, entity, parent=None):
		super(CameraNode, self).__init__(name, entity, parent)

	def typeInfo(self):
		return self.entity.type


class LightNode(Node):
	"""docstring for LightNode"""
	def __init__(self, name, entity, parent=None):
		super(LightNode, self).__init__(name, entity, parent)

	def typeInfo(self):
		return self.entity.type


# if __name__ == '___main__':

# print "___main__"

# app = QtGui.QApplication(sys.argv)
# app.setStyle("plastique")


# rootNode = Node('Hips')
# childNode0 = Node('LeftPirateleg', rootNode)
# childNode1 = Node('RightLeg', rootNode)
# childNode2 = Node('RightFoot', childNode1)
# childNode3 = CameraNode('Xxxree', rootNode)
# childNode4 = LightNode('kldjskfds', childNode1)

# print rootNode

# model = TreeModel(rootNode)

# treeview = QtGui.QTreeView()
# treeview.show()
# treeview.setModel(model)

# sys.exit(app.exec_())
