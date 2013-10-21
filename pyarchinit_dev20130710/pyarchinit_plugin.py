#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
        pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
        					 stored in Postgres
                             -------------------
    begin                : 2007-12-01
    copyright            : (C) 2008 by Luca Mandolesi
    email                : mandoluca at gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import sys
import os

filepath = os.path.dirname(__file__)

gui_path = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'gui'))
gis_path = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'gis'))
db_path  = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'db'))
utility  = ('%s%s') % (filepath, os.path.join(os.sep, 'modules', 'utility'))

sys.path.insert(0,gui_path)
sys.path.insert(1,gis_path)
sys.path.insert(2,db_path)
sys.path.insert(3,utility)
sys.path.insert(4,filepath)

from PyQt4.QtCore import *
from PyQt4.QtGui import *
try:
	from qgis.core import *
	from qgis.gui import *
except:
	pass

from pyarchinit_folder_installation import *
fi = pyarchinit_Folder_installation()
fi.install_dir()

# Import the code for the dialog
from pyarchinit_US_mainapp import pyarchinit_US
from pyarchinit_Site_mainapp import pyarchinit_Site
from pyarchinit_Periodizzazione_mainapp import pyarchinit_Periodizzazione
from pyarchinit_Struttura_mainapp import pyarchinit_Struttura
from pyarchinit_Inv_Materiali_mainapp import pyarchinit_Inventario_reperti
from pyarchinit_Upd_mainapp import pyarchinit_Upd_Values
from pyarchinitConfigDialog import pyArchInitDialog_Config
from pyarchinitInfoDialog import pyArchInitDialog_Info
from pyarchinit_Gis_Time_controller import pyarchinit_Gis_Time_Controller
from pyarchinit_image_viewer_main import Main
from pyarchinit_Schedaind_mainapp import pyarchinit_Schedaind
from pyarchinit_Detsesso_mainapp import pyarchinit_Detsesso
from pyarchinit_Deteta_mainapp import pyarchinit_Deteta
from pyarchinit_Tafonomia_mainapp import pyarchinit_Tafonomia
from pyarchinit_Archeozoology_mainapp import pyarchinit_Archeozoology
from pyarchinit_UT_mainapp import pyarchinit_UT
from pyarchinit_images_directory_export_mainapp import pyarchinit_Images_directory_export
from pyarchinit_images_comparision_main import Comparision
from dbmanagment import pyarchinit_dbmanagment
from pyarchinitplugindialog import PyarchinitPluginDialog
from pyarchinit_pdf_export_mainapp import pyarchinit_pdf_export

class PyArchInitPlugin:
	def __init__(self, iface):
		self.iface = iface
		
		userPluginPath = QFileInfo( QgsApplication.qgisUserDbFilePath() ).path() + "/python/plugins/pyarchinit"
		systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/pyarchinit"

##		overrideLocale = QSettings().value( "locale/overrideFlag", QVariant( False ) ).toBool()
##		if not overrideLocale:
##			localeFullName = QLocale.system().name()
##		else:
##			localeFullName = QSettings().value( "locale/userLocale", QVariant( "" ) ).toString()
##
##		if QFileInfo( userPluginPath ).exists():
##			translationPath = userPluginPath + "/i18n/pyarchinit_plugin_" + localeFullName + ".qm"
##		else:
##			translationPath = systemPluginPath + "/i18n/pyarchinit_plugin_" + localeFullName + ".qm"
##
##		self.localePath = translationPath
##		if QFileInfo( self.localePath ).exists():
##			self.translator = QTranslator()
##			self.translator.load( self.localePath )
##			QCoreApplication.installTranslator( self.translator )


	def initGui(self):
		self.action = QAction(QIcon(":/plugins/pyarchinit/icons/pai_us.png"), "pyArchInit Main Panel", self.iface.mainWindow())
		QObject.connect(self.action, SIGNAL("triggered()"), self.showHideDockWidget)
		
		# dock widget
		self.dockWidget = PyarchinitPluginDialog(self.iface)
		self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
		
		icon_site = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconSite.png'))
		self.actionSite = QAction(QIcon(icon_site), "Scheda di Sito", self.iface.mainWindow())
		self.actionSite.setWhatsThis("Scheda di Sito")
		QObject.connect(self.actionSite, SIGNAL("triggered()"), self.runSite)

		icon_per = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconPer.png'))
		self.actionPer = QAction(QIcon(icon_per), "Scheda di Periodizzazione", self.iface.mainWindow())
		self.actionPer.setWhatsThis("Scheda di Periodizzazione")
		QObject.connect(self.actionPer, SIGNAL("triggered()"), self.runPer)

		icon_Struttura = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconStrutt.png'))
		self.actionStruttura = QAction(QIcon(icon_Struttura), "Scheda struttura", self.iface.mainWindow())
		QObject.connect(self.actionStruttura, SIGNAL("triggered()"), self.runStruttura)

		icon_US = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconSus.png'))
		self.actionUS = QAction(QIcon((icon_US)), u"Scheda di Unità Stratigrafica - US", self.iface.mainWindow())
		self.actionUS.setWhatsThis(u"Scheda di Unità Stratigrafica - US")
		QObject.connect(self.actionUS, SIGNAL("triggered()"), self.runUS)

		icon_Finds = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconFinds.png'))
		self.actionInr = QAction(QIcon(icon_Finds), "Scheda Inventario Reperti", self.iface.mainWindow())
		self.actionInr.setWhatsThis("Scheda Inventario Reperti")
		QObject.connect(self.actionInr, SIGNAL("triggered()"), self.runInr)

		icon_Upd = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconUpd.png'))
		self.actionUpd = QAction(QIcon(icon_Upd), "Aggiornamento Valori", self.iface.mainWindow())
		self.actionUpd.setWhatsThis("Aggiornamento Valori")
		QObject.connect(self.actionUpd, SIGNAL("triggered()"), self.runUpd)
		
		icon_Con = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconConn.png'))
		self.actionConf = QAction(QIcon(icon_Con), "Configurazione parametri di connessione al Database", self.iface.mainWindow())
		self.actionConf.setWhatsThis("Configurazione parametri di connessione al Database")
		QObject.connect(self.actionConf, SIGNAL("triggered()"), self.runConf)

		icon_Info = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconInfo.png'))
		self.actionInfo = QAction(QIcon(icon_Info), "pyArchInit Info", self.iface.mainWindow())
		self.actionInfo.setWhatsThis("pyArchInit Info")
		QObject.connect(self.actionInfo, SIGNAL("triggered()"), self.runInfo)

		icon_GisTimeController = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconTimeControll.png'))
		self.actionGisTimeController = QAction(QIcon(icon_GisTimeController), "pyArchInit Gis Time Controller", self.iface.mainWindow())
		self.actionGisTimeController.setWhatsThis("pyArchInit Gis Time Controller")
		QObject.connect(self.actionGisTimeController, SIGNAL("triggered()"), self.runGisTimeController)

		icon_imageViewer = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','photo.png'))
		self.actionimageViewer = QAction(QIcon(icon_imageViewer), "pyArchInit Image Viewer", self.iface.mainWindow())
		self.actionimageViewer.setWhatsThis("pyArchInit Image Viewer")
		QObject.connect(self.actionimageViewer, SIGNAL("triggered()"), self.runImageViewer)

		icon_Schedaind = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconIND.png'))
		self.actionSchedaind = QAction(QIcon(icon_Schedaind), "pyArchInit Scheda Individuo", self.iface.mainWindow())
		self.actionSchedaind.setWhatsThis("pyArchInit Scheda Individuo")
		QObject.connect(self.actionSchedaind, SIGNAL("triggered()"), self.runSchedaind)

		icon_Detsesso = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconSESSO.png'))
		self.actionDetsesso = QAction(QIcon(icon_Detsesso), "pyArchInit Scheda Determinazione del sesso", self.iface.mainWindow())
		self.actionDetsesso.setWhatsThis("pyArchInit Scheda Determinazione del sesso")
		QObject.connect(self.actionDetsesso, SIGNAL("triggered()"), self.runDetsesso)

		icon_Deteta = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconETA.png'))
		self.actionDeteta = QAction(QIcon(icon_Deteta), "pyArchInit Scheda Determinazione dell'età", self.iface.mainWindow())
		self.actionSchedaind.setWhatsThis("pyArchInit Scheda Determinazione dell'età")
		QObject.connect(self.actionDeteta, SIGNAL("triggered()"), self.runDeteta)

		icon_Tafonomia = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconGrave.png'))
		self.actionTafonomia = QAction(QIcon(icon_Tafonomia), "pyArchInit Scheda Tafonomica", self.iface.mainWindow())
		self.actionTafonomia.setWhatsThis("pyArchInit Scheda Tafonomica")
		QObject.connect(self.actionTafonomia, SIGNAL("triggered()"), self.runTafonomia)

		icon_Archeozoology = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconMegacero.png'))
		self.actionArcheozoology = QAction(QIcon(icon_Archeozoology), "pyArchInit Scheda Archeozoologia", self.iface.mainWindow())
		self.actionArcheozoology.setWhatsThis("pyArchInit Scheda Archeozoologia")
		QObject.connect(self.actionArcheozoology, SIGNAL("triggered()"), self.runArcheozoology)

		icon_UT = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','iconUT.png'))
		self.actionUT = QAction(QIcon(icon_UT), "pyArchInit UT", self.iface.mainWindow())
		self.actionUT.setWhatsThis("pyArchInit UT")
		QObject.connect(self.actionUT, SIGNAL("triggered()"), self.runUT)

		icon_Directory_export = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','directoryExp.png'))
		self.actionImages_Directory_export = QAction(QIcon(icon_Directory_export), "pyArchInit Images Directories Export", self.iface.mainWindow())
		self.actionImages_Directory_export.setWhatsThis("pyArchInit Images Directories Export")
		QObject.connect(self.actionImages_Directory_export, SIGNAL("triggered()"),self.runImages_directory_export)
		
		icon_Comparision = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','comparision.png'))
		self.actionComparision = QAction(QIcon(icon_Comparision), "pyArchInit Images Comparision", self.iface.mainWindow())
		self.actionComparision.setWhatsThis("pyArchInit Images Comparision")
		QObject.connect(self.actionComparision, SIGNAL("triggered()"),self.runComparision)
		
		icon_Dbmanagment = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','beckup.jpg'))
		self.actionDbmanagment = QAction(QIcon(icon_Dbmanagment), "pyArchInit Scheda gestione db", self.iface.mainWindow())
		self.actionDbmanagment.setWhatsThis("pyArchInit Scheda gestione db")
		QObject.connect(self.actionDbmanagment, SIGNAL("triggered()"), self.runDbmanagment)

		icon_pdf_exp = ('%s%s') % (filepath, os.path.join(os.sep, 'icons','pdf-icon.jpg'))
		self.actionpdfExp = QAction(QIcon(icon_pdf_exp), "pyArchInit Sistema di esportazione PDF", self.iface.mainWindow())
		self.actionpdfExp.setWhatsThis("pyArchInit Sistema di esportazione PDF")
		QObject.connect(self.actionpdfExp, SIGNAL("triggered()"), self.runPdfexp)
		#MENU
		self.menu=QMenu("pyArchInit")

		#self.pyarchinitSite = pyarchinit_Site(self.iface)

		self.menu.addActions([self.actionSite, self.actionUS, self.actionInr])
		self.menu.addSeparator()
		self.menu.addActions([self.actionPer, self.actionStruttura])
		self.menu.addSeparator()
		self.menu.addActions([self.actionTafonomia, self.actionSchedaind,self.actionDetsesso,self.actionDeteta])
		self.menu.addSeparator()
		self.menu.addActions([self.actionArcheozoology])
		self.menu.addSeparator()
		self.menu.addActions([self.actionUT])
		self.menu.addSeparator()
		self.menu.addActions([self.actionUpd, self.actionGisTimeController])
		self.menu.addSeparator()
		self.menu.addActions([self.actionimageViewer, self.actionImages_Directory_export, self.actionpdfExp, self.actionComparision])
		self.menu.addSeparator()
		self.menu.addActions([self.actionConf])
		self.menu.addSeparator()
		self.menu.addActions([self.actionInfo])
		self.menu.addSeparator()
		self.menu.addActions([self.actionDbmanagment])


		menuBar = self.iface.mainWindow().menuBar()
		menuBar.addMenu(self.menu)

		#TOOLBAR
		self.toolBar = self.iface.addToolBar("pyArchInit - Archaeological GIS Tools")
		self.toolBar.addAction(self.actionSite)
		self.toolBar.addAction(self.actionPer)
		self.toolBar.addAction(self.actionStruttura)
		self.toolBar.addAction(self.actionUS)
		self.toolBar.addAction(self.actionInr)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionTafonomia)
		self.toolBar.addAction(self.actionSchedaind)
		self.toolBar.addAction(self.actionDetsesso)
		self.toolBar.addAction(self.actionDeteta)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionArcheozoology)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionUT)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionGisTimeController)
		self.toolBar.addAction(self.actionUpd)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionimageViewer)
		self.toolBar.addAction(self.actionImages_Directory_export)
		self.toolBar.addAction(self.actionpdfExp)
		self.toolBar.addAction(self.actionComparision)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionConf)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionInfo)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.actionDbmanagment)
		
		

		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionSite)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionPer)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionStruttura)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionUS)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionInr)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionTafonomia)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionSchedaind)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionDetsesso)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionDeteta)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionArcheozoology)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionUT)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionGisTimeController)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionUpd)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionimageViewer)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionComparision)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionImages_Directory_export)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionpdfExp)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionConf)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionInfo)
		self.iface.addPluginToMenu("&pyArchInit - Archaeological GIS Tools", self.actionDbmanagment)


	def runSite(self):
		pluginGui = pyarchinit_Site(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save
		
	def runPer(self):
		pluginGui = pyarchinit_Periodizzazione(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runStruttura(self):
		pluginGui = pyarchinit_Struttura(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runUS(self):
		pluginGui = pyarchinit_US(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runInr(self):
		pluginGui = pyarchinit_Inventario_reperti(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runGisTimeController(self):
		pluginGui = pyarchinit_Gis_Time_Controller(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runUpd(self):
		pluginGui = pyarchinit_Upd_Values(self.iface)
		pluginGui.show()
		self.pluginGui = pluginGui # save

	def runConf(self):
		pluginConfGui = pyArchInitDialog_Config()
		pluginConfGui.show()
		self.pluginGui = pluginConfGui # save

	def runInfo(self):
		pluginInfoGui = pyArchInitDialog_Info()
		pluginInfoGui.show()
		self.pluginGui = pluginInfoGui # save

	def runImageViewer(self):
		pluginImageView = Main()
		pluginImageView.show()
		self.pluginGui = pluginImageView # save

	def runTafonomia(self):
		pluginTafonomia = pyarchinit_Tafonomia(self.iface)
		pluginTafonomia.show()
		self.pluginGui = pluginTafonomia # save

	def runSchedaind(self):
		pluginIndividui = pyarchinit_Schedaind(self.iface)
		pluginIndividui.show()
		self.pluginGui = pluginIndividui # save

	def runDetsesso(self):
		pluginSesso = pyarchinit_Detsesso(self.iface)
		pluginSesso.show()
		self.pluginGui = pluginSesso # save

	def runDeteta(self):
		pluginEta = pyarchinit_Deteta(self.iface)
		pluginEta.show()
		self.pluginGui = pluginEta # save

	def runArcheozoology(self):
		pluginArchezoology = pyarchinit_Archeozoology(self.iface)
		pluginArchezoology.show()
		self.pluginGui = pluginArchezoology # save

	def runUT(self):
		pluginUT = pyarchinit_UT(self.iface)
		pluginUT.show()
		self.pluginGui = pluginUT # save

	def runImages_directory_export(self):
		pluginImage_directory_export = pyarchinit_Images_directory_export()
		pluginImage_directory_export.show()
		self.pluginGui = pluginImage_directory_export # save

	def runComparision(self):
		pluginComparision = Comparision()
		pluginComparision.show()
		self.pluginGui = pluginComparision # save

	def runDbmanagment(self):
		pluginDbmanagment = pyarchinit_dbmanagment(self)
		pluginDbmanagment.show()
		self.pluginGui = pluginDbmanagment # save

	def runPdfexp(self):
		pluginPdfexp = pyarchinit_pdf_export()
		pluginPdfexp.show()
		self.pluginGui =pluginPdfexp # save

	def unload(self):
		# Remove the plugin
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionSite)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionPer)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionStruttura)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionUS)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionInr)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionSchedaind)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionDetsesso)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionDeteta)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionTafonomia)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionArcheozoology)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionUT)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionUpd)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionimageViewer)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionImages_Directory_export)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionpdfExp)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionComparision)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionConf)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionGisTimeController)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionInfo)
		self.iface.removePluginMenu("&pyArchInit - Archaeological GIS Tools",self.actionDbmanagment)

		self.iface.removeToolBarIcon(self.actionSite)
		self.iface.removeToolBarIcon(self.actionPer)
		self.iface.removeToolBarIcon(self.actionStruttura)
		self.iface.removeToolBarIcon(self.actionUS)
		self.iface.removeToolBarIcon(self.actionInr)
		self.iface.removeToolBarIcon(self.actionTafonomia)
		self.iface.removeToolBarIcon(self.actionSchedaind)
		self.iface.removeToolBarIcon(self.actionDetsesso)
		self.iface.removeToolBarIcon(self.actionDeteta)
		self.iface.removeToolBarIcon(self.actionArcheozoology)
		self.iface.removeToolBarIcon(self.actionUT)
		self.iface.removeToolBarIcon(self.actionUpd)
		self.iface.removeToolBarIcon(self.actionimageViewer)
		self.iface.removeToolBarIcon(self.actionImages_Directory_export)
		self.iface.removeToolBarIcon(self.actionpdfExp)
		self.iface.removeToolBarIcon(self.actionComparision)
		self.iface.removeToolBarIcon(self.actionGisTimeController)
		self.iface.removeToolBarIcon(self.actionConf)
		self.iface.removeToolBarIcon(self.actionInfo)
		self.iface.removeToolBarIcon(self.actionDbmanagment)

		# remove tool bar
		del self.toolBar

	def showHideDockWidget(self):
		if self.dockWidget.isVisible():
			self.dockWidget.hide()
		else:
			self.dockWidget.show()
