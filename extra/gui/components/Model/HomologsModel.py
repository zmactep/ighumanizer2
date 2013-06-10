__author__ = 'mactep'

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from extra.gui.components.Common.AminoColors import AMINO_COLORS


class HomologsModel(QObject):
    def __init__(self, mainwindow):
        QObject.__init__(self)
        self.mainwindow = mainwindow

    def setupHomolog(self, homolog, germline, i):
        table = self.mainwindow.ui.tableHomologs
        if germline:
            table = self.mainwindow.ui.tableGermlines
        for j, c in enumerate(homolog):
            item = QTableWidgetItem(c)
            try:
                item.setBackgroundColor(AMINO_COLORS[c])
            except KeyError:
                item.setBackgroundColor(QColor(90, 90, 90))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table.setItem(i, j, item)

    def setupDomainSeq(self, domain):
        table = self.mainwindow.ui.tableDomain
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
        self.mainwindow.ui.tableDomain.clear()
        self.mainwindow.ui.tableGermlines.clear()
        self.mainwindow.ui.tableHomologs.clear()
        if domain:
            self.mainwindow.ui.tabHomologs.setEnabled(True)
            self.setupDomainSeq(domain)
            tablecol = len(domain.getDomain().generatedSeq())
            # Germlines
            tablerow = len(domain.germlineDomDict)
            self.mainwindow.ui.tableGermlines.setColumnCount(tablecol)
            self.mainwindow.ui.tableGermlines.setRowCount(tablerow)
            for i, homolog in enumerate(domain.germlineDomDict):
                seq = domain.germlineDomDict[homolog].generatedSeq()
                self.setupHomolog(seq, True, i)
            # Homologs
            tablerow = len(domain.homologDomDict)
            self.mainwindow.ui.tableHomologs.setColumnCount(tablecol)
            self.mainwindow.ui.tableHomologs.setRowCount(tablerow)
            for i, homolog in enumerate(domain.homologDomDict):
                seq = domain.homologDomDict[homolog].generatedSeq()
                self.setupHomolog(seq, False, i)
            for table in [self.mainwindow.ui.tableDomain,
                          self.mainwindow.ui.tableGermlines,
                          self.mainwindow.ui.tableHomologs]:
                table.resizeColumnsToContents()
                table.resizeRowsToContents()
                # table.setFixedWidth(table.horizontalHeader().length())
        else:
            self.mainwindow.ui.tabHomologs.setEnabled(False)