# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ConfigurationPanel.ui'
#
# Created: Mon Jun 10 00:05:33 2013
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.dbpathLineEdit = QtGui.QLineEdit(Form)
        self.dbpathLineEdit.setObjectName(_fromUtf8("dbpathLineEdit"))
        self.horizontalLayout.addWidget(self.dbpathLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.specieLineEdit = QtGui.QLineEdit(Form)
        self.specieLineEdit.setObjectName(_fromUtf8("specieLineEdit"))
        self.horizontalLayout_2.addWidget(self.specieLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.threadsSpinBox = QtGui.QSpinBox(Form)
        self.threadsSpinBox.setMinimum(1)
        self.threadsSpinBox.setMaximum(100)
        self.threadsSpinBox.setObjectName(_fromUtf8("threadsSpinBox"))
        self.horizontalLayout_3.addWidget(self.threadsSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.alignmentsSpinBox = QtGui.QSpinBox(Form)
        self.alignmentsSpinBox.setMinimum(1)
        self.alignmentsSpinBox.setMaximum(100)
        self.alignmentsSpinBox.setObjectName(_fromUtf8("alignmentsSpinBox"))
        self.horizontalLayout_4.addWidget(self.alignmentsSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.saveButton = QtGui.QPushButton(Form)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_5.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Database path:", None))
        self.label_2.setText(_translate("Form", "Specie:", None))
        self.label_3.setText(_translate("Form", "Number of threads:", None))
        self.label_4.setText(_translate("Form", "Number of alignments:", None))
        self.saveButton.setText(_translate("Form", "Save", None))

