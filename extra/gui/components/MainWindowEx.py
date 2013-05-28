__author__ = 'mactep'

from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from extra.gui.components.ViewForms.MainWindow import Ui_MainWindow
from extra.gui.components.Model.ConfigurationModel import ConfigurationModel
from extra.gui.components.Model.DataModel import DataModel
from extra.gui.components.Model.RegionsModel import RegionsModel
from extra.gui.components.Model.HomologsModel import HomologsModel
from extra.gui.components.Model.HumanizationModel import HumanizationModel

from extra.share.humanize_tools import getMethods

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class MainWindowEx(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.domainList = []
        self.methodList = []
        self.humanizationMethods = getMethods()

        self.configuration = ConfigurationModel()
        self.dataModel = DataModel(self.configuration)

        # Ui
        self._init_domain_menu()
        self._init_humanization_menu()
        self._init_toolbar()
        self._create_toolbar()

        # Views
        self.regionsView = RegionsModel(self)
        self.homologsView = HomologsModel(self)
        self.humanizationsView = HumanizationModel(self)

        # Actions
        self._init_icons()
        self._init_actions()

    # Icons
    def _init_icons(self):
        self.ui.actionE_xit.setIcon(QIcon().fromTheme("application-exit"))
        self.ui.action_Open.setIcon(QIcon().fromTheme("document-open"))
        self.ui.actionSave_FASTA.setIcon(QIcon().fromTheme("document-save-as"))
        self.ui.action_Close.setIcon(QIcon().fromTheme("document-close"))
        self.ui.actionCreate_report.setIcon(QIcon().fromTheme("document-print-preview"))
        self.ui.action_Print.setIcon(QIcon().fromTheme("document-print"))
        self.ui.actionRun.setIcon(QIcon().fromTheme("media-playback-start"))
        self.ui.actionHumanize.setIcon(QIcon().fromTheme("system-run"))
        self.ui.actionConfigure_settings.setIcon(QIcon().fromTheme("document-properties"))
        self.ui.action_About.setIcon(QIcon().fromTheme("help-about"))
        self.ui.action_Help.setIcon(QIcon().fromTheme("help-contents"))

    # Ui
    def _init_domain_menu(self):
        for model in self.configuration.getDomainModels():
            self.domainList.append(QAction(model, self))
            self.domainList[-1].setCheckable(True)
            self.ui.menuDomain_Model.addAction(self.domainList[-1])

    def _init_humanization_menu(self):
        for method in self.humanizationMethods:
            self.methodList.append(QAction(method, self))
            self.methodList[-1].setCheckable(True)
            self.ui.menuHumanization_method.addAction(self.methodList[-1])

    def _init_toolbar(self):
        # Domain combo box
        self.domainCombo = QComboBox(self.ui.toolBar)
        for model in self.configuration.getDomainModels():
            self.domainCombo.addItem(model)
        self.domainCombo.setCurrentIndex(0)

        # Method combo box
        self.methodCombo = QComboBox(self.ui.toolBar)
        for method in self.humanizationMethods:
            self.methodCombo.addItem(method)
        self.methodCombo.setCurrentIndex(0)

    def _create_toolbar(self):
        self.ui.toolBar.addWidget(QLabel("Domain: "))
        self.ui.toolBar.addWidget(self.domainCombo)
        self.ui.toolBar.addWidget(QLabel("BLAST: "))
        self.ui.toolBar.addAction(self.ui.actionRun)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addWidget(QLabel("Method: "))
        self.ui.toolBar.addWidget(self.methodCombo)
        self.ui.toolBar.addWidget(QLabel("Humanize: "))
        self.ui.toolBar.addAction(self.ui.actionHumanize)

    # Actions
    def _init_domain_actions(self):
        # Make groups of actions
        self.domainActions = QActionGroup(self)
        for action in self.domainList:
            action.setActionGroup(self.domainActions)
        self.domainList[0].setChecked(True)

        # Connect actions and interface
        for action in self.domainList:
            action.triggered.connect(self.domainModelChanged)
        self.domainCombo.currentIndexChanged.connect(self.domainModelComboChanged)
        self.dataModel.setDomainModel(self.domainList[0].text())

    def _init_humanization_actions(self):
        # Make groups of actions
        self.humanizationActions = QActionGroup(self)
        for action in self.methodList:
            action.setActionGroup(self.humanizationActions)
        self.methodList[0].setChecked(True)

        # Connect actions and interface
        for action in self.methodList:
            action.triggered.connect(self.humanizationMethodChanged)
        self.methodCombo.currentIndexChanged.connect(self.humanizationMethodComboChanged)
        self.dataModel.setHumanizationMethod(self.methodList[0].text())

    def _init_actions_map(self):
        self.ui.action_Open.triggered.connect(self.openFiles)
        self.ui.action_Close.triggered.connect(self.closeFiles)
        self.ui.actionCreate_report.triggered.connect(self.createReport)
        self.ui.actionConfigure_settings.triggered.connect(self.configureSettings)
        self.ui.actionRun.triggered.connect(self.runBLAST)
        self.ui.actionHumanize.triggered.connect(self.runHumanization)
        self.ui.action_About.triggered.connect(self.about)
        self.ui.actionAbout_Qt.triggered.connect(QtGui.qApp.aboutQt)
        self.ui.action_Help.triggered.connect(self.help)

    def _init_data_actions_map(self):
        self.dataModel.dataModelChanged.connect(self.buildDataTree)
        self.dataModel.currentDomainChanged.connect(self.updateViews)
        self.ui.treeWidget.itemDoubleClicked.connect(self.changeCurrentDomain)

    def _init_actions(self):
        self._init_domain_actions()
        self._init_humanization_actions()
        self._init_data_actions_map()
        self._init_actions_map()

    # Slots
    @pyqtSlot(name="updateViews")
    def updateViews(self):
        domain = self.dataModel.getCurrent()
        self.regionsView.viewDomain(domain)
        self.homologsView.viewDomain(domain)
        self.humanizationsView.viewDomain(domain)

    @pyqtSlot(name="changeCurrentDomain")
    def changeCurrentDomain(self):
        item = self.ui.treeWidget.currentItem()
        if item.childCount() > 0:
            return
        p1 = item.parent()
        p2 = p1.parent()
        if not p2:
            #print str(p1.text(0)), None, str(item.text(0))
            self.dataModel.setCurrentDomain(str(p1.text(0)), None, str(item.text(0)))
        else:
            #print str(p2.text(0)), str(p1.text(0)), str(item.text(0))
            self.dataModel.setCurrentDomain(str(p2.text(0)), str(p1.text(0)), str(item.text(0)))

    @pyqtSlot(name="buildDataTree")
    def buildDataTree(self):
        self.ui.treeWidget.clear()
        data = self.dataModel.getData().getData()[self.dataModel.getDomainModel()]
        for basename in data:
            #print basename
            fastaItem = QTreeWidgetItem([basename])
            self.ui.treeWidget.addTopLevelItem(fastaItem)
            for ig in data[basename][0]:
                #print " "*4, ig
                igItem = QTreeWidgetItem([ig])
                fastaItem.addChild(igItem)
                for dom in ["VL", "VH"]:
                    #print " "*8, dom
                    domItem = QTreeWidgetItem([dom])
                    igItem.addChild(domItem)
            for dom in data[basename][1]:
                #print " "*4, dom
                domItem = QTreeWidgetItem([dom])
                fastaItem.addChild(domItem)

    @pyqtSlot(name="openFiles")
    def openFiles(self):
        fileList = QtGui.QFileDialog.getOpenFileNamesAndFilter(self, "Open files",
                                                               QDir.homePath(), "FASTA files (*.fa *.fasta)")[0]
        self.dataModel.loadData(fileList)

    @pyqtSlot(name="closeFiles")
    def closeFiles(self):
        self.dataModel.cleanup()

    @pyqtSlot(name="createReport")
    def createReport(self):
        pass

    @pyqtSlot(name="configureSettings")
    def configureSettings(self):
        pass

    @pyqtSlot(name="runBLAST")
    def runBLAST(self):
        self.dataModel.runBLAST()

    @pyqtSlot(name="runHumanization")
    def runHumanization(self):
        self.dataModel.runHumanization()

    @pyqtSlot(name="about")
    def about(self):
        pass

    @pyqtSlot(name="help")
    def help(self):
        pass

    @pyqtSlot(name="domainModelChanged")
    def domainModelChanged(self):
        model = self.sender().text()
        self.domainCombo.setCurrentIndex(self.domainCombo.findText(model))
        # Update data model
        self.dataModel.setDomainModel(model)

    @pyqtSlot(name="domainModelComboChanged")
    def domainModelComboChanged(self):
        model = self.domainCombo.currentText()
        for action in self.domainActions.actions():
            if model == action.text():
                action.setChecked(True)
                break
        # Update data model
        self.dataModel.setDomainModel(model)

    @pyqtSlot(name="humanizationMethodChanged")
    def humanizationMethodChanged(self):
        method = self.sender().text()
        self.methodCombo.setCurrentIndex(self.methodCombo.findText(method))
        # Update data model
        self.dataModel.setHumanizationMethod(method)

    @pyqtSlot(name="humanizationMethodComboChanged")
    def humanizationMethodComboChanged(self):
        method = self.methodCombo.currentText()
        for action in self.humanizationActions.actions():
            if method == action.text():
                action.setChecked(True)
                break
        # Update data model
        self.dataModel.setHumanizationMethod(method)

    @pyqtSlot(name="getDomainByTree")
    def getDomainByTree(self):
        pass