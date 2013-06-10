__author__ = 'mactep'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from extra.gui.components.Common.AminoColors import AMINO_COLORS


class HumanizationModel(QObject):
    def __init__(self, mainwindow):
        QObject.__init__(self)
        self.mainwindow = mainwindow

    def setupHumanization(self, variant, i):
        table = self.mainwindow.ui.tableHumanizations
        for j, c in enumerate(variant):
            item = QTableWidgetItem(c)
            try:
                item.setBackgroundColor(AMINO_COLORS[c])
            except KeyError:
                item.setBackgroundColor(QColor(90, 90, 90))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table.setItem(i, j, item)

    def setupDomainSeq(self, domain):
        table = self.mainwindow.ui.tableDomainHum
        table.clear()
        if domain:
            seq = domain.getDomain().generatedSeq()
            table.setColumnCount(len(seq))
            table.setRowCount(1)
            for i, c in enumerate(seq):
                item = QTableWidgetItem(c)
                try:
                    item.setBackgroundColor(AMINO_COLORS[c])
                except KeyError:
                    item.setBackgroundColor(QColor(90, 90, 90))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                table.setItem(0, i, item)

    @pyqtSlot(name="viewDomain")
    def viewDomain(self, domain):
        self.mainwindow.ui.tableDomainHum.clear()
        self.mainwindow.ui.tableHumanizations.clear()
        if domain:
            self.mainwindow.ui.tabHumanization.setEnabled(True)
            self.setupDomainSeq(domain)
            tablecol = len(domain.getDomain().generatedSeq())
            tablerow = len(domain.humanizeDomDict)
            self.mainwindow.ui.tableHumanizations.setColumnCount(tablecol)
            self.mainwindow.ui.tableHumanizations.setRowCount(tablerow)
            for i, variant in enumerate(domain.humanizeDomDict):
                seq = domain.humanizeDomDict[variant].generatedSeq()
                self.setupHumanization(seq, i)
            for table in [self.mainwindow.ui.tableDomainHum,
                          self.mainwindow.ui.tableHumanizations]:
                table.resizeColumnsToContents()
                table.resizeRowsToContents()
                # table.setFixedWidth(table.horizontalHeader().length())
        else:
            self.mainwindow.ui.tabHumanization.setEnabled(False)