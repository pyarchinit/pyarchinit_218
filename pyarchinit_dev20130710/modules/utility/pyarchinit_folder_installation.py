#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
/***************************************************************************
	pyArchInit Plugin  - A QGIS plugin to manage archaeological dataset
							 stored in Postgres
							 -------------------
	begin				 : 2007-12-01
	copyright			 : (C) 2008 by Luca Mandolesi
	email				 : mandoluca at gmail.com
 ***************************************************************************/

/***************************************************************************
 *																		   *
 *	 This program is free software; you can redistribute it and/or modify  *
 *	 it under the terms of the GNU General Public License as published by  *
 *	 the Free Software Foundation; either version 2 of the License, or	   *
 *	 (at your option) any later version.								   *
 *																		   *
 ***************************************************************************/
"""

import os
import shutil
from pyarchinit_OS_utility import *

class pyarchinit_Folder_installation:

	def install_dir(self):
		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		module_path_rel = os.path.join(os.sep, '.qgis', 'python','plugins', 'pyarchinit', 'modules', 'utility')
		module_path = ('%s%s') % (home, module_path_rel)

		home_DB_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_DB_folder')

		config_copy_from_path_rel = os.path.join(os.sep, 'DBfiles', 'config.cfg')
		config_copy_from_path =  ('%s%s') % (module_path, config_copy_from_path_rel)
		config_copy_to_path = ('%s%s%s') % (home_DB_path, os.sep, 'config.cfg')

		db_copy_from_path_rel = os.path.join(os.sep, 'DBfiles', 'pyarchinit_db.sqlite')
		db_copy_from_path = ('%s%s') % (module_path, db_copy_from_path_rel)
		db_copy_to_path = ('%s%s%s') % (home_DB_path, os.sep, 'pyarchinit_db.sqlite')
	
		OS_utility = pyarchinit_OS_Utility()

		OS_utility.create_dir(str(home_DB_path))

		OS_utility.copy_file(config_copy_from_path, config_copy_to_path)
		OS_utility.copy_file(db_copy_from_path, db_copy_to_path)


		home_PDF_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_PDF_folder')
		OS_utility.create_dir(home_PDF_path)

		home_MATRIX_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_Matrix_folder')
		OS_utility.create_dir(home_MATRIX_path)
	
		home_THUMBNAILS_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_Thumbnails_folder')
		OS_utility.create_dir(home_THUMBNAILS_path)
		
		
		home_MAPS_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_MAPS_folder')
		OS_utility.create_dir(home_MAPS_path)

		home_REPORT_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_Report_folder')
		OS_utility.create_dir(home_REPORT_path)

		home_QUANT_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_Quantificazioni_folder')
		OS_utility.create_dir(home_QUANT_path)

		home_TEST_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_Test_folder')
		OS_utility.create_dir(home_TEST_path)

		home_BECKUP_linux_path = ('%s%s%s') % (home, os.sep,'pyarchinit_db_beckup')
		OS_utility.create_dir(home_BECKUP_linux_path)
		
		
