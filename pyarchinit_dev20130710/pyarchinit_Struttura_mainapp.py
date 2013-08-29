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
from  pyarchinit_Struttura_ui import Ui_DialogStruttura
from  pyarchinit_Struttura_ui import *
from  pyarchinit_utility import *
from  pyarchinit_error_check import *

try:
	from  pyarchinit_db_manager import *
except:
	pass

from  sortpanelmain import SortPanelMain
from delegateComboBox import *

from  pyarchinit_exp_Strutturasheet_pdf import *

class pyarchinit_Struttura(QDialog, Ui_DialogStruttura):
	MSG_BOX_TITLE = "PyArchInit - Scheda Struttura"
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
	TABLE_NAME = 'struttura_table'
	MAPPER_TABLE_CLASS = 'STRUTTURA'
	NOME_SCHEDA = "Scheda Struttura"
	ID_TABLE = "id_struttura"
	CONVERSION_DICT = {
	ID_TABLE:ID_TABLE,
	"Sito":"sito",
	"Sigla struttura":"sigla_struttura",
	"Numero struttura":"numero_struttura",
	"Categoria struttura":"categoria_struttura",
	"Tipologia struttura":"tipologia_struttura",
	"Definizione struttura":"definizione_struttura",
	"Descrizione":"descrizione",
	"Interpretazione":"interpretazione",
	"Periodo iniziale":"periodo_iniziale",
	"Fase iniziale":"fase_iniziale",
	"Periodo finale":"periodo_finale",
	"Fase_finale":"fase_finale",
	"Datazione estesa":"datazione_estesa"
	}
	SORT_ITEMS = [
				ID_TABLE,
				"Sito",
				"Sigla struttura",
				"Numero struttura",
				"Categoria struttura",
				"Tipologia struttura",
				"Definizione struttura",
				"Descrizione",
				"Interpretazione",
				"Periodo iniziale",
				"Fase iniziale",
				"Periodo finale",
				"Fase_finale",
				"Datazione estesa"
				]

	TABLE_FIELDS = [
					"sito",
					"sigla_struttura",
					"numero_struttura",
					"categoria_struttura",
					"tipologia_struttura",
					"definizione_struttura",
					"descrizione",
					"interpretazione",
					"periodo_iniziale",
					"fase_iniziale",
					"periodo_finale",
					"fase_finale",
					"datazione_estesa",
					"materiali_impiegati",
					"elementi_strutturali",
					"rapporti_struttura",
					"misure_struttura"
					]

	def __init__(self, iface):
		self.iface = iface

		QDialog.__init__(self)
		self.setupUi(self)
		self.customize_GUI()
		self.currentLayerId = None


		try:
			self.on_pushButton_connect_pressed()
		except:
			pass

		#SIGNALS & SLOTS Functions
		self.connect(self.comboBox_sigla_struttura, SIGNAL("editTextChanged (const QString&)"), self.add_value_to_categoria)
		self.connect(self.comboBox_sito, SIGNAL("editTextChanged (const QString&)"), self.charge_periodo_list)
		self.connect(self.comboBox_per_iniz, SIGNAL("currentIndexChanged(int)"), self.charge_fase_iniz_list)
		self.connect(self.comboBox_per_fin, SIGNAL("currentIndexChanged(int)"), self.charge_fase_fin_list)

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
				self.charge_list()
				self.fill_fields()
			else:
				QMessageBox.warning(self, "BENVENUTO", "Benvenuto in pyArchInit" + self.NOME_SCHEDA + ". Il database e' vuoto. Premi 'Ok' e buon lavoro!",  QMessageBox.Ok)
				self.charge_list()
				self.on_pushButton_new_rec_pressed()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita" + str(e) + "<br>Tabella non presente. E' NECESSARIO RIAVVIARE QGIS" ,  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def customize_GUI(self):
		self.tableWidget_rapporti.setColumnWidth(0,120)
		self.tableWidget_rapporti.setColumnWidth(1,280)
		self.tableWidget_rapporti.setColumnWidth(2,75)
		self.tableWidget_rapporti.setColumnWidth(3,75)

		self.tableWidget_materiali_impiegati.setColumnWidth(0,535)

		self.tableWidget_elementi_strutturali.setColumnWidth(0,480)
		self.tableWidget_elementi_strutturali.setColumnWidth(1,60)

		self.tableWidget_misurazioni.setColumnWidth(0,360)
		self.tableWidget_misurazioni.setColumnWidth(1,100)
		self.tableWidget_misurazioni.setColumnWidth(2,60)

		self.setComboBoxEditable(["self.comboBox_per_iniz"],1)
		self.setComboBoxEditable(["self.comboBox_fas_iniz"],1)
		self.setComboBoxEditable(["self.comboBox_per_fin"],1)
		self.setComboBoxEditable(["self.comboBox_fas_fin"],1)

		valuesRapporti = ['Si appoggia a', 'Gli si appoggia' 'Connesso con', 'Si sovrappone a', 'Gli si sovrappone', 'Ampliato da', 'Amplia']
		self.delegateRapporti = ComboBoxDelegate()
		self.delegateRapporti.def_values(valuesRapporti)
		self.delegateRapporti.def_editable('True')
		self.tableWidget_rapporti.setItemDelegateForColumn(0,self.delegateRapporti)
		

		valuesMateriali = ["Terra", "Pietre", "Laterizio", "Ciottoli", "Calcare", "Calce", "Legno", "Concotto", "Ghiaia", "Sabbia", "Malta", "Metallo", "Gesso"]
		self.delegateMateriali = ComboBoxDelegate()
		self.delegateMateriali.def_values(valuesMateriali)
		self.delegateMateriali.def_editable('False')
		self.tableWidget_materiali_impiegati.setItemDelegateForColumn(0,self.delegateMateriali)




	def charge_list(self):
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))

		try:
			sito_vl.remove('')
		except:
			pass
		self.comboBox_sito.clear()
		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)

	def charge_periodo_list(self):
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			}

			periodo_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

			periodo_list = []

			for i in range(len(periodo_vl)):
				periodo_list.append(str(periodo_vl[i].periodo))
			try:
				periodo_vl.remove('')
			except:
				pass

			periodo_list.sort()

			self.comboBox_per_iniz.clear()
			self.comboBox_per_iniz.addItems(periodo_list)
			self.comboBox_per_iniz.setEditText(self.DATA_LIST[self.rec_num].periodo_iniziale)
			self.comboBox_per_fin.clear()
			self.comboBox_per_fin.addItems(periodo_list)
			self.comboBox_per_fin.setEditText(self.DATA_LIST[self.rec_num].periodo_finale)
		except:
			pass

	def charge_fase_iniz_list(self):
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			'periodo'  : "'"+str(self.comboBox_per_iniz.currentText())+"'",
			}

			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(str(fase_list_vl[i].fase))

			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_iniz.clear()

			fase_list.sort()
			self.comboBox_fas_iniz.addItems(fase_list)
			self.comboBox_fas_iniz.setEditText(self.DATA_LIST[self.rec_num].fase_iniziale)

		except:
			pass


	def charge_fase_fin_list(self):
		try:
			search_dict = {
			'sito'  : "'"+str(self.comboBox_sito.currentText())+"'",
			'periodo'  : "'"+str(self.comboBox_per_fin.currentText())+"'",
			}

			fase_list_vl = self.DB_MANAGER.query_bool(search_dict, 'PERIODIZZAZIONE')

			fase_list = []

			for i in range(len(fase_list_vl)):
				fase_list.append(str(fase_list_vl[i].fase))

			try:
				fase_list.remove('')
			except:
				pass

			self.comboBox_fas_fin.clear()

			fase_list.sort()
			self.comboBox_fas_fin.addItems(fase_list)
			self.comboBox_fas_fin.setEditText(self.DATA_LIST[self.rec_num].fase_finale)

		except:
			pass



	#buttons functions
	def on_pushButton_sort_pressed(self):
		dlg = SortPanelMain(self)
		dlg.insertItems(self.SORT_ITEMS)
		dlg.exec_()

		items,order_type = dlg.ITEMS, dlg.TYPE_ORDER

		items_converted = []
		for i in items:
			items_converted.append(self.CONVERSION_DICT[i])

		self.SORT_MODE = order_type
		self.empty_fields()

		id_list = []
		for i in self.DATA_LIST:
			id_list.append(eval("i." + self.ID_TABLE))
		self.DATA_LIST = []

		temp_data_list = self.DB_MANAGER.query_sort(id_list, items_converted, order_type, self.MAPPER_TABLE_CLASS, self.ID_TABLE)

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
		self.label_sort.setText(self.SORTED_ITEMS["o"])
		self.set_rec_counter(len(self.DATA_LIST), self.REC_CORR+1)
		self.fill_fields()

	def add_value_to_categoria(self):
		if str(self.comboBox_sigla_struttura.currentText()) == 'Aggiungi un valore...':
			self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)


	def on_pushButton_new_rec_pressed(self):
		
		#set the GUI for a new record
		if self.BROWSE_STATUS != "n":
			self.BROWSE_STATUS = "n"
			self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
			self.empty_fields()
			self.label_sort.setText(self.SORTED_ITEMS["n"])

			self.setComboBoxEditable(["self.comboBox_sito"],1)
			self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)
			self.setComboBoxEnable(["self.comboBox_sito"],True)
			self.setComboBoxEnable(["self.comboBox_sigla_struttura"],True)
			self.setComboBoxEnable(["self.numero_struttura"],True)

			self.set_rec_counter('', '')

			self.enable_button(0)


	def on_pushButton_save_pressed(self):
		#save record
		if self.BROWSE_STATUS == "b":
			if self.records_equal_check() == 1:
				self.update_if(QMessageBox.warning(self,'ATTENZIONE',"Il record e' stato modificato. Vuoi salvare le modifiche?", QMessageBox.Cancel,1))
				self.SORT_STATUS = "n"
				self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
				self.enable_button(1)
			else:
				QMessageBox.warning(self, "ATTENZIONE", u"Non è stata realizzata alcuna modifica.",  QMessageBox.Ok)
		else:
			if self.data_error_check() == 0:
				test_insert = self.insert_new_rec()
				if test_insert == 1:
					self.empty_fields()
					self.SORT_STATUS = "n"
					self.label_sort.setText(self.SORTED_ITEMS[self.SORT_STATUS])
					self.charge_records()
					self.charge_list()
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])
					self.REC_TOT, self.REC_CORR = len(self.DATA_LIST), len(self.DATA_LIST)-1
					self.set_rec_counter(self.REC_TOT, self.REC_CORR+1)

				self.setComboBoxEditable(["self.comboBox_sito"],1)
				self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)
				self.setComboBoxEnable(["self.comboBox_sito"],"False")
				self.setComboBoxEnable(["self.comboBox_sigla_struttura"],"False")
				self.setComboBoxEnable(["self.numero_struttura"],"False")
	
				self.fill_fields(self.REC_CORR)
				self.enable_button(1)
				

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

		#TableWidget
		##Materiali_impiegati
		materiali_impiegati = self.table2dict("self.tableWidget_materiali_impiegati")
		##Elementi_strutturali
		elementi_strutturali = self.table2dict("self.tableWidget_elementi_strutturali")
		##Rapporti_struttura
		rapporti_struttura = self.table2dict("self.tableWidget_rapporti")
		##Misurazioni
		misurazioni = self.table2dict("self.tableWidget_misurazioni")

		try:
			if self.comboBox_per_iniz.currentText() == "":
				per_iniz = None
			else:
				per_iniz = int(self.comboBox_per_iniz.currentText())

			if self.comboBox_fas_iniz.currentText() == "":
				fas_iniz = None
			else:
				fas_iniz = int(self.comboBox_fas_iniz.currentText())

			if self.comboBox_per_fin.currentText() == "":
				per_fin = None
			else:
				per_fin = int(self.comboBox_per_fin.currentText())

			if self.comboBox_fas_fin.currentText() == "":
				fas_fin = None
			else:
				fas_fin = int(self.comboBox_fas_fin.currentText())


			data = self.DB_MANAGER.insert_struttura_values(
			self.DB_MANAGER.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1, #0
			str(self.comboBox_sito.currentText()), 														#1 - Sito
			str(self.comboBox_sigla_struttura.currentText()), 											#2 - sigla_struttura
			int(self.numero_struttura.text()), 																#3 - numero_struttura
			str(self.comboBox_categoria_struttura.currentText()), 									#4 - categoria_struttura
			str(self.comboBox_tipologia_struttura.currentText()), 										#5 - tipologia_struttura
			str(self.comboBox_definizione_struttura.currentText()), 									#6 - definizione_struttura
			unicode(self.textEdit_descrizione_struttura.toPlainText()),									#7 - descrizione
			unicode(self.textEdit_interpretazione_struttura.toPlainText()),							#8 - interpretazione
			per_iniz,																									#9 - periodo iniziale
			fas_iniz,																									#10 - fase iniziale
			per_fin, 																									#11 - periodo finale iniziale
			fas_fin, 																									#12 - fase finale
			str(self.lineEdit_datazione_estesa.text()),														#13 - datazione estesa
			str(materiali_impiegati),																				#14 - materiali impiegati
			str(elementi_strutturali),																			#15 - elementi_strutturali
			str(rapporti_struttura),																				#16 - rapporti struttura
			str(misurazioni))																						#17 - misurazioni

			try:
				self.DB_MANAGER.insert_data_session(data)

			except Exception, e:
				e_str = str(e)
				if e_str.__contains__("Integrity"):
					msg = self.ID_TABLE + " gia' presente nel database"
				else:
					msg = e
				QMessageBox.warning(self, "Errore", "immisione 1 \n"+ str(msg),  QMessageBox.Ok)
		except Exception, e:
			QMessageBox.warning(self, "Errore", "Errore di immissione 2 \n"+str(e),  QMessageBox.Ok)

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
			self.setComboBoxEditable(["self.comboBox_sito"],1)
			self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)
			self.setComboBoxEnable(["self.comboBox_sito"],True)
			self.setComboBoxEnable(["self.comboBox_sigla_struttura"],True)
			self.setComboBoxEnable(["self.numero_struttura"],True)
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
			if self.numero_struttura.text() != "":
				numero_struttura = int(self.numero_struttura.text())
			else:
				numero_struttura = ""

			if self.comboBox_per_iniz.currentText() != "":
				periodo_iniziale = int(self.comboBox_per_iniz.currentText())
			else:
				periodo_iniziale = ""

			if self.comboBox_fas_iniz.currentText() != "":
				fase_iniziale = int(self.comboBox_fas_iniz.currentText())
			else:
				fase_iniziale = ""

			if self.comboBox_per_fin.currentText() != "":
				periodo_finale = int(self.comboBox_per_fin.currentText())
			else:
				periodo_finale = ""

			if self.comboBox_fas_fin.currentText() != "":
				fase_finale = int(self.comboBox_fas_fin.currentText())
			else:
				fase_finale = ""

			search_dict = {
			self.TABLE_FIELDS[0] : "'"+str(self.comboBox_sito.currentText())+"'",							#1 - Sito
			self.TABLE_FIELDS[1] : "'"+str(self.comboBox_sigla_struttura.currentText())+"'", 			#2 - Sigla struttura
			self.TABLE_FIELDS[2] : numero_struttura, 																#3 - numero struttura
			self.TABLE_FIELDS[3] : "'"+str(self.comboBox_categoria_struttura.currentText())+"'",		#4 - categoria struttura
			self.TABLE_FIELDS[4] : "'"+str(self.comboBox_tipologia_struttura.currentText())+"'", 		#5 - tipologia struttura
			self.TABLE_FIELDS[5] : "'"+str(self.comboBox_definizione_struttura.currentText())+"'", 	#6 - definizione struttura
			#self.TABLE_FIELDS[6] : str(self.textEdit_descrizione_struttura.toPlainText()),					#7 - descrizione struttura
			#self.TABLE_FIELDS[7] : str(self.textEdit_interpretazione_struttura.toPlainText()),				#8 - intepretazione struttura
			self.TABLE_FIELDS[8] : periodo_iniziale,																	#9 - periodo iniziale
			self.TABLE_FIELDS[9] : fase_iniziale,																		#10 - fase iniziale
			self.TABLE_FIELDS[10] : periodo_finale,																	#11 - periodo finale
			self.TABLE_FIELDS[11] : fase_finale,																		#12 - fase finale
			self.TABLE_FIELDS[12] : str(self.lineEdit_datazione_estesa.text())									#10 - datazione_estesa
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
					self.BROWSE_STATUS = "b"
					self.label_status.setText(self.STATUS_ITEMS[self.BROWSE_STATUS])

					self.setComboBoxEditable(["self.comboBox_sito"],0)
					self.setComboBoxEditable(["self.comboBox_sigla_struttura"],0)
					self.setComboBoxEnable(["self.comboBox_sito"],"True")
					self.setComboBoxEnable(["self.comboBox_sigla_struttura"],"True")
					self.setComboBoxEnable(["self.numero_struttura"],"True")

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
					self.setComboBoxEditable(["self.comboBox_sigla_struttura"],1)
					self.setComboBoxEnable(["self.comboBox_sito"],"False")
					self.setComboBoxEnable(["self.comboBox_sigla_struttura"],"False")
					self.setComboBoxEnable(["self.numero_struttura"],"False")

					QMessageBox.warning(self, "Messaggio", "%s %d %s" % strings,  QMessageBox.Ok)
		self.enable_button_search(1)

	def on_pushButton_pdf_exp_pressed(self):
		Struttura_pdf_sheet = generate_struttura_pdf() #deve essere importata la classe
		data_list = self.generate_list_pdf() #deve essere aggiunta la funzione
		Struttura_pdf_sheet.build_Struttura_sheets(data_list) #deve essere aggiunto il file per generare i pdf

	def generate_list_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			data_list.append([
			unicode(self.DATA_LIST[i].sito), 									#1 - Sito
			unicode(self.DATA_LIST[i].sigla_struttura),									#2 - Area
			int(self.DATA_LIST[i].numero_struttura),												#3 - US
			unicode(self.DATA_LIST[i].categoria_struttura),				#4 - definizione stratigrafica
			unicode(self.DATA_LIST[i].tipologia_struttura),						#5 - definizione intepretata
			unicode(self.DATA_LIST[i].definizione_struttura),							#6 - descrizione
			unicode(self.DATA_LIST[i].descrizione),						#7 - interpretazione
			unicode(self.DATA_LIST[i].interpretazione),						#7 - interpretazione
			unicode(self.DATA_LIST[i].periodo_iniziale),						#8 - periodo iniziale
			unicode(self.DATA_LIST[i].fase_iniziale),							#9 - fase iniziale
			unicode(self.DATA_LIST[i].periodo_finale),						#10 - periodo finale iniziale
			unicode(self.DATA_LIST[i].fase_finale), 							#11 - fase finale
			unicode(self.DATA_LIST[i].datazione_estesa),								#12 - scavato
			unicode(self.DATA_LIST[i].materiali_impiegati),									#13 - attivita
			unicode(self.DATA_LIST[i].elementi_strutturali),							#14 - anno scavo
			unicode(self.DATA_LIST[i].rapporti_struttura),					#15 - metodo
			unicode(self.DATA_LIST[i].misure_struttura)									#16 - inclusi
		])
		return data_list



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

		materiali_impiegati_row_count = self.tableWidget_materiali_impiegati.rowCount()
		elementi_strutturali_row_count = self.tableWidget_elementi_strutturali.rowCount()
		rapporti_struttura_row_count = self.tableWidget_rapporti.rowCount()
		misurazioni_row_count = self.tableWidget_misurazioni.rowCount()

		self.comboBox_sito.setEditText("") 								#1 - Sito
		self.comboBox_sigla_struttura.setEditText("")				#2 - sigla_struttura
		self.numero_struttura.clear()										#3 - numero_struttura
		self.comboBox_categoria_struttura.setEditText("") 			#4 - categoria_struttura
		self.comboBox_tipologia_struttura.setEditText("") 			#5 - tipologia_struttura
		self.comboBox_definizione_struttura.setEditText("") 		#6 - definizione_struttura
		self.textEdit_descrizione_struttura.clear()						#7 - descrizione
		self.textEdit_interpretazione_struttura.clear()					#8 - interpretazione
		self.comboBox_per_iniz.setEditText("")							#9 - periodo iniziale
		self.comboBox_fas_iniz.setEditText("")							#10 - fase iniziale
		self.comboBox_per_fin.setEditText("")							#11 - periodo finale iniziale
		self.comboBox_fas_fin.setEditText("")							#12 - fase finale
		self.lineEdit_datazione_estesa.clear()							#13 - datazione estesa

		for i in range(materiali_impiegati_row_count):
			self.tableWidget_materiali_impiegati.removeRow(0)
		self.insert_new_row("self.tableWidget_materiali_impiegati")#14 - materiali impiegati

		for i in range(elementi_strutturali_row_count):
			self.tableWidget_elementi_strutturali.removeRow(0)
		self.insert_new_row("self.tableWidget_elementi_strutturali")#15 - elementi_strutturali

		for i in range(rapporti_struttura_row_count):
			self.tableWidget_rapporti.removeRow(0)
		self.insert_new_row("self.tableWidget_rapporti")				#16 - rapporti struttura

		for i in range(misurazioni_row_count):
			self.tableWidget_misurazioni.removeRow(0)
		self.insert_new_row("self.tableWidget_misurazioni")			#17 - rapporti struttura

	def fill_fields(self, n=0):
		self.rec_num = n

		if str(self.DATA_LIST[self.rec_num].periodo_iniziale) == 'None':
			periodo_iniziale = ''
		else:
			periodo_iniziale = str(self.DATA_LIST[self.rec_num].periodo_iniziale)

		if str(self.DATA_LIST[self.rec_num].fase_iniziale) == 'None':
			fase_iniziale = ''
		else:
			fase_iniziale = str(self.DATA_LIST[self.rec_num].fase_iniziale)

		if str(self.DATA_LIST[self.rec_num].periodo_finale) == 'None':
			periodo_finale = ''
		else:
			periodo_finale = str(self.DATA_LIST[self.rec_num].periodo_finale)

		if str(self.DATA_LIST[self.rec_num].fase_finale) == 'None':
			fase_finale = ''
		else:
			fase_finale = str(self.DATA_LIST[self.rec_num].fase_finale)

		try:
			self.comboBox_sito.setEditText(self.DATA_LIST[self.rec_num].sito)																#1 - Sito
			self.comboBox_sigla_struttura.setEditText(str(self.DATA_LIST[self.rec_num].sigla_struttura)) 							#2 - Periodo
			self.numero_struttura.setText(str(self.DATA_LIST[self.rec_num].numero_struttura)) 										#3 - Fase
			self.comboBox_categoria_struttura.setEditText(str(self.DATA_LIST[self.rec_num].categoria_struttura))				#4 - Fase
			self.comboBox_tipologia_struttura.setEditText(str(self.DATA_LIST[self.rec_num].tipologia_struttura))					#5 - tipologia_struttura
			self.comboBox_definizione_struttura.setEditText(str(self.DATA_LIST[self.rec_num].definizione_struttura)) 			#6 - definizione_struttura
			unicode(self.textEdit_descrizione_struttura.setText(self.DATA_LIST[self.rec_num].descrizione))							#6 - descrizione
			unicode(self.textEdit_interpretazione_struttura.setText(self.DATA_LIST[self.rec_num].interpretazione))				#7 - interpretazione
			self.comboBox_per_iniz.setEditText(periodo_iniziale)																					#8 - periodo iniziale
			self.comboBox_fas_iniz.setEditText(fase_iniziale)																						#9 - fase iniziale
			self.comboBox_per_fin.setEditText(periodo_finale)																						#10 - periodo finale
			self.comboBox_fas_fin.setEditText(fase_finale)																							#11 - fase finale
			self.lineEdit_datazione_estesa.setText(str(self.DATA_LIST[self.rec_num].datazione_estesa))								#12 - datazione estesa
			self.tableInsertData("self.tableWidget_materiali_impiegati", self.DATA_LIST[self.rec_num].materiali_impiegati)			#13 - materiali impiegati
			self.tableInsertData("self.tableWidget_elementi_strutturali", self.DATA_LIST[self.rec_num].elementi_strutturali)		#14 - elementi struttura
			self.tableInsertData("self.tableWidget_rapporti", self.DATA_LIST[self.rec_num].rapporti_struttura)						#15 - rapporti struttura
			self.tableInsertData("self.tableWidget_misurazioni", self.DATA_LIST[self.rec_num].misure_struttura)					#16 - misure struttura
		except Exception, e:
			QMessageBox.warning(self, "Errore Fill Fields", "Problema di riempimento campi" + str(e),  QMessageBox.Ok)

	def set_rec_counter(self, t, c):
		self.rec_tot = t
		self.rec_corr = c
		self.label_rec_tot.setText(str(self.rec_tot))
		self.label_rec_corrente.setText(str(self.rec_corr))

	def set_LIST_REC_TEMP(self):
		#data

		if self.numero_struttura.text() != "":
			numero_struttura = self.numero_struttura.text()
		else:
			numero_struttura = 'None'

		if self.comboBox_per_iniz.currentText() != "":
			periodo_iniziale = self.comboBox_per_iniz.currentText()
		else:
			periodo_iniziale = 'None'

		if self.comboBox_fas_iniz.currentText() != "":
			fase_iniziale = self.comboBox_fas_iniz.currentText()
		else:
			fase_iniziale = 'None'

		if self.comboBox_per_fin.currentText() != "":
			periodo_finale = self.comboBox_per_fin.currentText()
		else:
			periodo_finale = 'None'

		if self.comboBox_fas_fin.currentText() != "":
			fase_finale = self.comboBox_fas_fin.currentText()
		else:
			fase_finale = 'None'
			
		##Campioni
		materiali_impiegati = self.table2dict("self.tableWidget_materiali_impiegati")
		##Elementi_strutturali
		elementi_strutturali = self.table2dict("self.tableWidget_elementi_strutturali")
		##Rapporti_struttura
		rapporti_struttura = self.table2dict("self.tableWidget_rapporti")
		##Misurazioni
		misurazioni = self.table2dict("self.tableWidget_misurazioni")

		self.DATA_LIST_REC_TEMP = [
		str(self.comboBox_sito.currentText()), 												#1 - Sito
		str(self.comboBox_sigla_struttura.currentText()), 									#2 - sigla
		str(numero_struttura), 																		#3 - numero_struttura
		str(self.comboBox_categoria_struttura.currentText()),							#3 - numero_struttura
		str(self.comboBox_tipologia_struttura.currentText()), 								#3 - numero_struttura
		str(self.comboBox_definizione_struttura.currentText()),							#4 - cron iniziale
		str(self.textEdit_descrizione_struttura.toPlainText().toLatin1()),					#6 - descrizioene
		str(self.textEdit_interpretazione_struttura.toPlainText().toLatin1()),			#6 - descrizioene
		str(periodo_iniziale),																			#6 - descrizioene
		str(fase_iniziale),																				#6 - descrizioene
		str(periodo_finale),																			#6 - descrizioene
		str(fase_finale),																				#6 - descrizioene
		str(self.lineEdit_datazione_estesa.text()),												#7- cron estesa
		str(materiali_impiegati),
		str(elementi_strutturali),
		str(rapporti_struttura),
		str(misurazioni)
		]

	def rec_toupdate(self):
		rec_to_update = self.UTILITY.pos_none_in_list(self.DATA_LIST_REC_TEMP)
		return rec_to_update

	def set_LIST_REC_CORR(self):
		self.DATA_LIST_REC_CORR = []
		for i in self.TABLE_FIELDS:
			self.DATA_LIST_REC_CORR.append(eval("str(self.DATA_LIST[self.REC_CORR]." + i + ")"))

	def records_equal_check(self):
		self.set_LIST_REC_TEMP()
		self.set_LIST_REC_CORR()
		if self.DATA_LIST_REC_CORR == self.DATA_LIST_REC_TEMP:
			return 0
		else:
			return 1

	def tableInsertData(self, t, d):
		"""Set the value into alls Grid"""
		self.table_name = t
		self.data_list = eval(d)
		self.data_list.sort()

		#column table count
		table_col_count_cmd = ("%s.columnCount()") % (self.table_name)
		table_col_count = eval(table_col_count_cmd)

		#clear table
		table_clear_cmd = ("%s.clearContents()") % (self.table_name)
		eval(table_clear_cmd)

		for i in range(table_col_count):
			table_rem_row_cmd = ("%s.removeRow(%d)") % (self.table_name, i)
			eval(table_rem_row_cmd)

		#for i in range(len(self.data_list)):
			#self.insert_new_row(self.table_name)

		for row in range(len(self.data_list)):
			cmd = ('%s.insertRow(%s)') % (self.table_name, row)
			eval(cmd)
			for col in range(len(self.data_list[row])):
				#item = self.comboBox_sito.setEditText(self.data_list[0][col]
				item = QTableWidgetItem(self.data_list[row][col])
				exec_str = ('%s.setItem(%d,%d,item)') % (self.table_name,row,col)
				eval(exec_str)

	#insert new row into tableWidget
	def on_pushButton_insert_row_rapporti_pressed(self):
		self.insert_new_row('self.tableWidget_rapporti')

	def on_pushButton_insert_row_materiali_pressed(self):
		self.insert_new_row('self.tableWidget_materiali_impiegati')

	def on_pushButton_insert_row_elementi_pressed(self):
		self.insert_new_row('self.tableWidget_elementi_strutturali')

	def on_pushButton_insert_row_misurazioni_pressed(self):
		self.insert_new_row('self.tableWidget_misurazioni')

	def insert_new_row(self, table_name):
		"""insert new row into a table based on table_name"""
		cmd = table_name+".insertRow(0)"
		eval(cmd)

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
