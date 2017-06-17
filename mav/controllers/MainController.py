from PyQt4 import QtGui
class MainController(object):

    def __init__(self, model):
        self.model = model

    #### widget event functions ####
    def change_my_button(self, checked):
        self.model.my_button = checked
        print 'DEBUG: change_my_button called with arg value:', checked
