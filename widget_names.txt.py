#####################
# views\MainView.py #
#####################
from PySide import QtGui
from gen.ui_MainView import Ui_MainView

class MainView(QtGui.QMainWindow):

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

    def __init__(self, model, main_ctrl):
        self.model = model
        self.main_ctrl = main_ctrl
        super(MainView, self).__init__()
        self.build_ui()
        # register func with model for model update announcements
        self.model.subscribe_update_func(self.update_ui_from_model)

    def build_ui(self):
        self.ui = Ui_MainView()
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


###########################
# ctrls\MainController.py #
###########################
from PyQt4 import QtGui

class MainController(object):

    def __init__(self, model):
        self.model = model

    #### widget event functions ####
    def change_my_button(self, checked):
        self.model.my_button = checked
        print 'DEBUG: change_my_button called with arg value:', checked


##################
# model\Model.py #
##################
from PySide import QtGui

class Model(object):

    #### properties for value of Qt model contents ####

    def __init__(self):
        self._update_funcs = []
        self.config_section = 'settings'
        self.config_options = (
            ('my_button', 'getboolean'),
        )

        #### create Qt models for compatible widget types ####

        #### model variables ####
        self.my_button = None

    def subscribe_update_func(self, func):
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    def unsubscribe_update_func(self, func):
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    def announce_update(self):
        for func in self._update_funcs:
            func()


##########
# App.py #
##########
import sys
from PySide import QtGui
from model.Model import Model
from ctrls.MainController import MainController
from views.MainView import MainView

class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.main_ctrl = MainController(self.model)
        self.main_view = MainView(self.model, self.main_ctrl)
        self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
