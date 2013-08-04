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

from datetime import date
from psycopg2 import *

#--import pyArchInit modules--#
from  pyarchinit_Periodo_fase_ui import Ui_DialogPeriodoFase
from  pyarchinit_Periodo_fase_ui import *
from  pyarchinit_pyqgis import Pyarchinit_pyqgis
from  pyarchinit_utility import *
from  pyarchinit_error_check import *

try:
	from  pyarchinit_db_manager import *
except:
	pass

from  sortpanelmain import SortPanelMain

from pyarchinit_PDF_administrator_mainapp import pyarchinit_PDFAdministrator  #sistema sperimentale non attivo
from  pyarchinit_exp_Periodizzazionesheet_pdf import *

class pyarchinit_Periodizzazione(QDialog, Ui_DialogPeriodoFase):
	MSG_BOX_TITLE = "PyArchInit - Scheda Periodizzazione"
	DATA_LIST = []
	DATA_LIST_REC_CORR = []
	DATA_LIST_REC_TEMP = []
	REC_CORR = 0
	REC_TOT = 0
	BROWSE_STATUS = "b"
	STATUS_ITEMS = {"b": "Usa", "f": "Trova", "n": "Nuovo Record"}
	SORT_MODE = 'asc'
	SORTED_ITEMS = {"n": "Non ordinati", "o": "Ordinati"}
	SORT_STATUS = "n"
	UTILITY = Utility()
	DB_MANAGER = ""
	TABLE_NAME = 'periodizzazione_table'
	MAPPER_TABLE_CLASS = "PERIODIZZAZIONE"
	NOME_SCHEDA = "Scheda Periodizzazione"
	ID_TABLE = "id_perfas"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito":"sito",
	"Periodo":"periodo",
	"Fase":"fase",
	"Cronologia iniziale":"cron_iniziale",
	"Cronologia finale":"cron_finale",
	"Descrizione":"descrizione",
	"Datazione estesa":"datazione_estesa",
	"Codice periodo":"cont_per"
	}
	SORT_ITEMS = [
				ID_TABLE,
				"Sito",
				"Periodo",
				"Fase",
				"Descrizione",
				"Cronologia iniziale",
				"Cronologia finale",
				"Codice periodo"
				]

	TABLE_FIELDS = [
					'sito',
					'periodo',
					'fase',
					'cron_iniziale',
					'cron_finale',
					'descrizione',
					'datazione_estesa',
					'cont_per'
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
				self.BROWSE_STATUS = "b"
				self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
				self.label_sort.setText(self.SORTED_ITEMS["n"])
				self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
				self.charge_list_sito()
				self.fill_fields()
			else:
				QMessageBox.warning(self, "BENVENUTO", "Benvenuto in pyArchInit" + self.NOME_SCHEDA + ". Il database e' vuoto. Premi 'Ok' e buon lavoro!",  QMessageBox.Ok)
				self.charge_list_sito()
				self.on_pushButton_new_rec_pressed()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> Tabella non presente. E' NECESSARIO RIAVVIARE QGIS" ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def charge_list_sito(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))

		try:
			sito_vl.remove('')
		except:
			pass
		self.comboBox_sito.clear()
		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)

	def on_pushButton_pdf_exp_pressed(self):
		Periodizzazione_pdf_sheet = generate_Periodizzazione_pdf() #deve essere importata la classe
		data_list = self.generate_list_pdf() #deve essere aggiunta la funzione
		Periodizzazione_pdf_sheet.build_Periodizzazione_sheets(data_list) #deve essere aggiunto il file per generare i pdf
		#codice per l'esportazione sperimentale dei PDF #
		"""
		dlg = pyarchinit_PDFAdministrator()
		dlg.set_table_name(self.TABLE_NAME)
		dlg.connect()
		msg = QMessageBox.warning(self,'ATTENZIONE',"Vuoi creare un nuovo layout PFD?", QMessageBox.Cancel,1)
		dlg.connect()
		##		dlg.on_pushButton_connect_pressed()
		if msg == 1:
			dlg.on_pushButton_new_rec_pressed()
			dlg.charge_list()
		
		id_list = []

		for i in self.DATA_LIST:
			id_list.append(eval("i." + self.ID_TABLE))
		dlg.add_id_list(id_list)

		dlg.exec_()
		"""
	def generate_list_pdf(self):
		periodo = ""
		fase = ""
		cron_iniz = ""
		cron_fin = ""
		
		data_list = []
		for i in range(len(self.DATA_LIST)):
			
			if self.DATA_LIST[i].periodo == None:
				periodo = ""
			else:
				periodo = str(self.DATA_LIST[i].periodo)
			
			if self.DATA_LIST[i].fase == None:
				fase = ""
			else:
				fase = str(self.DATA_LIST[i].fase)
				
			if self.DATA_LIST[i].cron_iniziale == None:
				cron_iniz = ""
			else:
				cron_iniz = str(self.DATA_LIST[i].cron_iniziale)
				
			if self.DATA_LIST[i].cron_finale == None:
				cron_fin = ""
			else:
				cron_fin = str(self.DATA_LIST[i].cron_finale)
			
			
			data_list.append([
			str(self.DATA_LIST[i].sito), 										#1 - Sito
			str(periodo),															#2 - Area
			str(fase),																#3 - US
			str(cron_iniz),															#4 - definizione stratigrafica
			str(cron_fin),															#5 - definizione intepretata
			str(self.DATA_LIST[i].datazione_estesa),						#6 - descrizione
			unicode(self.DATA_LIST[i].descrizione)						#7 - interpretazione
		])
		return data_list

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
		if self.records_equal_check() == 1 and self.BROWSE_STATUS == "b":
			msg = self.update_if(QMessageBox.warning(self,'Errore',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
		#else:
		self.enable_button_search(0)

		#set the GUI for a new search

		if self.BROWSE_STATUS != "f":
			self.BROWSE_STATUS = "f"
			
			###

			self.setComboBoxEditable(["self.comboBox_sito"],0)
			self.setComboBoxEditable(["self.comboBox_periodo"],0)
			self.setComboBoxEditable(["self.comboBox_fase"],0)
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.comboBox_periodo"],"True")
			self.setComboBoxEnable(["self.comboBox_fase"],"True")

			###
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.set_rec_counter('','')
			self.label_sort.setText(self.SORTED_ITEMS["n"])
			self.charge_list()
			self.empty_fields()


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
					self.charge_list_sito()
					self.charge_records()
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)
					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_periodo"],1)
					self.setComboBoxEditable(["self.comboBox_fase"],1)
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_periodo"],"False")
					self.setComboBoxEnable(["self.comboBox_fase"],"False")
					self.fill_fields(self.REC_CORR)
					self.enable_button(1)
			else:
				pass

	def data_error_check(self):
		test = 0
		EC = Error_check()

		cron_iniz = self.lineEdit_cron_iniz.text()
		cron_fin = self.lineEdit_cron_fin.text()
		if cron_iniz != "":
			if EC.data_is_int(cron_iniz) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Cronologia Iniziale. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		if cron_fin != "":
			if EC.data_is_int(cron_fin) == 0:
				QMessageBox.warning(self, "ATTENZIONE", "Campo Cronologia Finale. \n Il valore deve essere di tipo numerico",  QMessageBox.Ok)
				test = 1

		return test

	def insert_new_rec(self):
		cont_per = 0
		try:
			if self.lineEdit_cron_iniz.text() == "":
				cron_iniz = None
			else:
				cron_iniz = int(self.lineEdit_cron_iniz.text())

			if self.lineEdit_cron_fin.text() == "":
				cron_fin = None
			else:
				cron_fin = int(self.lineEdit_cron_fin.text())

			if self.lineEdit_codice_periodo.text() == "":
				cont_per = None
			else:
				cont_per = int(self.lineEdit_codice_periodo.text())
				
			data = self.DB_MANAGER.insert_periodizzazione_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1, #0 - max num id
			unicode(self.comboBox_sito.currentText()), 													#1 - Sito
			int(self.comboBox_periodo.currentText()), 													#2 - Periodo
			int(self.comboBox_fase.currentText()), 														#3 - Fase
			cron_iniz,																								#4 - Cron iniziale
			cron_fin,																									#5 - Cron finale
			unicode(self.textEdit_descrizione_per.toPlainText()),										#6 - Descrizione
			unicode(self.lineEdit_per_estesa.text()),														#7 - Periodizzazione estesa
			cont_per)																								#8 - Cont_per 

			try:
				self.DB_MANAGER.insert_data_session(data)
				return 1
			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.ID_TABLE + " gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "immisione 1 \n"+ str(msg),  QMessageBox.Ok)
				return 0
		except Exception, e:
			QMessageBox.warning(self, "Errore", "Errore di immissione 2 \n"+str(e),  QMessageBox.Ok)
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
		self.enable_button_search(0)
		self.setComboBoxEditable(["self.comboBox_sito"],1)

		#set the GUI for a new search

		if self.BROWSE_STATUS != "f":
			self.BROWSE_STATUS = "f"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()
			self.set_rec_counter('','')
			self.label_sort.setText(self.SORTED_ITEMS["n"])

			self.setComboBoxEditable(["self.comboBox_sito"],1)
			self.setComboBoxEditable(["self.comboBox_periodo"],1)
			self.setComboBoxEditable(["self.comboBox_fase"],1)
			self.setComboBoxEnable(["self.comboBox_sito"],"True")
			self.setComboBoxEnable(["self.comboBox_periodo"],"True")
			self.setComboBoxEnable(["self.comboBox_fase"],"True")

	def on_pushButton_search_go_pressed(self):
		if self.BROWSE_STATUS != "f":
			QMessageBox.warning(self, "ATTENZIONE", "Per eseguire una nuova ricerca clicca sul pulsante 'new search' ",  QMessageBox.Ok)
		else:
			if self.lineEdit_cron_iniz.text() != "":
				cron_iniziale = "'"+unicode(self.lineEdit_cron_iniz.text())+"'"
			else:
				cron_iniziale = ""
				
			if self.lineEdit_cron_fin.text() != "":
				cron_finale ="'"+ unicode(self.lineEdit_cron_fin.text())+"'"
			else:
				cron_finale = ""

			if self.comboBox_periodo.currentText() != "":
				periodo = "'"+unicode(self.comboBox_periodo.currentText())+"'"
			else:
				periodo = ""

			if self.comboBox_fase.currentText() != "":
				fase = "'"+unicode(self.comboBox_fase.currentText())+"'"
			else:
				fase = ""

			search_dict = {
			'sito' : "'"+unicode(self.comboBox_sito.currentText())+"'",					#1 - Sito
			'periodo': periodo,																			#2 - Periodo
			'fase': fase,																					#3 - Fase
			'cron_iniziale': cron_iniziale,																#4 - Cron iniziale
			'cron_finale': cron_finale,																#5 - Crion finale
			'descrizione': unicode(self.textEdit_descrizione_per.toPlainText()),			#6 - Descrizione
			'datazione_estesa': "'" + unicode(self.lineEdit_per_estesa.text()) + "'",	#7 - Periodizzazione estesa
			'cont_per': "'" + unicode(self.lineEdit_codice_periodo.text()) + "'"			#8 - Codice periodo
			}

			u = Utility()
			search_dict = u.remove_empty_items_fr_dict(search_dict)

			if bool(search_dict) == False:
				QMessageBox.warning(self, "ATTENZIONE", "Non e' stata impostata alcuna ricerca!!!",  QMessageBox.Ok)
			else:
				res = self.DB_MANAGER.query_bool(search_dict, self.MAPPER_TABLE_CLASS)
				
				
				if bool(res) == False:
					QMessageBox.warning(self, "ATTENZIONE", "Non e' stato trovato alcun record!",  QMessageBox.Ok)

					self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
					self.DATA_LIST_REC_TEMP = self.DATA_LIST_REC_CORR = self.DATA_LIST[0]
					self.fill_fields(self.REC_CORR)

					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_periodo"],1)
					self.setComboBoxEditable(["self.comboBox_fase"],1)

					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_periodo"],"False")
					self.setComboBoxEnable(["self.comboBox_fase"],"False")

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

					self.setComboBoxEditable(["self.comboBox_sito"],1)
					self.setComboBoxEditable(["self.comboBox_periodo"],1)
					self.setComboBoxEditable(["self.comboBox_fase"],1)
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_periodo"],"False")
					self.setComboBoxEnable(["self.comboBox_fase"],"False")

					QMessageBox.warning(self, "Messaggio", "%s %d %s" % strings,  QMessageBox.Ok)

		self.enable_button_search(1)

	def on_pushButton_show_periodo_pressed(self):
		if self.lineEdit_codice_periodo.text() == "":
			QMessageBox.warning(self, "Messaggio", "Codice periodo non assegnato",  QMessageBox.Ok)
		else:
			cont_per = self.lineEdit_codice_periodo.text()
			self.pyQGIS.charge_vector_layers_periodo(int(cont_per))


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
		id_list = []
		self.DATA_LIST = []
		for i in self.DB_MANAGER.query(eval(self.MAPPER_TABLE_CLASS)):
			id_list.append(eval("i." + self.ID_TABLE))
		temp_data_list = self.DB_MANAGER.query_sort(id_list, [self.ID_TABLE], 'asc', self.MAPPER_TABLE_CLASS, self.ID_TABLE)
		for i in temp_data_list:
			self.DATA_LIST.append(i)


	def setComboBoxEditable(self, f, n):
		field_names = f
		value = n

		for fn in field_names:
			cmd = ('%s%s%d%s') % (fn, '.setEditable(', n, ')')
			eval(cmd)

	def setComboBoxEnable(self, f, v):
		field_names = f
		value = v

		for fn in field_names:
			cmd = ('%s%s%s%s') % (fn, '.setEnabled(', v, ')')
			eval(cmd)

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
		self.comboBox_sito.setEditText("")  						#1 - Sito
		self.comboBox_periodo.setEditText("") 					#2 - Periodo
		self.comboBox_fase.setEditText("") 						#3 - Fase
		self.lineEdit_cron_iniz.clear()									#4 - Cronologia iniziale
		self.lineEdit_cron_fin.clear()									#5 - Cronologia finale
		self.lineEdit_per_estesa.clear()								#6 - Datazione estesa
		self.textEdit_descrizione_per.clear()							#7 - Descrizione
		self.lineEdit_codice_periodo.clear()							#8 - Codice periodo

	def fill_fields(self, n=0):
		self.rec_num = n
		try:
			unicode(self.comboBox_sito.setEditText(self.DATA_LIST[self.rec_num].sito))  							#1 - Sito
			
			self.comboBox_periodo.setEditText(str(self.DATA_LIST[self.rec_num].periodo))							#2 - Periodo
			self.comboBox_fase.setEditText(str(self.DATA_LIST[self.rec_num].fase))									#3 - Fase

			if self.DATA_LIST[self.rec_num].cron_iniziale == None:															#4 - Cronologia iniziale
				self.lineEdit_cron_iniz.setText("")
			else:
				self.lineEdit_cron_iniz.setText(str(self.DATA_LIST[self.rec_num].cron_iniziale))

			if self.DATA_LIST[self.rec_num].cron_finale == None:															#5 - Cronologia finale
				self.lineEdit_cron_fin.setText("")
			else:
				self.lineEdit_cron_fin.setText(str(self.DATA_LIST[self.rec_num].cron_finale))

			unicode(self.lineEdit_per_estesa.setText(self.DATA_LIST[self.rec_num].datazione_estesa))			#6 - Datazione estesa
			unicode(self.textEdit_descrizione_per.setText(self.DATA_LIST[self.rec_num].descrizione))				#7 - Descrizione

			if self.DATA_LIST[self.rec_num].cont_per == None:															#8 - Codice periodo
				self.lineEdit_codice_periodo.setText("")
			else:
				self.lineEdit_codice_periodo.setText(str(self.DATA_LIST[self.rec_num].cont_per))
	
		except Exception, e:
			QMessageBox.warning(self, "Errore Fill Fields", str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		#data
		if self.lineEdit_cron_iniz.text() == "":
			cron_iniz = None
		else:
			cron_iniz = unicode(self.lineEdit_cron_iniz.text())

		if self.lineEdit_cron_fin.text() == "":
			cron_fin = None
		else:
			cron_fin = unicode(self.lineEdit_cron_fin.text())

		if self.lineEdit_codice_periodo.text() == "":
			cont_per = None
		else:
			cont_per = unicode(self.lineEdit_codice_periodo.text())

		self.DATA_LIST_REC_TEMP = [
		unicode(self.comboBox_sito.currentText()), 								#1 - Sito
		unicode(self.comboBox_periodo.currentText()), 						#2 - Periodo
		unicode(self.comboBox_fase.currentText()), 							#3 - Fase
		unicode(cron_iniz),																#4 - Cron iniziale
		unicode(cron_fin),																#5 - Cron finale
		unicode(self.textEdit_descrizione_per.toPlainText()),					#6 - Descrizioene
		unicode(self.lineEdit_per_estesa.text()),									#7 - Cron estesa
		unicode(cont_per)]																#8 - Cont_per

	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("unicode(self.DATA_LIST[self.REC_CORR]." + i + ")"))

	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()

		if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
			return 0
		else:
			return 1

	def update_record(self):
		self.DB_MANAGER.update(self.MAPPER_TABLE_CLASS, 
						self.ID_TABLE,
						[eval("int(self.DATA_LIST[self.REC_CORR]." + self.ID_TABLE+")")],
						self.TABLE_FIELDS,
						self.rec_toupdate())

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