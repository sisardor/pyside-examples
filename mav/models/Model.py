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
        print func
        if func not in self._update_funcs:
            self._update_funcs.append(func)

    def unsubscribe_update_func(self, func):
        if func in self._update_funcs:
            self._update_funcs.remove(func)

    def announce_update(self):
        print self._update_funcs
        for func in self._update_funcs:
            func()
