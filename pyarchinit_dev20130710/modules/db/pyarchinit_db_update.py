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
from sqlalchemy import *
from pyarchinit_conn_strings import *

class DB_update:

	# connection string postgres"
	internal_connection = Connection()

	# create engine and metadata

	engine = create_engine(internal_connection.conn_str(), echo=False)
	metadata = MetaData(engine)
	
	def update_table(self):
		table = Table("site_table", self.metadata, autoload=True)
		table_column_names_list = []
		for i in table.columns:
			table_column_names_list.append(str(i.name))

		if table_column_names_list.__contains__('provincia') == False:
			self.engine.execute("ALTER TABLE site_table ADD COLUMN provincia varchar DEFAULT 'inserici un valore' ")

		table = Table("us_table", self.metadata, autoload=True)
		table_column_names_list = []
		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('cont_per') == False:
			self.engine.execute("ALTER TABLE us_table ADD COLUMN cont_per varchar DEFAULT")

		if table_column_names_list.__contains__('documentazione') == False:
			self.engine.execute("ALTER TABLE us_table ADD COLUMN documentazione varchar DEFAULT")

		table = Table("periodizzazione_table", self.metadata, autoload=True)
		table_column_names_list = []
		for i in table.columns:
			table_column_names_list.append(str(i.name))

		if table_column_names_list.__contains__('cont_per') == False:
			self.engine.execute("ALTER TABLE periodizzazione_table ADD COLUMN cont_per integer DEFAULT 0 ")

		table = Table("inventario_materiali_table", self.metadata, autoload=True)
		table_column_names_list = []
		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('stato_conservazione') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN stato_conservazione varchar DEFAULT ''")

		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('datazione_reperto') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN datazione_reperto varchar(30) DEFAULT 'inserisci un valore'")

		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('elementi_reperto') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN elementi_reperto text")

		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('misurazioni') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN misurazioni text")

		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('rif_biblio') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN rif_biblio text")

		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('tecnologie') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN tecnologie text")
		
		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('forme_minime') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN forme_minime integer DEFAULT 0")
		
		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('forme_massime') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN forme_massime integer DEFAULT 0")
		
		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('totale_frammenti') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN totale_frammenti integer DEFAULT 0")
		
		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('corpo_ceramico') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN corpo_ceramico varchar(20)")
			self.engine.execute("update inventario_materiali_table set corpo_ceramico = ''")
		
		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('rivestimento') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN rivestimento varchar(20)")
			self.engine.execute("update inventario_materiali_table set rivestimento = ''")
		
		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('diametro_orlo') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN diametro_orlo Numeric(7,3) DEFAULT 0")

		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('peso') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN peso Numeric(9,3) DEFAULT 0")


		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('tipo') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN tipo varchar(20)")
			self.engine.execute("update inventario_materiali_table set tipo = ''")

		for i in table.columns:
			table_column_names_list.append(str(i.name))
		if table_column_names_list.__contains__('eve_orlo') == False:
			self.engine.execute("ALTER TABLE inventario_materiali_table ADD COLUMN eve_orlo Numeric(7,3) DEFAULT 0")

if __name__ == '__main__':
	dbup=DB_update()
	dbup.update_table()