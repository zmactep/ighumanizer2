__author__ = 'mactep'

import PyQt4
from PyQt4 import QtGui
from extra.gui.components.ViewForms.MainWindow import Ui_MainWindow

from PyQt4.QtCore import pyqtSlot, pyqtSignal, QObject, SIGNAL, QString

from extra.share import fasta_tools
from extra.share.fasta_tools import readFASTA,parseFASTA2IG

from extra.share import igblastp_tools
from extra.share.igblastp_tools import runIgBlastp, parseIgBlastpOut

from extra.gui.components.Common.AminoColors import AMINO_COLORS


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(QtGui.QMainWindow, self).__init__(None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.viewDomain = False
        self.fastaInfo = {}
        self.fastaRes = {}

        self.humanizationMethods = {}
        self.loadMethods()

        self.createWidgets()
        self.fixActions()
        self.createToolBar()

    def loadMethods(self):
        pass

    def createWidgets(self):
        # Domain combo box
        self.domainCombo = QtGui.QComboBox(self.ui.toolBar)
        self.domainCombo.addItem("Kabat")
        self.domainCombo.addItem("IMGT")
        self.domainCombo.setCurrentIndex(0)

        # Method combo box
        self.methodCombo = QtGui.QComboBox(self.ui.toolBar)
        for method in self.humanizationMethods:
            self.methodCombo.addAction(self.humanizationMethods[method])

    def fixActions(self):
        # Fix icons
        self.ui.actionE_xit.setIcon(QtGui.QIcon().fromTheme("application-exit"))
        self.ui.action_Open.setIcon(QtGui.QIcon().fromTheme("document-open"))
        self.ui.actionSave_FASTA.setIcon(QtGui.QIcon().fromTheme("document-save-as"))
        self.ui.action_Close.setIcon(QtGui.QIcon().fromTheme("document-close"))
        self.ui.actionCreate_report.setIcon(QtGui.QIcon().fromTheme("document-print-preview"))
        self.ui.action_Print.setIcon(QtGui.QIcon().fromTheme("document-print"))
        self.ui.actionRun.setIcon(QtGui.QIcon().fromTheme("media-playback-start"))
        self.ui.actionHumanize.setIcon(QtGui.QIcon().fromTheme("system-run"))
        self.ui.actionConfigure_settings.setIcon(QtGui.QIcon().fromTheme("document-properties"))
        self.ui.action_About.setIcon(QtGui.QIcon().fromTheme("help-about"))
        self.ui.action_Help.setIcon(QtGui.QIcon().fromTheme("help-contents"))

        # Make groups of actions
        self.domainActions = QtGui.QActionGroup(self)
        self.ui.actionKabat.setActionGroup(self.domainActions)
        self.ui.actionIMGT.setActionGroup(self.domainActions)
        self.ui.actionKabat.setChecked(True)

        # Connect actions and interface
        self.ui.actionKabat.triggered.connect(self.domainModelChanged)
        self.ui.actionIMGT.triggered.connect(self.domainModelChanged)
        self.domainCombo.currentIndexChanged.connect(self.domainModelComboChanged)

        # Create signal-slot connections
        self.ui.action_Open.triggered.connect(self.loadFastaFiles)
        self.ui.action_Close.triggered.connect(self.closeFastaFiles)

        self.ui.treeWidget.itemClicked.connect(self.setDomainView)
        pass

    def createToolBar(self):
        self.ui.toolBar.addWidget(QtGui.QLabel("Domain: "))
        self.ui.toolBar.addWidget(self.domainCombo)
        self.ui.toolBar.addWidget(QtGui.QLabel("IgBLAST: "))
        self.ui.toolBar.addAction(self.ui.actionRun)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addWidget(QtGui.QLabel("Method: "))
        self.ui.toolBar.addWidget(self.methodCombo)
        self.ui.toolBar.addWidget(QtGui.QLabel("Humanize: "))
        self.ui.toolBar.addAction(self.ui.actionHumanize)

    def generateTree(self):
        self.ui.treeWidget.clear()

        for fasta in self.fastaInfo:
            fastaItem = QtGui.QTreeWidgetItem([fasta])
            self.ui.treeWidget.addTopLevelItem(fastaItem)

            igDict  = self.fastaInfo[fasta][0]
            domDict = self.fastaInfo[fasta][1]

            for ig in igDict:
                igItem = QtGui.QTreeWidgetItem([ig])
                fastaItem.addChild(igItem)

                for dom in igDict[ig]:
                    igItem.addChild(QtGui.QTreeWidgetItem([dom, igDict[ig][dom]]))

            for dom in domDict:
                domItem = QtGui.QTreeWidgetItem([dom, domDict[dom]])
                fastaItem.addChild(domItem)

    def domain2item(self, domain):
        # domain: fasta/./ig/./domain or fasta.domain
        dom = domain.split('/./')
        for i in xrange(self.ui.treeWidget.topLevelItemCount()):
            fasta = self.ui.treeWidget.topLevelItem(i)
            if fasta.text(0) == dom[0]:
                for j in xrange(fasta.childCount()):
                    igdom = fasta.child(j)
                    if igdom.text(0) == dom[1]:
                        if len(dom) == 2:
                            return igdom
                        else:
                            for k in xrange(igdom.childCount()):
                                if igdom.child(k).text(0) == dom[2]:
                                    return igdom.child(k)

    @pyqtSlot(name="item2domain")
    def item2domain(self):
        item = self.ui.treeWidget.selectedItems()[0]
        if item.childCount() > 0:
            return None

        l = [item.text(0)]
        tmp = item.parent()
        while tmp != None:
            l.append(tmp.text(0))
            tmp = tmp.parent()

        ll = [str(i) for i in l]
        s = "/./".join(ll[::-1])
        return s

    @pyqtSlot(name="domain2res")
    def domain2res(self, domain):
        dom = domain.split('/./')
        fq = self.fastaRes[dom[0]][str(self.domainCombo.currentText().toLower())]
        dom = dom[1:]
        if len(dom) == 1:
            return fq[1][dom[0]]
        else:
            return fq[0][dom[0]].get(dom[1])

    @pyqtSlot(name="processDomain")
    def processDomain(self, domainItem):
        pass

    @pyqtSlot(name="domainModelChanged")
    def domainModelChanged(self):
        sender = self.sender()
        if sender == self.ui.actionKabat:
            self.domainCombo.setCurrentIndex(0)
        elif sender == self.ui.actionIMGT:
            self.domainCombo.setCurrentIndex(1)

    @pyqtSlot(name="domainModelComboChanged")
    def domainModelComboChanged(self):
        if self.domainCombo.currentText() == "Kabat":
            self.ui.actionKabat.setChecked(True)
        elif self.domainCombo.currentText() == "IMGT":
            self.ui.actionIMGT.setChecked(True)

    @pyqtSlot(name="setupRegion")
    def setupRegion(self, region, regName):
        tbl = None
        if regName == "FR1":
            tbl = self.ui.tableFR1
        elif regName == "FR2":
            tbl = self.ui.tableFR2
        elif regName == "FR3":
            tbl = self.ui.tableFR3
        elif regName == "CDR1":
            tbl = self.ui.tableCDR1
        elif regName == "CDR2":
            tbl = self.ui.tableCDR2
        elif regName == "CDR3":
            tbl = self.ui.tableCDR3
        else:
            return

        tbl.clear()
        tbl.setColumnCount(len(region))
        tbl.setRowCount(1)
        for i in xrange(len(region)):
            item = None
            if region[i] != "-":
                item = QtGui.QTableWidgetItem(region[i])
                item.setBackgroundColor(AMINO_COLORS[region[i]])
                item.setFlags(PyQt4.QtCore.Qt.ItemIsSelectable | PyQt4.QtCore.Qt.ItemIsEnabled)
            # else:
            #     item = QtGui.QTableWidgetItem("")
            tbl.setItem(0,i, item)
        tbl.resizeColumnsToContents()
        tbl.resizeRowsToContents()
        tbl.setFixedWidth(tbl.horizontalHeader().length())


    @pyqtSlot(name="setupDomain")
    def setupDomain(self, resDomain):
        # Region view
        self.ui.tabRegions.setEnabled(True)
        for i in ["FR", "CDR"]:
            for j in [1,2,3]:
                s = i + str(j)
                self.setupRegion(resDomain.getDomain().get(s), s)

        # Homologs view

        # Humanization view

        # Info view

    @pyqtSlot(name="setDomainView")
    def setDomainView(self):
        self.viewDomain = True

        s = self.item2domain()
        if s == None:
            return
        r = self.domain2res(s)
        self.setupDomain(r)

    @pyqtSlot(name="clearViews")
    def clearViews(self):
        self.viewDomain = False

        # Region view
        self.ui.tableFR1.clear()
        self.ui.tableFR2.clear()
        self.ui.tableFR3.clear()
        self.ui.tableCDR1.clear()
        self.ui.tableCDR2.clear()
        self.ui.tableCDR3.clear()
        self.ui.tabRegions.setDisabled(True)

        # Homolog view
        self.ui.tableDomain.clear()
        self.ui.tableGermlines.clear()
        self.ui.tableHomologs.clear()
        self.ui.tabHomologs.setDisabled(True)

        # Humanization view
        self.ui.tableDomainHum.clear()
        self.ui.tableHumanizations.clear()
        self.ui.tabHumanization.setDisabled(True)

        # Info view
        self.ui.lineName.clear()
        self.ui.lineSeq.clear()
        self.ui.tableAminoAcid.clear()
        self.ui.tabInfoWidget.setDisabled(True)

    @pyqtSlot(name="loadFastaFiles")
    def loadFastaFiles(self):
        fileList = QtGui.QFileDialog.getOpenFileNamesAndFilter(self,"Open files",
                                                               PyQt4.QtCore.QDir.homePath(),
                                                               "FASTA files (*.fa *.fasta)")
        firstPBStep = 50.0/len(fileList[0])
        lastValue = 0
        self.ui.progressBar.setValue(lastValue)

        self.fastaInfo = {}
        self.fastaRes = {}
        for i in fileList[0]:
            if i == "":
                continue
            name = str(i).split('/')[-1]
            name = name[:name.rfind('.')]

            resKabat = runIgBlastp(str(i), igblastp_tools.GERMLINE_HUMAN, igblastp_tools.DOMAIN_KABAT)
            bodKabat = parseIgBlastpOut(resKabat, str(i))
            lastValue += firstPBStep
            self.ui.progressBar.setValue(lastValue)

            resIMGT = runIgBlastp(str(i), igblastp_tools.GERMLINE_HUMAN, igblastp_tools.DOMAIN_KABAT)
            bodIMGT  = parseIgBlastpOut(resIMGT, str(i))
            lastValue += firstPBStep
            self.ui.progressBar.setValue(lastValue)

            self.fastaRes[name] = {"kabat" : bodKabat, "imgt" : bodIMGT}
            self.fastaInfo[name] = parseFASTA2IG(readFASTA(str(i)))

        self.generateTree()

    @pyqtSlot(name="closeFastaFiles")
    def closeFastaFiles(self):
        self.fastaInfo = {}
        self.fastaRes = {}

        self.ui.progressBar.setValue(0)
        self.ui.treeWidget.clear()

        self.clearViews()

    @pyqtSlot(name="updateDomainModelView")
    def updateDomainModelView(self):
        pass