__author__ = 'mactep'

from PyQt4.QtCore import *


class ConfigurationModel(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.domainModels = ["Kabat", "IMGT"]

    def getDomainModels(self):
        return self.domainModels