#! /usr/bin/env python
#-*- coding: utf-8 -*-
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
import sys, os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQt4.QtGui
try:
	from qgis.core import *
	from qgis.gui import *
except:
	pass

from  pyarchinit_db_manager import *

from datetime import date
from psycopg2 import *

#--import pyArchInit modules--#
from  pyarchinit_Archeozoology_ui import Ui_DialogArcheoZoology
from  pyarchinit_Archeozoology_ui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *

from  pyarchinit_pyqgis import Pyarchinit_pyqgis
from  sortpanelmain import SortPanelMain

class pyarchinit_Archeozoology(QDialog, Ui_DialogArcheoZoology):
	MSG_BOX_TITLE = "PyArchInit - pyarchinit_version 0.4 - Scheda Archeozoologia Quantificazioni"
	DATA_LIST = []
	DATA_LIST_REC_CORR = []
	DATA_LIST_REC_TEMP = []
	REC_CORR = 0
	REC_TOT = 0
	STATUS_ITEMS = {"b": "Usa", "f": "Trova", "n": "Nuovo Record"}
	BROWSE_STATUS = "b"
	SORT_MODE = 'asc'
	SORTED_ITEMS = {"n": "Non ordinati", "o": "Ordinati"}
	SORT_STATUS = "n"
	UTILITY = Utility()
	DB_MANAGER = ""
	TABLE_NAME = 'archeozoology_table'
	MAPPER_TABLE_CLASS = "ARCHEOZOOLOGY"
	NOME_SCHEDA = "Scheda Archeozoologia"
	ID_TABLE = "id_archzoo"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE, 
	'Sito':'sito',
	'Area':'area',
	'US':'us',
	'Quadrato':'quadrato',
	'Coordinata x':'coord_x',
	'Coordinata y':'coord_y',
	'Coordinata z':'coord_z',
	'Bos/Bison':'bos_bison',
	'Calcinati':'calcinati',
	'Camoscio':'camoscio',
	'Capriolo':'capriolo',
	'Cervo':'cervo',
	'Combusto':'combusto',
	'Coni':'coni',
	'Pdi':'pdi',
	'Stambecco':'stambecco',
	'Strie':'strie',
	'Canidi':'canidi',
	'Ursidi':'ursidi',
	'Megacero':'megacero'
	}
	SORT_ITEMS = [
				ID_TABLE,
				'Sito',
				'Area',
				'US',
				'Quadrato',
				'Coordinata x',
				'Coordinata y',
				'Coordinata z',
				'Bos/Bison',
				'Calcinati',
				'Camoscio',
				'Capriolo',
				'Cervo',
				'Combusto',
				'Coni',
				'Pdi',
				'Stambecco',
				'Strie',
				'Canidi',
				'Ursidi',
				'Megacero'
				]

	TABLE_FIELDS = [
					'sito',
					'area',
					'us',
					'quadrato',
					'coord_x',
					'coord_y',
					'coord_z',
					'bos_bison',
					'calcinati',
					'camoscio',
					'capriolo',
					'cervo',
					'combusto',
					'coni',
					'pdi',
					'stambecco',
					'strie',
					'canidi',
					'ursidi',
					'megacero'
				]

	def __init__(self, iface):
		self.iface = iface
		self.pyQGIS = Pyarchinit_pyqgis(self.iface)
		QDialog.__init__(self)
		self.setupUi(self)
		self.currentLayerId = None
		try:
			self.on_pushButton_connect_pressed()
		except:
			pass
	
	def enable_button(self, n):
		self.pushButton_connect.setEnabled(n)

		self.pushButton_new_rec.setEnabled(n)

		self.pushButton_view_all.setEnabled(n)

		self.pushButton_first_rec.setEnabled(n)

		self.pushButton_last_rec.setEnabled(n)

		self.pushButton_prev_rec.setEnabled(n)

		self.pushButton_next_rec.setEnabled(n)

		self.pushButton_delete.setEnabled(n)

		self.pushButton_new_search.setEnabled(n)

		self.pushButton_search_go.setEnabled(n)
		
		self.pushButton_sort.setEnabled(n)

	def enable_button_search(self, n):
		self.pushButton_connect.setEnabled(n)

		self.pushButton_new_rec.setEnabled(n)

		self.pushButton_view_all.setEnabled(n)

		self.pushButton_first_rec.setEnabled(n)

		self.pushButton_last_rec.setEnabled(n)

		self.pushButton_prev_rec.setEnabled(n)

		self.pushButton_next_rec.setEnabled(n)

		self.pushButton_delete.setEnabled(n)

		self.pushButton_save.setEnabled(n)

		self.pushButton_sort.setEnabled(n)

	def on_pushButton_connect_pressed(self):
		from pyarchinit_conn_strings import *
		conn = Connection()
		conn_str = conn.conn_str()
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
			self.charge_records() #charge records from DB
			#check if DB is empty
			if bool(self.DATA_LIST) == True:
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.BROWSE_STATUS = 'b'
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
				self.charge_list()
				self.fill_fields()
			else:
				QMessageBox.warning(self, "BENVENUTO", "Benvenuto in pyArchInit" + self.NOME_SCHEDA + ". Il database e' vuoto. Premi 'Ok' e buon lavoro!",  QMessageBox.Ok)
				self.charge_list()
				self.on_pushButton_new_rec_pressed()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert 1", "La connessione e' fallita <br><br> Tabella non presente. E' NECESSARIO RIAVVIARE QGIS" + str(e) ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert 2", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)


	def charge_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))

		try:
			sito_vl.remove('')
		except:
			pass
		self.comboBox_sito.clear()
		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)


	#buttons functions
	def on_pushButton_sort_pressed(self):
		dlg = SortPanelMain(self)
		dlg.insertItems(self.SORT_ITEMS)
		dlg.exec_()

		items,order_type = dlg.ITEMS, dlg.TYPE_ORDER

		self.SORT_ITEMS_CONVERTED = []
		for i in items:
			self.SORT_ITEMS_CONVERTED.append(self.CONVERSION_DICT[unicode(i)])

		self.SORT_MODE = order_type
		self.empty_fields()

		id_list = []
		for i in self.DATA_LIST:
			id_list.append(eval("i." + self.ID_TABLE))
		self.DATA_LIST = []

		temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

		for i in temp_data_list:
			self.DATA_LIST.append(i)
		self.BROWSE_STATUS = "b"
		self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR

		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
		self.SORT_STATUS = "o"
		self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.fill_fields()

	def on_pushButton_new_rec_pressed(self):
		#set the GUI for a new record
		if self.BROWSE_STATUS != "n":
			self.BROWSE_STATUS = "n"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()
			self.label_sort.setText(self.SORTED_ITEMS["n"])

			self.setComboBoxEnable(["self.comboBox_sito"],"True")

			self.set_rec_counter('', '')
			self.enable_button(0)

	def on_pushButton_save_pressed(self):
		#save record
		if self.BROWSE_STATUS == "b":
			if self.records_equal_check() == 1:
				self.update_if(QMessageBox.warning(self,'ATTENZIONE',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.enable_button(1)
			else:
				QMessageBox.warning(self, "ATTENZIONE", "Non è stata realizzata alcuna modifica.",  QMessageBox.Ok)
		else:
			if self.data_error_check() == 0:
				test_insert = self.insert_new_rec()
				if test_insert == 1:
					self.empty_fields()
					self.label_sort.setText(self.SORTED_ITEMS["n"])
					self.charge_list()
					self.charge_records()
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
					self.fill_fields(self.REC_CORR)
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.enable_button(1)
				else:
					pass

	def data_error_check(self):
		test = 0
		EC = Error_check()

		if EC.data_is_empty(str(self.comboBox_sito.currentText())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Sito. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1
		elif EC.data_is_empty(str(self.lineEdit_quadrato.text())) == 0:
			QMessageBox.warning(self, "ATTENZIONE", "Campo Quadrato. \n Il campo non deve essere vuoto",  QMessageBox.Ok)
			test = 1

		return test

	def insert_new_rec(self):
		if self.lineEdit_us.text() == "":
			us = None
		else:
			us = int(self.lineEdit_us.text())

		if self.lineEdit_coord_x.text() == "":
			coord_x = None
		else:
			coord_x = float(self.lineEdit_coord_x.text())

		#f = open("test_coord.txt", "w")
		#f.write(str(coord_x))
		#f.close()

		if self.lineEdit_coord_y.text() == "":
			coord_y = None
		else:
			coord_y = float(self.lineEdit_coord_y.text())

		if self.lineEdit_coord_z.text() == "":
			coord_z = None
		else:
			coord_z = float(self.lineEdit_coord_z.text())

		if self.lineEdit_bos_bison.text() == "":
			bos_bison = None
		else:
			bos_bison = int(self.lineEdit_bos_bison.text())

		if self.lineEdit_calcinati.text() == "":
			calcinati = None
		else:
			calcinati = int(self.lineEdit_calcinati.text())

		if self.lineEdit_camoscio.text() == "":
			camoscio = None
		else:
			camoscio = int(self.lineEdit_camoscio.text())

		if self.lineEdit_capriolo.text() == "":
			capriolo = None
		else:
			capriolo = int(self.lineEdit_capriolo.text())

		if self.lineEdit_cervi.text() == "":
			cervo = None
		else:
			cervo = int(self.lineEdit_cervi.text())

		if self.lineEdit_combuste.text() == "":
			combusto = None
		else:
			combusto = int(self.lineEdit_combuste.text())

		if self.lineEdit_Coni.text() == "":
			coni = None
		else:
			coni = int(self.lineEdit_Coni.text())

		if self.lineEdit_pdi.text() == "":
			pdi = None
		else:
			pdi = int(self.lineEdit_pdi.text())

		if self.lineEdit_stambecco.text() == "":
			stambecco = None
		else:
			stambecco = int(self.lineEdit_stambecco.text())

		if self.lineEdit_strie.text() == "":
			strie = None
		else:
			strie = int(self.lineEdit_strie.text())


		if self.lineEdit_canidi.text() == "":
			canidi = None
		else:
			canidi = int(self.lineEdit_canidi.text())

		if self.lineEdit_ursidi.text() == "":
			ursidi = None
		else:
			ursidi = int(self.lineEdit_ursidi.text())

		if self.lineEdit_megacero.text() == "":
			megacero = None
		else:
			megacero = int(self.lineEdit_megacero.text())

			
		try:
			data = self.DB_MANAGER.insert_values_archeozoology(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1,
			str(self.comboBox_sito.currentText()), 					#1 - Sito
			str(self.lineEdit_area.text()),
			us,
			str(self.lineEdit_quadrato.text()),
			coord_x,
			coord_y,
			coord_z,
			bos_bison,
			calcinati,
			camoscio,
			capriolo,
			cervo,
			combusto,
			coni,
			pdi,
			stambecco,
			strie,
			canidi,
			ursidi,
			megacero)
			
			try:
				self.DB_MANAGER.insert_data_session(data)
				return 1
			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.ID_TABLE + " gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "Attenzione 1 ! \n"+ str(msg),  QMessageBox.Ok)
				return 0
		except Exception, e:
			QMessageBox.warning(self, "Errore", "Attenzione 2 ! \n"+str(e),  QMessageBox.Ok)
			return 0

	def on_pushButton_view_all_pressed(self):
		self.empty_fields()
		self.charge_records()
		self.fill_fields()
		self.BROWSE_STATUS = "b"
		self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
		if type(self.REC_CORR) == "<type 'str'>":
			corr = 0
		else:
			corr = self.REC_CORR
		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
		self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
		self.label_sort.setText(self.SORTED_ITEMS["n"])

	#records surf functions
	def on_pushButton_first_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		try:
			self.empty_fields()
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
			self.fill_fields(0)
			self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_last_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		try:
			self.empty_fields()
			self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
			self.fill_fields(self.REC_CORR)
			self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
		except Exception, e:
			QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_prev_rec_pressed(self):
		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))

		self.REC_CORR = self.REC_CORR-1
		if self.REC_CORR == -1:
			self.REC_CORR = 0
			QMessageBox.warning(self, "Errore", "Sei al primo record!",  QMessageBox.Ok)
		else:
			try:
				self.empty_fields()
				self.fill_fields(self.REC_CORR)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
			except Exception, e:
				QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_next_rec_pressed(self):

		if self.records_equal_check() == 1:
			self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))

		self.REC_CORR = self.REC_CORR+1
		if self.REC_CORR >= self.REC_TOT:
			self.REC_CORR = self.REC_CORR-1
			QMessageBox.warning(self, "Errore", "Sei all'ultimo record!",  QMessageBox.Ok)
		else:
			try:
				self.empty_fields()
				self.fill_fields(self.REC_CORR)
				self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
			except Exception, e:
				QMessageBox.warning(self, "Errore", str(e),  QMessageBox.Ok)

	def on_pushButton_delete_pressed(self):
		msg = QMessageBox.warning(self,"Attenzione!!!","Vuoi veramente eliminare il record? \n L'azione e' irreversibile", QMessageBox.Cancel,1)
		if msg != 1:
			QMessageBox.warning(self,"Messagio!!!","Azione Annullata!")
		else:
			try:
				id_to_delete = eval("self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE)
				self.DB_MANAGER.delete_one_record(self.TABLE_NAME, self.ID_TABLE, id_to_delete)
				self.charge_records() #charge records from DB
				QMessageBox.warning(self,"Messaggio!!!","Record eliminato!")
				self.charge_list()
			except:
				QMessageBox.warning(self, "Attenzione", "Il database e' vuoto!",  QMessageBox.Ok)

			if bool(self.DATA_LIST) == False:

				self.DATA_LIST = []
				self.DATA_LIST_REC_CORR = []
				self.DATA_LIST_REC_TEMP = []
				self.REC_CORR = 0
				self.REC_TOT = 0
				self.empty_fields()
				self.set_rec_counter(0, 0)
			#check if DB is empty
			if bool(self.DATA_LIST) == True:
				self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
				self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
				self.fill_fields()
				self.BROWSE_STATUS = "b"
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.label_sort.setText(self.SORTED_ITEMS["n"])

	def on_pushButton_new_search_pressed(self):
		if self.records_equal_check() == 1 and self.BROWSE_STATUS == "b":
			msg = self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		#else:
		self.enable_button_search(0)

		#set the GUI for a new search

		if self.BROWSE_STATUS != "f":
			self.BROWSE_STATUS = "f"
			
			###
			self.setComboBoxEnable(["self.comboBox_sito"],"True")

			###

			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.set_rec_counter('','')
			self.label_sort.setText(self.SORTED_ITEMS["n"])
			self.charge_list()
			self.empty_fields()


	def on_pushButton_search_go_pressed(self):
		if self.BROWSE_STATUS != "f":
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:
			if self.lineEdit_us.text() == "":
				us = ''
			else:
				us = int(self.lineEdit_us.text())

			if self.lineEdit_coord_x.text() == "":
				coord_x = ''
			else:
				coord_x = int(self.lineEdit_coord_x.text())

			if self.lineEdit_coord_y.text() == "":
				coord_y = ''
			else:
				coord_y = int(self.lineEdit_coord_y.text())

			if self.lineEdit_coord_z.text() == "":
				coord_z = ''
			else:
				coord_z = int(self.lineEdit_coord_z.text())

			if self.lineEdit_bos_bison.text() == "":
				bos_bison = ''
			else:
				bos_bison = int(self.lineEdit_bos_bison.text())

			if self.lineEdit_calcinati.text() == "":
				calcinati = ''
			else:
				calcinati = int(self.lineEdit_calcinati.text())

			if self.lineEdit_camoscio.text() == "":
				camoscio = ''
			else:
				camoscio = int(self.lineEdit_camoscio.text())

			if self.lineEdit_capriolo.text() == "":
				capriolo = ''
			else:
				capriolo = int(self.lineEdit_capriolo.text())

			if self.lineEdit_cervi.text() == "":
				cervo = ''
			else:
				cervo = int(self.lineEdit_cervi.text())

			if self.lineEdit_combuste.text() == "":
				combusto = ''
			else:
				combusto = int(self.lineEdit_combuste.text())

			if self.lineEdit_Coni.text() == "":
				coni = ''
			else:
				coni = int(self.lineEdit_Coni.text())

			if self.lineEdit_pdi.text() == "":
				pdi = ''
			else:
				pdi = int(self.lineEdit_pdi.text())

			if self.lineEdit_stambecco.text() == "":
				stambecco = ''
			else:
				stambecco = int(self.lineEdit_stambecco.text())

			if self.lineEdit_canidi.text() == "":
				canidi = ''
			else:
				canidi = int(self.lineEdit_canidi.text())

			if self.lineEdit_ursidi.text() == "":
				ursidi = ''
			else:
				ursidi = int(self.lineEdit_ursidi.text())

			if self.lineEdit_megacero.text() == "":
				megacero = ''
			else:
				megacero = int(self.lineEdit_megacero.text())
			
			
			search_dict = {
			self.TABLE_FIELDS[0]  : "'"+str(self.comboBox_sito.currentText())+"'", 									#1 - Sito
			self.TABLE_FIELDS[1]  : "'"+str(self.lineEdit_area.text())+"'",									#2 - Area
			self.TABLE_FIELDS[2]  : us,																				#3 - US
			self.TABLE_FIELDS[3]  : "'"+str(self.lineEdit_quadrato.text())+"'",								#4 - Definizione stratigrafica
			self.TABLE_FIELDS[4]  : coord_x,							#5 - Definizione intepretata
			self.TABLE_FIELDS[5]  : coord_y,									#6 - descrizione
			self.TABLE_FIELDS[6]  : coord_z,								#7 - interpretazione
			self.TABLE_FIELDS[7]  : bos_bison,								#8 - periodo iniziale
			self.TABLE_FIELDS[8]  : calcinati,								#9 - fase iniziale
			self.TABLE_FIELDS[9]  : camoscio,	 							#10 - periodo finale iniziale
			self.TABLE_FIELDS[10] : capriolo, 								#11 - fase finale
			self.TABLE_FIELDS[11] : cervo,								#12 - attivita  
			self.TABLE_FIELDS[12] : combusto,										#13 - attivita  
			self.TABLE_FIELDS[13] : coni,											#14 - anno scavo
			self.TABLE_FIELDS[14] : pdi, 								#15 - metodo
			self.TABLE_FIELDS[15] : stambecco,								#16 - data schedatura
			self.TABLE_FIELDS[16] : strie,							#17 - schedatore
			self.TABLE_FIELDS[17] : canidi,							#18 - formazione
			self.TABLE_FIELDS[18] : ursidi,							#19 - conservazione
			self.TABLE_FIELDS[19] : megacero,								#20 - colore
			}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			if bool(search_dict) == False:
				QMessageBox.warning(self, "ATTENZIONE", "Non e' stata impostata alcuna ricerca!!!",  QMessageBox.Ok)
			else:
				res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
				if bool(search_dict) == False:
					QMessageBox.warning(self, "ATTENZIONE", "Non e' stata impostata alcuna ricerca!!!",  QMessageBox.Ok)
				else:
					res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)

					if bool(res) == False:
						QMessageBox.warning(self, "ATTENZIONE", "Non e' stato trovato alcun record!",  QMessageBox.Ok)

						self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
						self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
						self.fill_fields(self.REC_CORR)
						self.BROWSE_STATUS = "b"
						self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])

						self.setComboBoxEnable(["self.comboBox_sito"],"False")

					else:
						self.DATA_LIST = []
						for i in res:
							self.DATA_LIST.append(i)
						self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), 0
						self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
						self.fill_fields()
						self.BROWSE_STATUS = "b"
						self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
						self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)

						if self.REC_TOT == 1:
							strings = ("E' stato trovato", self.REC_TOT, "record")
						else:
							strings = ("Sono stati trovati", self.REC_TOT, "records")

						self.setComboBoxEnable(["self.comboBox_sito"],"False")

						QMessageBox.warning(self, "Messaggio", "%s %d %s" % strings,  QMessageBox.Ok)

		self.enable_button_search(1)

	def update_if(self, msg):
		rec_corr = self.REC_CORR
		self.msg = msg
		if self.msg == 1:
			test = self.update_record()
			if test == 1:
				id_list = []
				for i in self.DATA_LIST:
					id_list.append(eval("i."+ self.ID_TABLE))
				self.DATA_LIST = []
				if self.SORT_STATUS == "n":
					temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE) #self.DB_MANAGER.query_bool(self.SEARCH_DICT_TEMP, self.MAPPER_TABLE_CLASS) #
				else:
					temp_data_list = self.DB_MANAGER.query_sort(id_list, self.SORT_ITEMS_CONVERTED, self.SORT_MODE, self.MAPPER_TABLE_CLASS, self.ID_TABLE)
				for i in temp_data_list:
					self.DATA_LIST.append(i)
				self.BROWSE_STATUS = "b"
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				if type(self.REC_CORR) == "<type 'str'>":
					corr = 0
				else:
					corr = self.REC_CORR 
				return 1
			elif test == 0:
				return 0


	#custom functions
	def charge_records(self):
		self.DATA_LIST = []
		id_list = []
		for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
			id_list.append(eval("i."+ self.ID_TABLE))
		temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
		for i in temp_data_list:
			self.DATA_LIST.append(i)

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today


	def table2dict(self, n):
		self.tablename = n
		row = eval(self.tablename+".rowCount()")
		col = eval(self.tablename+".columnCount()")
		lista=[]
		for r in range(row):
			sub_list = []
			for c in range(col):
				value = eval(self.tablename+".item(r,c)")
				if bool(value) == True:
					sub_list.append(str(value.text()))
			lista.append(sub_list)
		return lista


	def empty_fields(self):
		self.comboBox_sito.setEditText("")
		self.lineEdit_area.clear()
		self.lineEdit_us.clear()
		self.lineEdit_quadrato.clear()
		self.lineEdit_coord_x.clear()
		self.lineEdit_coord_y.clear()
		self.lineEdit_coord_z.clear()
		self.lineEdit_bos_bison.clear()
		self.lineEdit_calcinati.clear()
		self.lineEdit_camoscio.clear()
		self.lineEdit_capriolo.clear()
		self.lineEdit_cervi.clear()
		self.lineEdit_combuste.clear()
		self.lineEdit_Coni.clear()
		self.lineEdit_pdi.clear()
		self.lineEdit_stambecco.clear()
		self.lineEdit_strie.clear()
		self.lineEdit_canidi.clear()
		self.lineEdit_ursidi.clear()
		self.lineEdit_megacero.clear()


	def fill_fields(self, n=0):
		self.rec_num = n
		try:
			self.comboBox_sito.setEditText(self.DATA_LIST[self.rec_num].sito)  									#1 - Sito
			self.lineEdit_area.setText(str(self.DATA_LIST[self.rec_num].area)) 						#2 - Periodo
			
			if self.DATA_LIST[self.rec_num].us == None:												#4 - cronologia iniziale
				self.lineEdit_us.setText("")
			else:
				self.lineEdit_us.setText(str(self.DATA_LIST[self.rec_num].us))
			
			 						#2 - Periodo
			self.lineEdit_quadrato.setText(str(self.DATA_LIST[self.rec_num].quadrato)) 						#2 - Periodo

			if self.DATA_LIST[self.rec_num].coord_x == None:												#4 - cronologia iniziale
				self.lineEdit_coord_x.setText("")
			else:
				self.lineEdit_coord_x.setText(str(self.DATA_LIST[self.rec_num].coord_x))

			if self.DATA_LIST[self.rec_num].coord_y == None:												#4 - cronologia iniziale
				self.lineEdit_coord_y.setText("")
			else:
				self.lineEdit_coord_y.setText(str(self.DATA_LIST[self.rec_num].coord_y))

			if self.DATA_LIST[self.rec_num].coord_z == None:												#4 - cronologia iniziale
				self.lineEdit_coord_z.setText("")
			else:
				self.lineEdit_coord_z.setText(str(self.DATA_LIST[self.rec_num].coord_z))

			if self.DATA_LIST[self.rec_num].bos_bison == None:												#4 - cronologia iniziale
				self.lineEdit_bos_bison.setText("")
			else:
				self.lineEdit_bos_bison.setText(str(self.DATA_LIST[self.rec_num].bos_bison))

			if self.DATA_LIST[self.rec_num].calcinati == None:												#4 - cronologia iniziale
				self.lineEdit_calcinati.setText("")
			else:
				self.lineEdit_calcinati.setText(str(self.DATA_LIST[self.rec_num].calcinati))

			if self.DATA_LIST[self.rec_num].camoscio == None:												#4 - cronologia iniziale
				self.lineEdit_camoscio.setText("")
			else:
				self.lineEdit_camoscio.setText(str(self.DATA_LIST[self.rec_num].camoscio))

			if self.DATA_LIST[self.rec_num].capriolo == None:												#4 - cronologia iniziale
				self.lineEdit_capriolo.setText("")
			else:
				self.lineEdit_capriolo.setText(str(self.DATA_LIST[self.rec_num].capriolo))

			if self.DATA_LIST[self.rec_num].cervo == None:												#4 - cronologia iniziale
				self.lineEdit_cervi.setText("")
			else:
				self.lineEdit_cervi.setText(str(self.DATA_LIST[self.rec_num].cervo))

			if self.DATA_LIST[self.rec_num].combusto == None:												#4 - cronologia iniziale
				self.lineEdit_combuste.setText("")
			else:
				self.lineEdit_combuste.setText(str(self.DATA_LIST[self.rec_num].combusto))

			if self.DATA_LIST[self.rec_num].coni == None:												#4 - cronologia iniziale
				self.lineEdit_Coni.setText("")
			else:
				self.lineEdit_Coni.setText(str(self.DATA_LIST[self.rec_num].coni))

			if self.DATA_LIST[self.rec_num].pdi == None:												#4 - cronologia iniziale
				self.lineEdit_pdi.setText("")
			else:
				self.lineEdit_pdi.setText(str(self.DATA_LIST[self.rec_num].pdi))

			if self.DATA_LIST[self.rec_num].stambecco == None:												#4 - cronologia iniziale
				self.lineEdit_stambecco.setText("")
			else:
				self.lineEdit_stambecco.setText(str(self.DATA_LIST[self.rec_num].stambecco))

			if self.DATA_LIST[self.rec_num].strie == None:												#4 - cronologia iniziale
				self.lineEdit_strie.setText("")
			else:
				self.lineEdit_strie.setText(str(self.DATA_LIST[self.rec_num].strie))

			if self.DATA_LIST[self.rec_num].canidi == None:												#4 - cronologia iniziale
				self.lineEdit_canidi.setText("")
			else:
				self.lineEdit_canidi.setText(str(self.DATA_LIST[self.rec_num].canidi))
	
			if self.DATA_LIST[self.rec_num].ursidi == None:												#4 - cronologia iniziale
				self.lineEdit_ursidi.setText("")
			else:
				self.lineEdit_ursidi.setText(str(self.DATA_LIST[self.rec_num].ursidi))
	
			if self.DATA_LIST[self.rec_num].megacero == None:												#4 - cronologia iniziale
				self.lineEdit_megacero.setText("")
			else:
				self.lineEdit_megacero.setText(str(self.DATA_LIST[self.rec_num].megacero))

		except Exception, e:
			QMessageBox.warning(self, "Errore Fill Fields", str(e),  QMessageBox.Ok)


	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		#data
		if self.lineEdit_us.text() == "":
			us = None
		else:
			us = str(self.lineEdit_us.text())

		if self.lineEdit_coord_x.text() == "":
			coord_x = None
		else:
			coord_x = float(self.lineEdit_coord_x.text())

		if self.lineEdit_coord_y.text() == "":
			coord_y = None
		else:
			coord_y = float(self.lineEdit_coord_y.text())

		if self.lineEdit_coord_z.text() == "":
			coord_z = None
		else:
			coord_z = float(self.lineEdit_coord_z.text())

		if self.lineEdit_bos_bison.text() == "":
			bos_bison = None
		else:
			bos_bison = str(self.lineEdit_bos_bison.text())

		if self.lineEdit_calcinati.text() == "":
			calcinati = None
		else:
			calcinati = str(self.lineEdit_calcinati.text())

		if self.lineEdit_camoscio.text() == "":
			camoscio = None
		else:
			camoscio = str(self.lineEdit_camoscio.text())

		if self.lineEdit_capriolo.text() == "":
			capriolo = None
		else:
			capriolo = str(self.lineEdit_capriolo.text())

		if self.lineEdit_cervi.text() == "":
			cervo = None
		else:
			cervo = str(self.lineEdit_cervi.text())

		if self.lineEdit_combuste.text() == "":
			combusto = None
		else:
			combusto = str(self.lineEdit_combuste.text())

		if self.lineEdit_Coni.text() == "":
			coni = None
		else:
			coni = str(self.lineEdit_Coni.text())

		if self.lineEdit_pdi.text() == "":
			pdi = None
		else:
			pdi = str(self.lineEdit_pdi.text())

		if self.lineEdit_stambecco.text() == "":
			stambecco = None
		else:
			stambecco = str(self.lineEdit_stambecco.text())

		if self.lineEdit_strie.text() == "":
			strie = None
		else:
			strie = str(self.lineEdit_strie.text())

		if self.lineEdit_canidi.text() == "":
			canidi = None
		else:
			canidi = str(self.lineEdit_canidi.text())

		if self.lineEdit_ursidi.text() == "":
			ursidi = None
		else:
			ursidi = str(self.lineEdit_ursidi.text())

		if self.lineEdit_megacero.text() == "":
			megacero = None
		else:
			megacero = str(self.lineEdit_megacero.text())

		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_sito.currentText()), 						#1 - Sito
		str(self.lineEdit_area.text()), 					#2 - periodo
		str(us),
		str(self.lineEdit_quadrato.text()), 					#3 - fase
		str(coord_x),
		str(coord_y),
		str(coord_z),
		str(bos_bison),
		str(calcinati),
		str(camoscio),
		str(capriolo),
		str(cervo),
		str(combusto),
		str(coni),
		str(pdi),
		str(stambecco),
		str(strie),
		str(canidi),
		str(ursidi),
		str(megacero)]												#8 - cont_per provvisorio


	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("str(self.DATA_LIST[self.REC_CORR]." + i + ")"))

	def setComboBoxEnable(self, f, v):
		field_names = f
		value = v

		for fn in field_names:
			cmd = ('%s%s%s%s') % (fn, '.setEnabled(', v, ')')
			eval(cmd)

	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()

		if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
			return 0
		else:
			return 1

	def update_record(self):
		try:
			self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, 
						self.ID_TABLE,
						[eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")],
						self.TABLE_FIELDS,
						self.rec_toupdate())
			return 1
		except Exception, e:
			QMessageBox.warning(self, "Messaggio", "Problema di encoding: sono stati inseriti accenti o caratteri non accettati dal database. Se chiudete ora la scheda senza correggere gli errori perderete i dati. Fare una copia di tutto su un foglio word a parte. Errore :" + str(e), QMessageBox.Ok)
			return 0

	def rec_toupdate(self):
		rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)
		return rec_to_update

	def testing(self, name_file, message):
		f = open(str(name_file), 'w')
		f.write(str(message))
		f.close()


## Class end

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = pyarchinit_US()
	ui.show()
	sys.exit(app.exec_())
