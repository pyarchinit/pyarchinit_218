# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyarchinit_pdf_exp_ui.ui'
#
# Created: Wed Jul 24 15:03:21 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog_pdf_exp(object):
    def setupUi(self, Dialog_pdf_exp):
        Dialog_pdf_exp.setObjectName(_fromUtf8("Dialog_pdf_exp"))
        Dialog_pdf_exp.setWindowModality(QtCore.Qt.NonModal)
        Dialog_pdf_exp.setEnabled(True)
        Dialog_pdf_exp.resize(476, 279)
        Dialog_pdf_exp.setMinimumSize(QtCore.QSize(450, 279))
        Dialog_pdf_exp.setMaximumSize(QtCore.QSize(1000, 1000))
        Dialog_pdf_exp.setCursor(QtCore.Qt.PointingHandCursor)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/directoryExp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog_pdf_exp.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog_pdf_exp)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog_pdf_exp)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.comboBox_sito = QtGui.QComboBox(self.tab)
        self.comboBox_sito.setEnabled(True)
        self.comboBox_sito.setMouseTracking(False)
        self.comboBox_sito.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.comboBox_sito.setAcceptDrops(False)
        self.comboBox_sito.setEditable(True)
        self.comboBox_sito.setDuplicatesEnabled(False)
        self.comboBox_sito.setFrame(True)
        self.comboBox_sito.setObjectName(_fromUtf8("comboBox_sito"))
        self.comboBox_sito.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.comboBox_sito)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 5)
        self.checkBox_US = QtGui.QCheckBox(self.tab)
        self.checkBox_US.setObjectName(_fromUtf8("checkBox_US"))
        self.gridLayout.addWidget(self.checkBox_US, 1, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(250, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 2)
        self.checkBox_periodo = QtGui.QCheckBox(self.tab)
        self.checkBox_periodo.setObjectName(_fromUtf8("checkBox_periodo"))
        self.gridLayout.addWidget(self.checkBox_periodo, 2, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(448, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 3)
        self.checkBox_struttura = QtGui.QCheckBox(self.tab)
        self.checkBox_struttura.setObjectName(_fromUtf8("checkBox_struttura"))
        self.gridLayout.addWidget(self.checkBox_struttura, 3, 0, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(307, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 2, 1, 3)
        self.checkBox_reperti = QtGui.QCheckBox(self.tab)
        self.checkBox_reperti.setObjectName(_fromUtf8("checkBox_reperti"))
        self.gridLayout.addWidget(self.checkBox_reperti, 4, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(178, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 4, 2, 1, 2)
        self.pushButton_exp_pdf = QtGui.QPushButton(self.tab)
        self.pushButton_exp_pdf.setObjectName(_fromUtf8("pushButton_exp_pdf"))
        self.gridLayout.addWidget(self.pushButton_exp_pdf, 5, 4, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog_pdf_exp)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog_pdf_exp)

    def retranslateUi(self, Dialog_pdf_exp):
        Dialog_pdf_exp.setWindowTitle(QtGui.QApplication.translate("Dialog_pdf_exp", "Impostazioni del sistema", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog_pdf_exp", "Seleziona un sito da esportare...", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_sito.setItemText(0, QtGui.QApplication.translate("Dialog_pdf_exp", "Seleziona un valore...", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_US.setText(QtGui.QApplication.translate("Dialog_pdf_exp", "Unità Stratigrafiche", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_periodo.setText(QtGui.QApplication.translate("Dialog_pdf_exp", "Periodo", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_struttura.setText(QtGui.QApplication.translate("Dialog_pdf_exp", "Struttura", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_reperti.setText(QtGui.QApplication.translate("Dialog_pdf_exp", "Reperti", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_exp_pdf.setText(QtGui.QApplication.translate("Dialog_pdf_exp", "Esporta PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog_pdf_exp", "Parametri di esportazione", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
