# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dbmanagment_ui.ui'
#
# Created: Fri Jul 12 11:28:14 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DBmanagment(object):
    def setupUi(self, DBmanagment):
        DBmanagment.setObjectName("DBmanagment")
        DBmanagment.resize(652, 300)
        self.beckup = QtGui.QPushButton(DBmanagment)
        self.beckup.setGeometry(QtCore.QRect(420, 60, 131, 31))
        self.beckup.setObjectName("beckup")
        self.label = QtGui.QLabel(DBmanagment)
        self.label.setGeometry(QtCore.QRect(50, 0, 291, 51))
        self.label.setObjectName("label")
        self.restore = QtGui.QPushButton(DBmanagment)
        self.restore.setGeometry(QtCore.QRect(440, 240, 93, 41))
        self.restore.setObjectName("restore")
        self.calendarWidget = QtGui.QCalendarWidget(DBmanagment)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 38, 351, 181))
        self.calendarWidget.setMinimumSize(QtCore.QSize(191, 181))
        self.calendarWidget.setStyleSheet("font: 10pt \"Andale Mono\";")
        self.calendarWidget.setObjectName("calendarWidget")
        self.upload = QtGui.QPushButton(DBmanagment)
        self.upload.setGeometry(QtCore.QRect(190, 250, 221, 31))
        self.upload.setObjectName("upload")
        self.beckup_total = QtGui.QPushButton(DBmanagment)
        self.beckup_total.setGeometry(QtCore.QRect(440, 160, 101, 31))
        self.beckup_total.setObjectName("beckup_total")
        self.label_2 = QtGui.QLabel(DBmanagment)
        self.label_2.setGeometry(QtCore.QRect(420, 20, 161, 51))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(DBmanagment)
        self.label_3.setGeometry(QtCore.QRect(360, 30, 251, 41))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(DBmanagment)
        self.label_4.setGeometry(QtCore.QRect(360, 120, 271, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(DBmanagment)
        self.label_5.setGeometry(QtCore.QRect(360, 220, 261, 17))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(DBmanagment)
        QtCore.QMetaObject.connectSlotsByName(DBmanagment)

    def retranslateUi(self, DBmanagment):
        DBmanagment.setWindowTitle(QtGui.QApplication.translate("DBmanagment", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.beckup.setText(QtGui.QApplication.translate("DBmanagment", "Backup pyarchinit", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DBmanagment", "             BeckUP e Restore DB Pyarchinit", None, QtGui.QApplication.UnicodeUTF8))
        self.restore.setText(QtGui.QApplication.translate("DBmanagment", "Ripristina", None, QtGui.QApplication.UnicodeUTF8))
        self.upload.setText(QtGui.QApplication.translate("DBmanagment", "Scegli il file da ripristinare", None, QtGui.QApplication.UnicodeUTF8))
        self.beckup_total.setText(QtGui.QApplication.translate("DBmanagment", "Backup totale", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DBmanagment", "Backup db pyarchinit (per win e linux)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DBmanagment", "Beckup totale di tutti i db (solo per linux)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("DBmanagment", "Scegli un file del beckup e ripristinalo", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DBmanagment = QtGui.QDialog()
    ui = Ui_DBmanagment()
    ui.setupUi(DBmanagment)
    DBmanagment.show()
    sys.exit(app.exec_())

