__author__ = 'mactep'

import sys

from PyQt4 import QtGui
from extra.gui.components.MainWindowEx import MainWindowEx


def run():
    app = QtGui.QApplication(sys.argv)

    mw = MainWindowEx()
    mw.setVisible(True)

    sys.exit(app.exec_())

if __name__ == "__main__":
    run()