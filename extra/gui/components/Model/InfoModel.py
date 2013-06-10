__author__ = 'mactep'

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class InfoModel(QObject):
    def __init__(self, mainwindow):
        QObject.__init__(self)
        self.mainwindow = mainwindow
        self.data = mainwindow.dataModel
        self.processDict = {self.mainwindow.ui.tableDomain: self.processSourceTable,
                            self.mainwindow.ui.tableDomainHum: self.processSourceTable,
                            self.mainwindow.ui.tableGermlines: self.processGermlineTable,
                            self.mainwindow.ui.tableHomologs: self.processHomologTable,
                            self.mainwindow.ui.tableHumanizations: self.processHumanizationTable}

    def setDomain(self, dom):
        self.mainwindow.ui.lineName.setText(dom.name)
        self.mainwindow.ui.lineSeq.setText(dom.seq)

    def setTable(self, aa, pos, region, g_aa, h_aa, s_aa, hom):
        self.mainwindow.ui.tableAminoAcid.clearContents()
        self.mainwindow.ui.tableAminoAcid.setRowCount(1)
        self.mainwindow.ui.tableAminoAcid.setItem(0, 0, QTableWidgetItem(aa))
        self.mainwindow.ui.tableAminoAcid.setItem(0, 1, QTableWidgetItem(pos))
        self.mainwindow.ui.tableAminoAcid.setItem(0, 2, QTableWidgetItem(region))
        self.mainwindow.ui.tableAminoAcid.setItem(0, 3, QTableWidgetItem(g_aa))
        self.mainwindow.ui.tableAminoAcid.setItem(0, 4, QTableWidgetItem(h_aa))
        self.mainwindow.ui.tableAminoAcid.setItem(0, 5, QTableWidgetItem(s_aa))
        self.mainwindow.ui.tableAminoAcid.setItem(0, 6, QTableWidgetItem(hom))

    def processSourceTable(self, row, col):
        print "SOURCE"
        domain = self.data.currentDomain
        domainDom = domain.getDomain()
        self.setDomain(domainDom)
        aa = '-'
        pos = str(col+1)
        region = '-'
        g_aa = '-'
        h_aa = '-'
        regpos = domainDom.getRegionByPos(col)
        if regpos:
            region, aa = regpos
        s_aa = aa
        hom = '-'
        self.setTable(aa, pos, region, g_aa, h_aa, s_aa, hom)

    def processGermlineTable(self, row, col):
        print "GERMLINE"
        domain = self.data.currentDomain
        germlineDom = domain.germlineDomDict.keys()[row]
        germlineDom = domain.germlineDomDict[germlineDom]
        self.setDomain(germlineDom)

    def processHomologTable(self, row, col):
        print "HOMOLOG"
        domain = self.data.currentDomain
        homologDom = domain.homologDomDict.keys()[row]
        homologDom = domain.homologDomDict[homologDom]
        self.setDomain(homologDom)

    def processHumanizationTable(self, row, col):
        print "HUMANIZATION"
        domain = self.data.currentDomain
        variantDom = domain.humanizeDomDict.keys()[row]
        variantDom = domain.humanizeDomDict[variantDom]
        self.setDomain(variantDom)

    @pyqtSlot(name="cleanup")
    def cleanup(self):
        self.mainwindow.ui.lineName.clear()
        self.mainwindow.ui.lineSeq.clear()
        self.mainwindow.ui.tableAminoAcid.clearContents()

    @pyqtSlot(name="viewPosition")
    def viewPosition(self, table):
        print table.objectName(), table.currentRow(), table.currentColumn(), table.currentItem().text()
        self.processDict[table](table.currentRow(), table.currentColumn())