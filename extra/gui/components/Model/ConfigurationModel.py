__author__ = 'mactep'

from PyQt4.QtCore import *


class ConfigurationModel(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.domainModels = ["Kabat", "IMGT"]
        self.settings = QSettings("biocad", "ighumanizer2")

    def getDomainModels(self):
        return self.domainModels

    def set(self, dbPath, specie, numThreads, numAlignments):
        self.settings.setValue("dbPath", dbPath)
        self.settings.setValue("specie", specie)
        self.settings.setValue("numThreads", numThreads)
        self.settings.setValue("numAlignments", numAlignments)
        self.settings.sync()

    def save(self):
        self.settings.sync()

    def setDBPath(self, dbPath):
        self.settings.setValue("dbPath", dbPath)

    def setSpecie(self, specie):
        self.settings.setValue("specie", specie)

    def setNumThreads(self, numThreads):
        self.settings.setValue("numThreads", numThreads)

    def setNumAlignments(self, numAlignments):
        self.settings.setValue("numAlignments", numAlignments)

    def getDBPath(self):
        return str(self.settings.value("dbPath", "").toString())

    def getSpecie(self):
        return str(self.settings.value("specie", "human").toString())

    def getNumThreads(self):
        return int(self.settings.value("numThreads", 1).toInt()[0])

    def getNumAlignments(self):
        return int(self.settings.value("numAlignments", 10).toInt()[0])