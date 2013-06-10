__author__ = 'mactep'

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from extra.gui.components.ViewForms.ConfigurationPanel import Ui_Form

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ConfigurationPanel(QDialog):
    def __init__(self, configurationModel):
        QDialog.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(_fromUtf8("Configuration"))
        self.setWindowFlags(Qt.Dialog)
        self.configurationModel = configurationModel
        self.load()
        self.ui.saveButton.clicked.connect(self.save)

    def load(self):
        self.ui.dbpathLineEdit.setText(self.configurationModel.getDBPath())
        self.ui.specieLineEdit.setText(self.configurationModel.getSpecie())
        self.ui.threadsSpinBox.setValue(self.configurationModel.getNumThreads())
        self.ui.alignmentsSpinBox.setValue(self.configurationModel.getNumAlignments())

    @pyqtSlot(name="save")
    def save(self):
        dbPath = str(self.ui.dbpathLineEdit.text())
        specie = str(self.ui.specieLineEdit.text())
        numThreads = int(self.ui.threadsSpinBox.text())
        numAlignments = int(self.ui.alignmentsSpinBox.text())
        self.configurationModel.set(dbPath, specie, numThreads, numAlignments)
        self.close()