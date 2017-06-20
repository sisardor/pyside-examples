import Node

class TransformNode(Node):
	"""docstring for TransformNode"""
	def __init__(self, name, parent):
		super(TransformNode, self).__init__(name, parent)

	def typeInfo(self):
		return "TRANSFORM"

class CameraNode(Node):
	"""docstring for CameraNode"""
	def __init__(self, name, parent):
		super(CameraNode, self).__init__(name, parent)

	def typeInfo(self):
		return "CAMERA"


class LightNode(Node):
	"""docstring for LightNode"""
	def __init__(self, name, parent):
		super(LightNode, self).__init__(name, parent)

	def typeInfo(self):
		return "LIGHT"
