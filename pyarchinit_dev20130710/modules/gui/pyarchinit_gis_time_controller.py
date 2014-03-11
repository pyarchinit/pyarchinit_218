# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyarchinit_gis_time_controller.ui'
#
# Created: Sun Feb 23 23:14:55 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogGisTimeController(object):
    def setupUi(self, DialogGisTimeController):
        DialogGisTimeController.setObjectName(_fromUtf8("DialogGisTimeController"))
        DialogGisTimeController.resize(446, 200)
        DialogGisTimeController.setMinimumSize(QtCore.QSize(400, 156))
        DialogGisTimeController.setMaximumSize(QtCore.QSize(500, 250))
        DialogGisTimeController.setSizeIncrement(QtCore.QSize(400, 156))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/iconTimeControll.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogGisTimeController.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(DialogGisTimeController)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtGui.QTextEdit(DialogGisTimeController)
        self.textEdit.setEnabled(False)
        self.textEdit.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 7)
        self.label_2 = QtGui.QLabel(DialogGisTimeController)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 6)
        self.label = QtGui.QLabel(DialogGisTimeController)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.spinBox_cron_iniz = QtGui.QSpinBox(DialogGisTimeController)
        self.spinBox_cron_iniz.setMinimum(-4000000)
        self.spinBox_cron_iniz.setMaximum(2010)
        self.spinBox_cron_iniz.setSingleStep(250)
        self.spinBox_cron_iniz.setObjectName(_fromUtf8("spinBox_cron_iniz"))
        self.gridLayout.addWidget(self.spinBox_cron_iniz, 2, 1, 1, 1)
        self.pushButton_visualize = QtGui.QPushButton(DialogGisTimeController)
        self.pushButton_visualize.setMinimumSize(QtCore.QSize(100, 25))
        self.pushButton_visualize.setObjectName(_fromUtf8("pushButton_visualize"))
        self.gridLayout.addWidget(self.pushButton_visualize, 3, 0, 1, 7)
        self.label_4 = QtGui.QLabel(DialogGisTimeController)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 1)
        self.label_3 = QtGui.QLabel(DialogGisTimeController)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 3, 1, 1)
        self.spinBox_cron_fin = QtGui.QSpinBox(DialogGisTimeController)
        self.spinBox_cron_fin.setMinimum(-4000000)
        self.spinBox_cron_fin.setMaximum(2010)
        self.spinBox_cron_fin.setSingleStep(250)
        self.spinBox_cron_fin.setObjectName(_fromUtf8("spinBox_cron_fin"))
        self.gridLayout.addWidget(self.spinBox_cron_fin, 2, 4, 1, 1)

        self.retranslateUi(DialogGisTimeController)
        QtCore.QMetaObject.connectSlotsByName(DialogGisTimeController)

    def retranslateUi(self, DialogGisTimeController):
        DialogGisTimeController.setWindowTitle(QtGui.QApplication.translate("DialogGisTimeController", "pyArchInit Gestione Scavi - Time Controller", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("DialogGisTimeController", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Per funzionare il sistema di ricerca per cronologie assolute richiede la creazione dei periodi di scavo nella scheda Periodizzazione. La cronologia assoluta qui utilizzata viene riferita ai termini &quot;avanti Cristo&quot; e &quot;dopo Cristo&quot;. Per settare valori avanti Cristo utilizzare il segno &quot;-&quot; davanti all\'anno (ex: 268 a.C. = -268). Per settare valori dopo Cristo utilizzare non e\' necessario utilizzare alcun segno (1400 d.C. = 1440).</span></p>\n"
"<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt; font-weight:600;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DialogGisTimeController", "Visualizza l\'intervallo di tempo compreso tra l\'anno:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogGisTimeController", "Cronologia iniziale", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_visualize.setToolTip(QtGui.QApplication.translate("DialogGisTimeController", "Prev rec", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_visualize.setText(QtGui.QApplication.translate("DialogGisTimeController", "Visualizza", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("DialogGisTimeController", "e l\'anno", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("DialogGisTimeController", "Cronologia finale", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
