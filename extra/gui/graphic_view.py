__author__ = 'mactep'

import sys

from PyQt4 import QtGui
from extra.gui.View.MainWindow import MainWindow

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    mw = MainWindow()
    mw.setVisible(True)

    sys.exit(app.exec_())