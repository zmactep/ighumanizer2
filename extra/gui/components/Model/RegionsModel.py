__author__ = 'mactep'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from extra.gui.components.Common.AminoColors import AMINO_COLORS


class RegionsModel(QObject):
    def __init__(self, mainwindow):
        QObject.__init__(self)
        self.mainwindow = mainwindow

    def setupRegion(self, region, name):
        regions = {"FR1": self.mainwindow.ui.tableFR1,
                   "CDR1": self.mainwindow.ui.tableCDR1,
                   "FR2": self.mainwindow.ui.tableFR2,
                   "CDR2": self.mainwindow.ui.tableCDR2,
                   "FR3": self.mainwindow.ui.tableFR3,
                   "CDR3": self.mainwindow.ui.tableCDR3}
        table = regions[name]
        table.clear()
        if region:
            table.setColumnCount(len(region)-region.count('-'))
            table.setRowCount(1)
            ri = 0
            for c in region:
                if c != '-':
                    item = QTableWidgetItem(c)
                    try:
                        item.setBackgroundColor(AMINO_COLORS[c])
                    except KeyError:
                        item.setBackgroundColor(QColor(90, 90, 90))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    table.setItem(0, ri, item)
                    ri += 1
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.setFixedWidth(table.horizontalHeader().length())

    @pyqtSlot(name="viewDomain")
    def viewDomain(self, domain):
        if domain:
            self.mainwindow.ui.tabRegions.setEnabled(True)
        else:
            self.mainwindow.ui.tabRegions.setEnabled(False)
        for type in ["FR", "CDR"]:
            for i in xrange(1, 4):
                region = type + str(i)
                if domain:
                    self.setupRegion(domain.getDomain().get(region), region)
                else:
                    self.setupRegion(domain, region)