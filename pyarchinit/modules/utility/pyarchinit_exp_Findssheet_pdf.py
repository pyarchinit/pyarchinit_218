import os
import copy
from reportlab.lib.testutils import makeSuiteForClasses, outputfile, printLocation
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, PageBreak, SimpleDocTemplate, Paragraph, Spacer, TableStyle, Image
from reportlab.platypus.paragraph import Paragraph

from datetime import date, time

from pyarchinit_OS_utility import *


class NumberedCanvas_Findssheet(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []
		
	def define_position(self, pos):
		self.page_position(pos)

	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		"""add page info to each page (page x of y)"""
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)

	def draw_page_number(self, page_count):
		self.setFont("Helvetica", 8)
		self.drawRightString(200*mm, 20*mm, "Pag. %d di %d" % (self._pageNumber, page_count)) #scheda us verticale 200mm x 20 mm

class NumberedCanvas_FINDSindex(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []

	def define_position(self, pos):
		self.page_position(pos)

	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		"""add page info to each page (page x of y)"""
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)

	def draw_page_number(self, page_count):
		self.setFont("Helvetica", 8)
		self.drawRightString(270*mm, 10*mm, "Pag. %d di %d" % (self._pageNumber, page_count)) #scheda us verticale 200mm x 20 mm


class NumberedCanvas_CASSEindex(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []

	def define_position(self, pos):
		self.page_position(pos)

	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		"""add page info to each page (page x of y)"""
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)

	def draw_page_number(self, page_count):
		self.setFont("Helvetica", 8)
		self.drawRightString(270*mm, 10*mm, "Pag. %d di %d" % (self._pageNumber, page_count)) #scheda us verticale 200mm x 20 mm





class single_Finds_pdf_sheet:

	def __init__(self, data):
		self.id_invmat = data[0]
		self.sito = data[1]
		self.numero_inventario = data[2]
		self.tipo_reperto = data[3]
		self.criterio_schedatura = data[4]
		self.definizione = data[5]
		self.descrizione = data[6]
		self.area = data[7]
		self.us = data[8]
		self.lavato =  data[9]
		self.nr_cassa = data[10]
		self.luogo_conservazione = data[11]
		self.stato_conservazione = data[12]
		self.datazione_reperto = data[13]
		self.elementi_reperto = data[14]
		self.misurazioni = data[15]
		self.rif_biblio = data[16]
		self.tecnologie = data[17]

	"""
	def unzip_rapporti_stratigrafici(self):
		rapporti = eval(self.rapporti)

		for rapporto in rapporti:
			if len(rapporto) == 2:
				if rapporto[0] == 'Si lega a' or rapporto[0] == 'si lega a':
					if self.si_lega_a == '':
						self.si_lega_a += str(rapporto[1])
					else:
						self.si_lega_a += ', ' + str(rapporto[1])

				if rapporto[0] == 'Uguale a' or rapporto[0] == 'uguale a':
					if self.uguale_a == '':
						self.uguale_a += str(rapporto[1])
					else:
						self.uguale_a += ', ' + str(rapporto[1])

				if rapporto[0] == 'Copre' or rapporto[0] == 'copre':
					if self.copre == '':
						self.copre += str(rapporto[1])
					else:
						self.copre += ', ' + str(rapporto[1])

				if rapporto[0] == 'Coperto da' or rapporto[0] == 'coperto da':
					if self.coperto_da == '':
						self.coperto_da += str(rapporto[1])
					else:
						self.coperto_da += ', ' + str(rapporto[1])

				if rapporto[0] == 'Riempie' or rapporto[0] == 'riempie':
					if self.riempie == '':
						self.riempie += str(rapporto[1])
					else:
						self.riempie += ', ' + str(rapporto[1])

				if rapporto[0] == 'Riempito da' or rapporto[0] == 'riempito da':
					if self.riempito_da == '':
						self.riempito_da += str(rapporto[1])
					else:
						self.riempito_da += ', ' + str(rapporto[1])
				if rapporto[0] == 'Taglia' or rapporto[0] == 'taglia':
					if self.taglia == '':
						self.taglia += str(rapporto[1])
					else:
						self.taglia += ', ' + str(rapporto[1])

				if rapporto[0] == 'Tagliato da' or rapporto[0] == 'tagliato da':
					if self.tagliato_da == '':
						self.tagliato_da += str(rapporto[1])
					else:
						self.tagliato_da += ', ' + str(rapporto[1])

				if rapporto[0] == 'Si appoggia a' or rapporto[0] == 'si appoggia a':
					if self.si_appoggia_a == '':
						self.si_appoggia_a+= str(rapporto[1])
					else:
						self.si_appoggia_a += ', ' + str(rapporto[1])

				if rapporto[0] == 'Gli si appoggia' or rapporto[0] == 'gli si appoggia a':
					if self.gli_si_appoggia == '':
						self.gli_si_appoggia += str(rapporto[1])
					else:
						self.gli_si_appoggia += ', ' + str(rapporto[1])
	"""

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def create_sheet(self):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT

		styleSheet = getSampleStyleSheet()
		styDescrizione = styleSheet['Normal']
		styDescrizione.spaceBefore = 20
		styDescrizione.spaceAfter = 20
		styDescrizione.alignment = 4 #Justified

		#format labels

		#0 row
		intestazione = Paragraph("<b>SCHEDA INVENTARIO REPERTI<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
		#intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

		if os.name == 'posix':
			home = os.environ['HOME']
		elif os.name == 'nt':
			home = os.environ['HOMEPATH']

		home_DB_path = ('%s%s%s') % (home, os.sep, 'pyarchinit_DB_folder')
		logo_path = ('%s%s%s') % (home_DB_path, os.sep, 'logo.jpg')
		logo = Image(logo_path)

		##		if test_image.drawWidth < 800:

		logo.drawHeight = 1.5*inch*logo.drawHeight / logo.drawWidth
		logo.drawWidth = 1.5*inch

		#1 row
		sito = Paragraph("<b>Sito</b><br/>"  + str(self.sito), styNormal)
		area = Paragraph("<b>Area</b><br/>"  + str(self.area), styNormal)
		us = Paragraph("<b>US</b><br/>"  + str(self.us), styNormal)
		nr_inventario = Paragraph("<b>Nr. Inventario</b><br/>"  + str(self.numero_inventario), styNormal)

		#2 row
		criterio_schedatura = Paragraph("<b>Criterio schedatura</b><br/>"  + self.criterio_schedatura, styNormal)
		tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>"  + self.tipo_reperto, styNormal)
		definizione = Paragraph("<b>Definizione</b><br/>"  + self.definizione, styNormal)

		#3 row
		stato_conservazione = Paragraph("<b>Stato Conservazione</b><br/>"  + self.stato_conservazione, styNormal)
		datazione = Paragraph("<b>Datazione</b><br/>"  + self.datazione_reperto, styNormal)
		
		#4 row
		descrizione = ''
		try:
			descrizione = Paragraph("<b>Descrizione</b><br/>" + str(self.descrizione), styDescrizione)
		except:
			pass

		#5 row
		elementi_reperto = ''
		if eval(self.elementi_reperto) > 0 :
			for i in eval(self.elementi_reperto):
				if elementi_reperto == '':
					try:
						elementi_reperto += ("Elemento rinvenuto: %s, Unita' di misura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass
				else:
					try:
						elementi_reperto += ("<br/>Elemento rinvenuto: %s, Unita' di misura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass

		elementi_reperto = Paragraph("<b>Elementi reperto</b><br/>"  + elementi_reperto, styNormal)

		#6 row
		misurazioni = ''
		if eval(self.misurazioni) > 0:
			for i in eval(self.misurazioni):
				if misurazioni == '':
					try:
						misurazioni += ("<b>Tipo di misura: %s, Unita' di misura: %s, Quantita': %s") % (str(i[0]), str(i[2]), str(i[1]))
					except:
						pass
				else:
					try:
						misurazioni += ("<br/><b>Tipo di misura: %s, Unita' di misura: %s, Quantita': %s") % (str(i[0]), str(i[2]), str(i[1]))
					except:
						pass
		misurazioni = Paragraph("<b>Misurazioni</b><br/>"  + misurazioni, styNormal)

		#7 row
		tecnologie = ''
		if eval(self.tecnologie) > 0:
			for i in eval(self.tecnologie):
				if tecnologie == '':
					try:
						tecnologie += ("<b>Tipo tecnologia: %s, Posizione: %s, Tipo quantita': %s, Unita' di misura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]),str(i[4]))
					except:
						pass
				else:
					try:
						tecnologie += ("<br/><b>Tipo tecnologia: %s, Posizione: %s, Tipo quantita': %s, Unita' di misura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]),str(i[4]))
					except:
						pass
		tecnologie = Paragraph("<b>Tecnologie</b><br/>"  + tecnologie, styNormal)

		#8 row
		rif_biblio = ''
		if eval(self.rif_biblio) > 0:
			for i in eval(self.rif_biblio): #gigi
				if rif_biblio == '':
					try:
						rif_biblio += ("<b>Autore: %s, Anno: %s, Titolo: %s, Pag.: %s, Fig.: %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]),str(i[4]))
					except:
						pass
				else:
					try:
						rif_biblio += ("<b>Autore: %s, Anno: %s, Titolo: %s, Pag.: %s, Fig.: %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]),str(i[4]))
					except:
						pass

		rif_biblio = Paragraph("<b>Riferimenti bibliografici</b><br/>"  + rif_biblio, styNormal)

		#9 row
		riferimenti_stratigrafici = Paragraph("<b>Riferimenti stratigrafici</b>",styNormal)

		#10 row
		area = Paragraph("<b>Area</b><br/>" + self.area,styNormal)
		us = Paragraph("<b>US</b><br/>" + self.us,styNormal)

		#11 row
		riferimenti_magazzino = Paragraph("<b>Riferimenti magazzino</b>",styNormal)

		#12 row
		lavato  = Paragraph("<b>Lavato</b><br/>" + self.lavato,styNormal)
		nr_cassa = Paragraph("<b>Nr. Cassa</b><br/>" + self.nr_cassa,styNormal)
		luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + self.luogo_conservazione,styNormal)

		#schema
		cell_schema =  [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
						[intestazione, '01', '02', '03', '04','05', '06', logo, '08', '09'],
						[sito, '01', '02', area, '04', us,'06', '07', nr_inventario, '09'], #1 row ok
						[tipo_reperto, '01', '02', criterio_schedatura,'04', '05',definizione, '07', '08', '09'], #2 row ok
						[datazione, '01', '02', '03', '04', stato_conservazione, '06', '07', '08', '09'], #3 row ok
						[descrizione, '01','02', '03', '04', '05','06', '07', '08', '09'], #4 row ok
						[elementi_reperto, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #5 row ok
						[misurazioni, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #6 row ok
						[tecnologie, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #7 row ok
						[rif_biblio, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #8 row ok
						[riferimenti_stratigrafici, '02', '03', '04', '05', '06', '07', '08', '09'], #9 row ok
						[area, '01', '02', us,'04', '05', '06', '07', '08', '09'], #10 row ok
						[riferimenti_magazzino, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #11 row ok
						[lavato, '01', '02', nr_cassa, '04', '05', luogo_conservazione, '07', '08', '09'] #12 row ok
						]


		#table style
		table_style=[

					('GRID',(0,0),(-1,-1),0.5,colors.black),
					#0 row
					('SPAN', (0,0),(6,0)),  #intestazione
					('SPAN', (7,0),(9,0)), #intestazione

					#1 row
					('SPAN', (0,1),(2,1)),  #dati identificativi
					('SPAN', (3,1),(4,1)),  #dati identificativi
					('SPAN', (5,1),(7,1)),  #dati identificativi
					('SPAN', (8,1),(9,1)),   #dati identificativi

					#2 row
					('SPAN', (0,2),(2,2)),  #definizione
					('SPAN', (3,2),(5,2)),  #definizione
					('SPAN', (6,2),(9,2)),  #definizione
					('VALIGN',(0,2),(9,2),'TOP'), 

					#3 row
					('SPAN', (0,3),(4,3)), #datazione
					('SPAN', (5,3),(9,3)),  #conservazione
					
					#4 row
					('SPAN', (0,4),(9,4)),  #descrizione

					#5 row
					('SPAN', (0,5),(9,5)),  #elementi_reperto

					#6 row
					('SPAN', (0,6),(9,6)),  #misurazioni
					
					#7 row
					('SPAN', (0,7),(9,7)),  #tecnologie

					#8 row
					('SPAN', (0,8),(9,8)),  #bibliografia
					
					#9 row
					('SPAN', (0,9),(9,9)),  #Riferimenti stratigrafici - Titolo

					#10 row
					('SPAN', (0,10),(2,10)),  #Riferimenti stratigrafici - area
					('SPAN', (3,10),(9,10)),  #Riferimenti stratigrafici - us

					#11 row
					('SPAN', (0,11),(9,11)),  #Riferimenti magazzino - Titolo

					#12 row
					('SPAN', (0,12),(2,12)),  #Riferimenti magazzino - lavato
					('SPAN', (3,12),(5,12)),  #Riferimenti magazzino - nr_cassa
					('SPAN', (6,12),(9,12)),   #Riferimenti magazzino - luogo conservazione

					('VALIGN',(0,0),(-1,-1),'TOP')

					]

		t=Table(cell_schema, colWidths=50, rowHeights=None,style= table_style)

		return t


class Box_labels_Finds_pdf_sheet:

	def __init__(self, data, sito):
		self.sito = sito #Sito
		self.cassa= data[0] #1 - Cassa
		self.elenco_inv_tip_rep = data[1] #2-  elenco US
		self.elenco_us = data[2] #3 - elenco Inventari
		self.luogo_conservazione = data[3]#4 - luogo conservazione

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def create_sheet(self):
		styleSheet = getSampleStyleSheet()
		
		styleSheet.add(ParagraphStyle(name='Cassa Label', fontName ='Helvetica',fontSize=22, textColor=colors.black, alignment=TA_LEFT))

		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT

		styCassaLabel = styleSheet['Cassa Label']
		styCassaLabel.spaceBefore = 20
		styCassaLabel.spaceAfter = 20
		styCassaLabel.alignment = 0 #LEFT


		#format labels

		num_cassa = Paragraph("<b>N. Cassa</b>" + str(self.cassa),styCassaLabel)
		sito = Paragraph("<b>Sito: </b>" + str(self.sito),styCassaLabel)

		if self.elenco_inv_tip_rep == None:
			elenco_inv_tip_rep = Paragraph("<b>Elenco N. Inv. / Tipo materiale</b><br/>",styNormal)
		else:
			elenco_inv_tip_rep = Paragraph("<b>Elenco N. Inv. / Tipo materiale</b><br/>" + str(self.elenco_inv_tip_rep ),styNormal)

		if self.elenco_us == None:
			elenco_us = Paragraph("<b>Elenco US/(Struttura)</b>",styNormal)
		else:
			elenco_us = Paragraph("<b>Elenco US/(Struttura)</b>" + str(self.elenco_us),styNormal)

		luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)

		#schema
		cell_schema =	[ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
							[sito, '01', '02', '03', '04','05', '06', '07', num_cassa, '09'],
							[elenco_us, '01', '02', '03','04', '05','06', '07', '08', '09'],
							[elenco_inv_tip_rep, '01', '02','03', '04', '05','06', '07', '08', '09'], #1 row ok
							[luogo_conservazione, '01', '02','03', '04', '05', '06' , '07', '08', '09']]


		#table style
		table_style=[

					('GRID',(0,0),(-1,-1),0,colors.white),#,0.0,colors.black
					#0 row
					('SPAN', (0,0),(7,0)),  #intestazione
					('SPAN', (8,0),(9,0)), #intestazione
					('VALIGN',(0,0),(9,0),'TOP'), 
					#1 row
					('SPAN', (0,1),(9,1)),  #elenco US
					('VALIGN',(0,1),(9,1),'TOP'), 
					#2 row
					('SPAN', (0,2),(9,2)),  #elenco_inv_tip_rep
					('VALIGN',(0,2),(9,2),'TOP'), 

					#3 row
					('SPAN', (0,3),(9,3)), #luogo conservazione
					('VALIGN',(0,3),(9,3),'TOP')
					]
		colWidths=[80,80,80, 80,80, 80,80,80,80, 60]
		t=Table(cell_schema, colWidths, rowHeights=80,style= table_style)

		return t




class CASSE_index_pdf_sheet:

	def __init__(self, data):
		self.cassa= data[0] #1 - Cassa
		self.elenco_inv_tip_rep = data[1] #2-  elenco US
		self.elenco_us = data[2] #3 - elenco Inventari
		self.luogo_conservazione = data[3]#4 - luogo conservazione

	def getTable(self):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT
		styNormal.fontSize = 9

		#self.unzip_rapporti_stratigrafici()

		num_cassa = Paragraph("<b>N. Cassa</b><br/>" + str(self.cassa),styNormal)

		if self.elenco_inv_tip_rep == None:
			elenco_inv_tip_rep = Paragraph("<b>Elenco N. Inv. / Tipo materiale</b><br/>",styNormal)
		else:
			elenco_inv_tip_rep = Paragraph("<b>Elenco N. Inv. / Tipo materiale</b><br/>" + str(self.elenco_inv_tip_rep ),styNormal)

		if self.elenco_us == None:
			elenco_us = Paragraph("<b>Elenco US/(Struttura)</b><br/>",styNormal)
		else:
			elenco_us = Paragraph("<b>Elenco US/(Struttura)</b><br/>" + str(self.elenco_us),styNormal)

		luogo_conservazione = Paragraph("<b>Luogo di conservazione</b><br/>" + str(self.luogo_conservazione),styNormal)


		data = [num_cassa,
					elenco_inv_tip_rep,
					elenco_us,
					luogo_conservazione]

		return data

	def makeStyles(self):
		styles =TableStyle([('GRID',(0,0),(-1,-1),0.0,colors.black),('VALIGN', (0,0), (-1,-1), 'TOP')])  #finale

		return styles


class FINDS_index_pdf_sheet:

	def __init__(self, data):
		self.sito = data[1] #1 - sito
		self.num_inventario = data[2] #2- numero_inventario
		self.tipo_reperto = data[3] #3 - tipo_reperto
		self.criterio_schedatura = data[4 ]#4 - criterio_schedatura
		self.definizione = data[5 ]#5 - definizione
		self.area = data[7] # 7 - area
		self.us = data[8] #8- us
		self.lavato = data[9] #9 - lavato
		self.numero_cassa = data[10] #10 - numero cassa

	def getTable(self):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT
		styNormal.fontSize = 9

		#self.unzip_rapporti_stratigrafici()

		num_inventario = Paragraph("<b>N. Inv.</b><br/>" + str(self.num_inventario),styNormal)

		if self.tipo_reperto == None:
			tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>",styNormal)
		else:
			tipo_reperto = Paragraph("<b>Tipo reperto</b><br/>" + str(self.tipo_reperto),styNormal)
	
		if self.criterio_schedatura == None:
			classe_materiale = Paragraph("<b>Classe materiale</b><br/>",styNormal)
		else:
			classe_materiale = Paragraph("<b>Classe materiale</b><br/>" + str(self.criterio_schedatura),styNormal)

		if self.definizione == None:
			definizione = Paragraph("<b>Definizione</b><br/>" ,styNormal)
		else:
			definizione = Paragraph("<b>Definizione</b><br/>" + str(self.definizione),styNormal)

		if str(self.area) == "None":
			area = Paragraph("<b>Area</b><br/>",styNormal)
		else:
			area = Paragraph("<b>Area</b><br/>" + str(self.area),styNormal)

		if str(self.us) == "None":
			us = Paragraph("<b>US</b><br/>",styNormal)
		else:
			us = Paragraph("<b>US</b><br/>" + str(self.us),styNormal)

		if self.lavato == None:
			lavato = Paragraph("<b>Lavato</b><br/>",styNormal)
		else:
			lavato = Paragraph("<b>Lavato</b><br/>" + str(self.lavato),styNormal)

		if str(self.numero_cassa) == "None":
			nr_cassa = Paragraph("<b>Nr. Cassa</b><br/>",styNormal)
		else:
			nr_cassa = Paragraph("<b>Nr. Cassa</b><br/>" + str(self.numero_cassa),styNormal)


		data = [num_inventario,
				tipo_reperto,
				classe_materiale,
				definizione,
				area,
				us,
				lavato,
				nr_cassa]

		return data

	def makeStyles(self):
		styles =TableStyle([('GRID',(0,0),(-1,-1),0.0,colors.black),('VALIGN', (0,0), (-1,-1), 'TOP')
		])  #finale

		return styles

class generate_reperti_pdf:
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']
	
	PDF_path = ('%s%s%s') % (HOME, os.sep, "pyarchinit_PDF_folder")

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def build_Finds_sheets(self, records):
		elements = []
		for i in range(len(records)):
			single_finds_sheet = single_Finds_pdf_sheet(records[i])
			elements.append(single_finds_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'scheda_Finds.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f)
		doc.build(elements, canvasmaker=NumberedCanvas_Findssheet)
		f.close()

	def build_index_Finds(self, records, sito):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
		styH1 = styleSheet['Heading1']
		data = self.datestrfdate()
		lst = []
		lst.append(Paragraph("<b>ELENCO MATERIALI</b><br/><b>Sito: %s <br/>Data: %s <br/>Ditta esecutrice: adArte snc, Rimini</b>" % (sito, data), styH1))

		table_data = []
		for i in range(len(records)):
			exp_index = FINDS_index_pdf_sheet(records[i])
			table_data.append(exp_index.getTable())
		
		styles = exp_index.makeStyles()
		table_data_formatted = Table(table_data,  colWidths=89)
		table_data_formatted.setStyle(styles)

		lst.append(table_data_formatted)
		lst.append(Spacer(0,2))

		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'indice_materiali.pdf')
		f = open(filename, "wb")

		doc = SimpleDocTemplate(f, pagesize=(29*cm, 21*cm), showBoundary=0)
		doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

		f.close()

	def build_index_Casse(self, records, sito):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
		styH3 = styleSheet['Heading3']
		data = self.datestrfdate()
		lst = []
		lst.append(Paragraph("<b>ELENCO CASSE</b><br/><b>Sito: %s <br/>Data: %s <br/>Ditta esecutrice: adArte snc, Rimini</b>" % (sito, data), styH3))

		table_data = []
		for i in range(len(records)):
			exp_index = CASSE_index_pdf_sheet(records[i])
			table_data.append(exp_index.getTable())

		styles = exp_index.makeStyles()
		colWidths=[60,150,100, 120]
		table_data_formatted = Table(table_data, colWidths, style=styles)
		table_data_formatted.hAlign = "LEFT"

		#table_data_formatted.setStyle(styles)

		lst.append(table_data_formatted)
		lst.append(Spacer(0,0))

		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'elenco_casse.pdf')
		f = open(filename, "wb")

		doc = SimpleDocTemplate(f, pagesize=(21*cm, 29*cm), showBoundary=1)
		doc.build(lst, canvasmaker=NumberedCanvas_FINDSindex)

		f.close()


	def build_box_labels_Finds(self, records, sito):
		elements = []
		for i in range(len(records)):
			single_finds_sheet = Box_labels_Finds_pdf_sheet(records[i], sito)
			elements.append(single_finds_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'etichette_casse.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f, pagesize=(29*cm, 21*cm), showBoundary=0)
		doc.build(elements)
		f.close()

