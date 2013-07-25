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

from pyarchinit_pdf_exp_ui import Ui_Dialog_pdf_exp
from pyarchinit_pdf_exp_ui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from  pyarchinit_utility import *
from  pyarchinit_db_manager import *
from  pyarchinit_OS_utility import pyarchinit_OS_Utility

from  pyarchinit_exp_USsheet_pdf import *
from  pyarchinit_exp_Periodizzazionesheet_pdf import *
from  pyarchinit_exp_Strutturasheet_pdf import *
from  pyarchinit_exp_Findssheet_pdf import *

#from PyQt4 import QtCore, QtGui
import sys, os


class pyarchinit_pdf_export(QDialog, Ui_Dialog_pdf_exp):
	UTILITY = Utility()
	OS_UTILITY = pyarchinit_OS_Utility()
	DB_MANAGER = ""
	HOME = ""
	DATA_LIST = []

##	if os.name == 'posix':
##		HOME = os.environ['HOME']
##	elif os.name == 'nt':
##		HOME = os.environ['HOMEPATH']
##
##	PARAMS_DICT={'SERVER':'',
##				'HOST': '',
##				'DATABASE':'',
##				'PASSWORD':'',
##				'PORT':'',
##				'USER':'',
##				'THUMB_PATH':''}


	def __init__(self, parent=None, db=None):
		QDialog.__init__(self, parent)
		# Set up the user interface from Designer.
		self.setupUi(self)

		try:
			self.connect()
		except:
			pass
		self.charge_list()
		self.set_home_path()
		#self.load_dict()
		#self.charge_data()

	def connect(self):
		from pyarchinit_conn_strings import *

		conn = Connection()
		conn_str = conn.conn_str()
		try:
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
		except Exception, e:
			e = str(e)
			if e.find("no such table"):
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br><br> %s. E' NECESSARIO RIAVVIARE QGIS" % (str(e)),  QMessageBox.Ok)
			else:
				QMessageBox.warning(self, "Alert", "La connessione e' fallita <br> Errore: <br>" + str(e) ,  QMessageBox.Ok)

	def charge_list(self):
		#lista sito
		sito_vl = self.UTILITY.tup_2_list_III(self.DB_MANAGER.group_by('site_table', 'sito', 'SITE'))
		try:
			sito_vl.remove('')
		except:
			pass

		self.comboBox_sito.clear()

		sito_vl.sort()
		self.comboBox_sito.addItems(sito_vl)

	def set_home_path(self):
		if os.name == 'posix':
			self.HOME = os.environ['HOME']
		elif os.name == 'nt':
			self.HOME = os.environ['HOMEPATH']

		
	def on_pushButton_exp_pdf_pressed(self):
		sito = str(self.comboBox_sito.currentText())

		#Esportazione della Scheda US
		if self.checkBox_US.isChecked() == True:

			us_res = self.db_search_DB('US','sito', sito)

			if bool(us_res) == True:
				id_list = []
				for i in range(len(us_res)):
					id_list.append(us_res[i].id_us)
					
				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['area', 'us'], 'asc', 'US', 'id_us')
				for i in temp_data_list:
					self.DATA_LIST.append(i)
				
				US_pdf_sheet = generate_US_pdf()
				data_list = self.generate_list_US_pdf()
				US_pdf_sheet.build_US_sheets(data_list)

			self.DATA_LIST = []

		if self.checkBox_periodo.isChecked() == True:
			
			periodizzazione_res = self.db_search_DB('PERIODIZZAZIONE','sito', sito)

			if bool(periodizzazione_res) == True:
				id_list = []
				for i in range(len(periodizzazione_res)):
					id_list.append(periodizzazione_res[i].id_perfas)

				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['cont_per'], 'asc', 'PERIODIZZAZIONE', 'id_perfas')

				for i in temp_data_list:
					self.DATA_LIST.append(i)
			
				Periodizzazione_pdf_sheet = generate_Periodizzazione_pdf() #deve essere importata la classe
				data_list = self.generate_list_periodizzazione_pdf() #deve essere aggiunta la funzione
				Periodizzazione_pdf_sheet.build_Periodizzazione_sheets(data_list) #deve essere aggiunto il file per generare i pdf

			self.DATA_LIST = []

		if self.checkBox_struttura.isChecked() == True:
			struttura_res = self.db_search_DB('STRUTTURA','sito', sito)

			if bool(struttura_res) == True:
				id_list = []
				for i in range(len(struttura_res)):
					id_list.append(struttura_res[i].id_struttura)

				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['sigla_struttura', 'numero_struttura'], 'asc', 'STRUTTURA', 'id_struttura')

				for i in temp_data_list:
					self.DATA_LIST.append(i)

				Struttura_pdf_sheet = generate_struttura_pdf() #deve essere importata la classe
				data_list = self.generate_list_struttura_pdf() #deve essere aggiunta la funzione
				Struttura_pdf_sheet.build_Struttura_sheets(data_list) #deve essere aggiunto il file per generare i pdf

			self.DATA_LIST = []

		if self.checkBox_reperti.isChecked() == True:
			reperti_res = self.db_search_DB('INVENTARIO_MATERIALI','sito', sito)

			if bool(reperti_res) == True:
				id_list = []
				for i in range(len(reperti_res)):
					id_list.append(reperti_res[i].id_invmat)

				temp_data_list = self.DB_MANAGER.query_sort(id_list, ['numero_inventario'], 'asc', 'INVENTARIO_MATERIALI', 'id_invmat')

				for i in temp_data_list:
					self.DATA_LIST.append(i)

			Finds_pdf_sheet = generate_reperti_pdf()
			data_list = self.generate_list_reperti_pdf()
			Finds_pdf_sheet.build_Finds_sheets(data_list)


			self.DATA_LIST = []

	def db_search_DB(self, table_class, field, value):
		self.table_class = table_class
		self.field = field
		self.value = value

		search_dict = {self.field : "'"+str(self.value)+"'"}

		u = Utility()
		search_dict = u.remove_empty_items_fr_dict(search_dict)

		res = self.DB_MANAGER.query_bool(search_dict, self.table_class)

		return res

	def generate_list_US_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			#assegnazione valori di quota mn e max
			sito =  unicode(self.DATA_LIST[i].sito)
			area = unicode(self.DATA_LIST[i].area)
			us = unicode(self.DATA_LIST[i].us)

			res = self.DB_MANAGER.select_quote_from_db_sql(sito, area, us)
			quote = []

			for sing_us in res:
				sing_quota_value = str(sing_us[5])
				if sing_quota_value[0] == '-':
					sing_quota_value = sing_quota_value[:7]
				else:
					sing_quota_value = sing_quota_value[:6]

				sing_quota = [sing_quota_value, sing_us[4]]
				quote.append(sing_quota)
			quote.sort()

			if bool(quote) == True:
				quota_min = '%s %s' % (quote[0][0], quote[0][1])
				quota_max = '%s %s' % (quote[-1][0], quote[-1][1])
			else:
				quota_min = "Non inserita su GIS"
				quota_max = "Non inserita su GIS"

			#assegnazione numero di pianta
			resus = self.DB_MANAGER.select_us_from_db_sql(sito, area, us, "2")
			elenco_record = []
			for us in resus:
				elenco_record.append(us)

			if bool(elenco_record) == True:
				sing_rec = elenco_record[0]
				elenco_piante = sing_rec[7]
				if elenco_piante != None:
					piante = elenco_piante
				else:
					piante = "US disegnata su base GIS"
			else:
				piante = "US disegnata su base GIS"

			data_list.append([
			unicode(self.DATA_LIST[i].sito), 									#1 - Sito
			unicode(self.DATA_LIST[i].area),									#2 - Area
			int(self.DATA_LIST[i].us),												#3 - US
			unicode(self.DATA_LIST[i].d_stratigrafica),						#4 - definizione stratigrafica
			unicode(self.DATA_LIST[i].d_interpretativa),						#5 - definizione intepretata
			unicode(self.DATA_LIST[i].descrizione),							#6 - descrizione
			unicode(self.DATA_LIST[i].interpretazione),						#7 - interpretazione
			unicode(self.DATA_LIST[i].periodo_iniziale),						#8 - periodo iniziale
			unicode(self.DATA_LIST[i].fase_iniziale),							#9 - fase iniziale
			unicode(self.DATA_LIST[i].periodo_finale),						#10 - periodo finale iniziale
			unicode(self.DATA_LIST[i].fase_finale), 							#11 - fase finale
			unicode(self.DATA_LIST[i].scavato),								#12 - scavato
			unicode(self.DATA_LIST[i].attivita),									#13 - attivita
			unicode(self.DATA_LIST[i].anno_scavo),							#14 - anno scavo
			unicode(self.DATA_LIST[i].metodo_di_scavo),					#15 - metodo
			unicode(self.DATA_LIST[i].inclusi),									#16 - inclusi
			unicode(self.DATA_LIST[i].campioni),								#17 - campioni
			unicode(self.DATA_LIST[i].rapporti),								#18 - rapporti
			unicode(self.DATA_LIST[i].data_schedatura),					#19 - data schedatura
			unicode(self.DATA_LIST[i].schedatore),							#20 - schedatore
			unicode(self.DATA_LIST[i].formazione),							#21 - formazione
			unicode(self.DATA_LIST[i].stato_di_conservazione),			#22 - conservazione
			unicode(self.DATA_LIST[i].colore),									#23 - colore
			unicode(self.DATA_LIST[i].consistenza),							#24 - consistenza
			unicode(self.DATA_LIST[i].struttura),								#25 - struttura
			unicode(quota_min),														#26 - quota_min
			unicode(quota_max),													#27 - quota_max
			unicode(piante),															#28 - piante
			unicode(self.DATA_LIST[i].documentazione)						#29 - documentazione
		])
		return data_list


	def generate_list_periodizzazione_pdf(self):
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


	def generate_list_struttura_pdf(self):
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


	def generate_list_reperti_pdf(self):
		data_list = []
		for i in range(len(self.DATA_LIST)):
			data_list.append([
			str(self.DATA_LIST[i].id_invmat), 							#1 - id_invmat
			unicode(self.DATA_LIST[i].sito),								#2 - sito
			int(self.DATA_LIST[i].numero_inventario),				#3 - numero_inventario
			unicode(self.DATA_LIST[i].tipo_reperto),					#4 - tipo_reperto
			unicode(self.DATA_LIST[i].criterio_schedatura),			#5 - criterio_schedatura
			unicode(self.DATA_LIST[i].definizione),					#6 - definizione
			unicode(self.DATA_LIST[i].descrizione),					#7 - descrizione
			unicode(self.DATA_LIST[i].area),							#8 - area
			unicode(self.DATA_LIST[i].us),								#9 - us
			unicode(self.DATA_LIST[i].lavato),							#10 - lavato
			unicode(self.DATA_LIST[i].nr_cassa), 						#11 - nr_cassa
			unicode(self.DATA_LIST[i].luogo_conservazione),		#12 - luogo_conservazione
			unicode(self.DATA_LIST[i].stato_conservazione),		#13 - stato_conservazione
			unicode(self.DATA_LIST[i].datazione_reperto),			#14 - datazione_reperto
			unicode(self.DATA_LIST[i].elementi_reperto),			#15 - elementi_reperto
			unicode(self.DATA_LIST[i].misurazioni),					#16 - misurazioni
			unicode(self.DATA_LIST[i].rif_biblio),						#17 - rif_biblio
			unicode(self.DATA_LIST[i].tecnologie),						#18 - misurazioni
			unicode(self.DATA_LIST[i].tipo),								#19 - tipo
			unicode(self.DATA_LIST[i].corpo_ceramico),				#20 - corpo_ceramico
			unicode(self.DATA_LIST[i].rivestimento)					#21- rivestimento
		])
		return data_list


if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	ui = pyarchinit_pdf_export()
	ui.show()
	sys.exit(app.exec_())