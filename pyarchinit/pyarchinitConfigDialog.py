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
from sqlalchemy.orm import sessionmaker
from Ui_pyarchinitConfig import Ui_Dialog_Config
from Ui_pyarchinitConfig import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from pyarchinit_db_manager import *
from pyarchinit_db_mapper import *
from pyarchinit_db_structure import *

from pyarchinit_OS_utility import *

#from PyQt4 import QtCore, QtGui
import sys, os

class pyArchInitDialog_Config(QDialog, Ui_Dialog_Config):
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']

	PARAMS_DICT={'SERVER':'',
				'HOST': '',
				'DATABASE':'',
				'PASSWORD':'',
				'PORT':'',
				'USER':'',
				'THUMB_PATH':''}


	def __init__(self, parent=None, db=None):
		QDialog.__init__(self, parent)
		# Set up the user interface from Designer.
		self.setupUi(self)
		self.load_dict()
		self.charge_data()

		self.connect(self.comboBox_Database, SIGNAL("editTextChanged (const QString&)"), self.set_db_name)


	def set_db_name(self):
		if str(self.comboBox_Database.currentText()) == 'postgres':
			self.lineEdit_DBname.setText("pyarchinit")
		if str(self.comboBox_Database.currentText()) == 'sqlite':
			self.lineEdit_DBname.setText("pyarchinit_db.sqlite")

	def load_dict(self):
		path_rel = os.path.join(os.sep, str(self.HOME), 'pyarchinit_DB_folder', 'config.cfg')
		conf = open(path_rel, "r")
		data = conf.read()
		self.PARAMS_DICT = eval(data)

	def save_dict(self):
		#save data into config.cfg file
		path_rel = os.path.join(os.sep, str(self.HOME), 'pyarchinit_DB_folder', 'config.cfg')
		f = open(path_rel, "w")
		f.write(str(self.PARAMS_DICT))
		f.close()
##
##	def on_pushButton_exp_directories_pressed(self):
##		module_path_rel = os.path.join(os.sep, '.qgis', 'python','plugins', 'pyarchinit', 'modules', 'utility')
##		module_path = ('%s%s') % (home, module_path_rel)
##
##		home_DB_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_DB_folder')
##
##		config_copy_from_path_rel = os.path.join(os.sep, 'DBfiles', 'config.cfg')
##		config_copy_from_path =  ('%s%s') % (module_path, config_copy_from_path_rel)
##		config_copy_to_path = ('%s%s%s') % (home_DB_path, os.sep, 'config.cfg')
##
##		db_copy_from_path_rel = os.path.join(os.sep, 'DBfiles', 'pyarchinit_db.sqlite')
##		db_copy_from_path = ('%s%s') % (module_path, db_copy_from_path_rel)
##		db_copy_to_path = ('%s%s%s') % (home_DB_path, os.sep, 'pyarchinit_db.sqlite')
##	
##		OS_utility = pyarchinit_OS_Utility()
##
##		OS_utility.create_dir(str(home_DB_path))

	def on_pushButton_save_pressed(self):
		self.PARAMS_DICT['SERVER'] = str(self.comboBox_Database.currentText())
		self.PARAMS_DICT['HOST'] =  str(self.lineEdit_Host.text())
		self.PARAMS_DICT['DATABASE'] = str(self.lineEdit_DBname.text())
		self.PARAMS_DICT['PASSWORD'] = str(self.lineEdit_Password.text())
		self.PARAMS_DICT['PORT'] = str(self.lineEdit_Port.text())
		self.PARAMS_DICT['USER'] = str(self.lineEdit_User.text()) 
		self.PARAMS_DICT['THUMB_PATH'] = str(self.lineEdit_Thumb_path.text())
		self.save_dict()
		self.try_connection()


	def on_pushButton_crea_database_pressed(self):
		import time
		try:
			db = os.popen("createdb -U postgres -p %s -h localhost -E UTF8  -T %s -e %s" % (str(self.lineEdit_port_db.text()), str(self.lineEdit_template_postgis.text()), str(self.lineEdit_dbname.text())))
			barra = self.pyarchinit_progressBar_db
			#barra.show()
			barra.setMinimum(0)
			barra.setMaximum(9)
			for a in range(10):
				time.sleep(1)
				barra.setValue(a)
			QMessageBox.warning(self, "ok","Installazione avvenuta con successo",  QMessageBox.Ok)
		except Exception,e:
			QMessageBox.warning(self, "opss", u"qualcosa non va" + str(e),  QMessageBox.Ok)


	def on_pushButton_crea_layer_pressed(self):
		from pyarchinit_OS_utility import *
		import time

		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		try:
			module_path_rel = os.path.join(os.sep, '.qgis2', 'python','plugins', 'pyarchinit', 'modules', 'utility','DBfiles', 'pyarchinit_postgis15_empty.dump')
			module_path = ('%s%s') % (home, module_path_rel)
			postgis15 = os.popen ("pg_restore --host localhost --port %s --username postgres --dbname %s --role postgres --no-password  --verbose %s" % (str(self.lineEdit_port_db.text()), str(self.lineEdit_dbname.text()), str(module_path)))
			barra2 = self.pyarchinit_progressBar_template
			barra2.setMinimum(0)
			barra2.setMaximum(9)
			for a in range(10):
				time.sleep(1)
				barra2.setValue(a)
			QMessageBox.warning(self, "ok","Installazione avvenuta con successo",  QMessageBox.Ok)
		except Exception,e:
			QMessageBox.warning(self, "opss", u"qualcosa non va" + str(e),  QMessageBox.Ok)
			
	
	def on_pushButton_crea_layer_2_pressed(self):
		from pyarchinit_OS_utility import *
		import time

		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		try:
			module_path_rel = os.path.join(os.sep, '.qgis2', 'python','plugins', 'pyarchinit', 'modules', 'utility','DBfiles', 'pyarchinit_postgis20_empty.dump')
			module_path = ('%s%s') % (home, module_path_rel)
			postgis15 = os.popen ("pg_restore --host localhost --port %s --username postgres --dbname %s --role postgres --no-password  --verbose %s" % (str(self.lineEdit_port_db.text()), str(self.lineEdit_dbname.text()), str(module_path)))
			barra2 = self.pyarchinit_progressBar_template
			barra2.setMinimum(0)
			barra2.setMaximum(9)
			for a in range(10):
				time.sleep(1)
				barra2.setValue(a)
			QMessageBox.warning(self, "ok","Installazione avvenuta con successo",  QMessageBox.Ok)
		except Exception,e:
			QMessageBox.warning(self, "opss", u"qualcosa non va" + str(e),  QMessageBox.Ok)

	def on_pushButton_crea_db_sqlite_pressed(self):
		try:
			from pyarchinit_conn_strings import *
			conn = Connection()
			conn_str = conn.conn_str()
			from  pyarchinit_db_manager import *
			self.DB_MANAGER = Pyarchinit_db_management(conn_str)
			self.DB_MANAGER.connection()
			self.DB_MANAGER.execute_sql_create_spatialite_db()
		except:
			QMessageBox.warning(self, "Alert", "L'installazione e' fallita. Riavvia Qgis. Se l'errore persiste verifica che i layer non siano gia' installati oppure sia stia usando un db Postgres",  QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Alert", "L'installazione ha avuto successo!",  QMessageBox.Ok)

	def try_connection(self):
		from pyarchinit_conn_strings import *
		conn = Connection()
		conn_str = conn.conn_str()

		from  pyarchinit_db_manager import *
		self.DB_MANAGER = Pyarchinit_db_management(conn_str)  #sqlite:///\Users\Windows\pyarchinit_DB_folder\pyarchinit_db.sqlite 

		test = self.DB_MANAGER.connection()
		test = str(test)
		if test == "":
			QMessageBox.warning(self, "Messaggio", "Connessione avvenuta con successo",  QMessageBox.Ok)
		elif test.find("create_engine") != -1:
			QMessageBox.warning(self, "Alert", "Verifica i parametri di connessione. <br> Se sono corretti RIAVVIA QGIS" ,  QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Alert", "Errore di connessione: <br>" + str(test) ,  QMessageBox.Ok)

	def charge_data(self):
		#load data from config.cfg file
		print self.PARAMS_DICT
		self.comboBox_Database.setEditText(self.PARAMS_DICT['SERVER'])
		self.lineEdit_Host.setText(self.PARAMS_DICT['HOST'])
		self.lineEdit_DBname.setText(self.PARAMS_DICT['DATABASE'])
		self.lineEdit_Password.setText(self.PARAMS_DICT['PASSWORD'])
		self.lineEdit_Port.setText(self.PARAMS_DICT['PORT'])
		self.lineEdit_User.setText(self.PARAMS_DICT['USER'])
		self.lineEdit_Thumb_path.setText(self.PARAMS_DICT['THUMB_PATH'])

	def on_pushButton_import_pressed(self):
		id_table_class_mapper_conv_dict = {
		'US' : 'id_us',
		'UT':'id_ut',
		'SITE':'id_sito',
		'PERIODIZZAZIONE':'id_perfas',
		'INVENTARIO_MATERIALI':'id_invmat',
		'STRUTTURA':'id_struttura',
		'TAFONOMIA':'id_tafonomia',
		'SCHEDAIND':'id_scheda_ind',
		'CAMPIONE':'id_campione',
		'DOCUMENTAZIONE':'id_documentazione'
		}

		#creazione del cursore di lettura
		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		####RICAVA I DATI IN LETTURA PER LA CONNESSIONE DALLA GUI
		conn_str_dict_read = {
								"server": str(self.comboBox_server_read.currentText()),
								"user": str(self.lineEdit_username_read.text()),
								"password" : str(self.lineEdit_pass_read.text()),
								"host": str(self.lineEdit_host_read.text()),
								"port": str(self.lineEdit_port_read.text()),
								"db_name": str(self.lineEdit_database_read.text())
								}

		####CREA LA STRINGA DI CONNESSIONE IN LETTURA
		
		if conn_str_dict_read["server"] == 'postgres':
			try:
				conn_str_read = "%s://%s:%s@%s:%s/%s%s?charset=utf8" % ("postgresql", conn_str_dict_read["user"],conn_str_dict_read["password"], conn_str_dict_read["host"], conn_str_dict_read["port"], conn_str_dict_read["db_name"], "?sslmode=allow")
			except:
				conn_str_read = "%s://%s:%s@%s:%d/%s" % ("postgresql", conn_str_dict_read["user"],conn_str_dict_read["password"], conn_str_dict_read["host"], conn_str_dict_read["port"], conn_str_dict_read["db_name"])

		elif conn_str_dict_read["server"] == 'sqlite':
			sqlite_DB_path = ('%s%s%s') % (home, os.sep, "pyarchinit_DB_folder") #"C:\\Users\\Windows\\Dropbox\\pyarchinit_san_marco\\" fare modifiche anche in pyarchinit_pyqgis
			
			dbname_abs = sqlite_DB_path + os.sep + conn_str_dict_read["db_name"]

			conn_str_read = "%s:///%s" % (conn_str_dict_read["server"], dbname_abs)

			QMessageBox.warning(self, "Alert", str(conn_str_dict_read["db_name"]),  QMessageBox.Ok)

		####SI CONNETTE AL DATABASE
		self.DB_MANAGER_read = Pyarchinit_db_management(conn_str_read)
		test =self.DB_MANAGER_read.connection()
		test = str(test)
		if test == "":
			QMessageBox.warning(self, "Messaggio", "Connessione avvenuta con successo",  QMessageBox.Ok)
		elif test.find("create_engine") != -1:
			QMessageBox.warning(self, "Alert", "Verifica i parametri di connessione. <br> Se sono corretti RIAVVIA QGIS" ,  QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Alert", "Errore di connessione: <br>" + str(test) ,  QMessageBox.Ok)

		####LEGGE I RECORD IN BASE AL PARAMETRO CAMPO=VALORE
		search_dict = {
			self.lineEdit_field_read.text() : "'"+str(self.lineEdit_value_read.text())+"'"
			}

		mapper_class_read = str(self.comboBox_mapper_read.currentText())
		res_read =self.DB_MANAGER_read.query_bool(search_dict,mapper_class_read)

		####INSERISCE I DATI DA UPLOADARE DENTRO ALLA LISTA DATA_LIST_TOIMP
		data_list_toimp = []

		for i in res_read:
			data_list_toimp.append(i)

		#creazione del cursore di scrittura

		####RICAVA I DATI IN LETTURA PER LA CONNESSIONE DALLA GUI
		conn_str_dict_write = {
										"server": str(self.comboBox_server_write.currentText()),
										"user": str(self.lineEdit_username_write.text()),
										"password" : str(self.lineEdit_pass_write.text()),
										"host": str(self.lineEdit_host_write.text()),
										"port": str(self.lineEdit_port_write.text()),
										"db_name": str(self.lineEdit_database_write.text())
										}

		####CREA LA STRINGA DI CONNESSIONE IN LETTURA
		
		if conn_str_dict_write["server"] == 'postgres':
			try:
				conn_str_write = "%s://%s:%s@%s:%s/%s%s?charset=utf8" % ("postgresql", conn_str_dict_writed["user"],conn_str_dict_write["password"], conn_str_dict_write["host"], conn_str_dict_write["port"], conn_str_dict_write["db_name"], "?sslmode=allow")
			except:
				conn_str_write = "%s://%s:%s@%s:%d/%s" % ("postgresql", conn_str_dict_write["user"],conn_str_dict_write["password"], conn_str_dict_write["host"], conn_str_dict_write["port"], conn_str_dict_write["db_name"])

		elif conn_str_dict_write["server"] == 'sqlite':
			sqlite_DB_path = ('%s%s%s') % (home, os.sep, "pyarchinit_DB_folder") #"C:\\Users\\Windows\\Dropbox\\pyarchinit_san_marco\\" fare modifiche anche in pyarchinit_pyqgis
			
			dbname_abs = sqlite_DB_path + os.sep + conn_str_dict_write["db_name"]

			conn_str_write = "%s:///%s" % (conn_str_dict_write["server"], dbname_abs)

			QMessageBox.warning(self, "Alert", str(conn_str_dict_write["db_name"]),  QMessageBox.Ok)

		####SI CONNETTE AL DATABASE
		self.DB_MANAGER_write = Pyarchinit_db_management(conn_str_write)
		test =self.DB_MANAGER_write.connection()
		test = str(test)
		if test == "":
			QMessageBox.warning(self, "Messaggio", "Connessione avvenuta con successo",  QMessageBox.Ok)
		elif test.find("create_engine") != -1:
			QMessageBox.warning(self, "Alert", "Verifica i parametri di connessione. <br> Se sono corretti RIAVVIA QGIS" ,  QMessageBox.Ok)
		else:
			QMessageBox.warning(self, "Alert", "Errore di connessione: <br>" + str(test) ,  QMessageBox.Ok)

		####inserisce i dati dentro al database
		data = self.DB_MANAGER_write.insert_values(
		self.DB_MANAGER_write.max_num_id(self.MAPPER_TABLE_CLASS, self.ID_TABLE)+1,
		unicode(self.comboBox_sito_doc.currentText()), 						#1 - Sito
		unicode(self.lineEdit_nome_doc.text()),									#2 - Nome Documentazione
		unicode(self.lineEdit_data_doc.text()),										#3 - Data
		unicode(self.comboBox_tipo_doc.currentText()),						#4 - Tipo Documentazione
		unicode(self.comboBox_sorgente_doc.currentText()),					#5 - Sorgente
		unicode(self.comboBox_scala_doc.currentText()),						#6 - Scala
		unicode(self.lineEdit_disegnatore_doc.text()),								#7 - Disegnatore
		unicode(self.textEdit_note_doc.toPlainText()))							#8 - Note





if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	ui = pyArchInitDialog_Config()
	ui.show()
	sys.exit(app.exec_())