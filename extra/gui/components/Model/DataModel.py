__author__ = 'mactep'

from PyQt4.QtCore import *
from extra.gui.components.Model.FastaModel import FastaModel

from extra.share.humanize_tools import runMethod


class DataModel(QObject):
    # Signals
    currentDomainChanged = pyqtSignal()
    dataModelChanged = pyqtSignal()

    def __init__(self, configuration):
        QObject.__init__(self)
        self.configuration = configuration
        # Data
        self.data = FastaModel(configuration.getDomainModels())
        # Common
        self.currentDomain = None
        self.domainModel = None
        self.humanizationMethod = None

    def getData(self):
        return self.data

    def getDomainModel(self):
        return self.domainModel

    def getCurrent(self):
        return self.currentDomain

    # Slots
    @pyqtSlot(name="loadData")
    def loadData(self, fileList):
        self.data.loadData(fileList)
        self.currentDomain = None
        self.dataModelChanged.emit()
        self.currentDomainChanged.emit()

    @pyqtSlot(name="cleanup")
    def cleanup(self):
        self.data.cleanup()
        self.currentDomain = None
        self.dataModelChanged.emit()
        self.currentDomainChanged.emit()

    @pyqtSlot(name="domainModel")
    def setDomainModel(self, model):
        self.domainModel = str(model).lower()

    @pyqtSlot(name="setHumanizationMethod")
    def setHumanizationMethod(self, method):
        self.humanizationMethod = str(method)

    @pyqtSlot(name="setCurrentDomain")
    def setCurrentDomain(self, baseName, igName, domainName):
        self.currentDomain = self.data.getDomain(baseName, igName, domainName, self.domainModel)
        self.currentDomainChanged.emit()

    @pyqtSlot(name="runBLAST")
    def runBLAST(self):
        if self.currentDomain:
            self.data.rerunBLAST(self.currentDomain, self.configuration)
            self.currentDomainChanged.emit()

    @pyqtSlot(name="runTotalBLAST")
    def runTotalBLAST(self):
        self.data.rerunTotalBLAST_slow(self.configuration)
        self.currentDomainChanged.emit()

    @pyqtSlot(name="runHumanization")
    def runHumanization(self):
        if self.currentDomain:
            runMethod(self.currentDomain, self.humanizationMethod)
            self.currentDomainChanged.emit()