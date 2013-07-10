# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dbmanagment_ui.ui'
#
# Created: Mon Jul  8 20:14:32 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DBmanagment(object):
    def setupUi(self, DBmanagment):
        DBmanagment.setObjectName("DBmanagment")
        DBmanagment.resize(400, 300)
        self.beckup = QtGui.QPushButton(DBmanagment)
        self.beckup.setGeometry(QtCore.QRect(290, 60, 93, 27))
        self.beckup.setObjectName("beckup")
        self.label = QtGui.QLabel(DBmanagment)
        self.label.setGeometry(QtCore.QRect(50, 0, 291, 51))
        self.label.setObjectName("label")
        self.restore = QtGui.QPushButton(DBmanagment)
        self.restore.setGeometry(QtCore.QRect(290, 236, 93, 41))
        self.restore.setObjectName("restore")
        self.calendarWidget = QtGui.QCalendarWidget(DBmanagment)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 40, 261, 179))
        self.calendarWidget.setObjectName("calendarWidget")
        self.upload = QtGui.QPushButton(DBmanagment)
        self.upload.setGeometry(QtCore.QRect(40, 247, 221, 20))
        self.upload.setObjectName("upload")

        self.retranslateUi(DBmanagment)
        QtCore.QMetaObject.connectSlotsByName(DBmanagment)

    def retranslateUi(self, DBmanagment):
        DBmanagment.setWindowTitle(QtGui.QApplication.translate("DBmanagment", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.beckup.setText(QtGui.QApplication.translate("DBmanagment", "Beckup", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DBmanagment", "             BeckUP e Restore DB Pyarchinit", None, QtGui.QApplication.UnicodeUTF8))
        self.restore.setText(QtGui.QApplication.translate("DBmanagment", "Restore", None, QtGui.QApplication.UnicodeUTF8))
        self.upload.setText(QtGui.QApplication.translate("DBmanagment", "Scegli il file da ripristinare", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DBmanagment = QtGui.QDialog()
    ui = Ui_DBmanagment()
    ui.setupUi(DBmanagment)
    DBmanagment.show()
    sys.exit(app.exec_())

