import os
import copy
from reportlab.lib.testutils import makeSuiteForClasses, outputfile, printLocation
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, PageBreak, SimpleDocTemplate, Paragraph, Spacer, TableStyle
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

class NumberedCanvas_USindex(canvas.Canvas):
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
		intestazione = Paragraph("<b>List Sample Form<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
		intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

		#1 row
		sito = Paragraph("<b>Site</b><br/>"  + str(self.sito), styNormal)
		area = Paragraph("<b>Area</b><br/>"  + str(self.area), styNormal)
		us = Paragraph("<b>SU</b><br/>"  + str(self.us), styNormal)
		nr_inventario = Paragraph("<b>Nr. List</b><br/>"  + str(self.numero_inventario), styNormal)

		#2 row
		criterio_schedatura = Paragraph("<b>Catalogue</b><br/>"  + self.criterio_schedatura, styNormal)
		tipo_reperto = Paragraph("<b>Sample Type</b><br/>"  + self.tipo_reperto, styNormal)
		definizione = Paragraph("<b>Definition</b><br/>"  + self.definizione, styNormal)

		#3 row
		stato_conservazione = Paragraph("<b>Preservation</b><br/>"  + self.stato_conservazione, styNormal)
		datazione = Paragraph("<b>Dating</b><br/>"  + self.datazione_reperto, styNormal)
		
		#4 row
		descrizione = ''
		try:
			descrizione = Paragraph("<b>Description</b><br/>" + str(self.descrizione), styDescrizione)
		except:
			pass

		#5 row
		elementi_reperto = ''
		if eval(self.elementi_reperto) > 0 :
			for i in eval(self.elementi_reperto):
				if elementi_reperto == '':
					try:
						elementi_reperto += ("Elemento rinvenuto: %s, Unita' di musura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass
				else:
					try:
						elementi_reperto += ("<br/>Sample Find: %s, Units: %s, Quantity: %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass

		elementi_reperto = Paragraph("<b>Sample</b><br/>"  + elementi_reperto, styNormal)

		#6 row
		misurazioni = ''
		if eval(self.misurazioni) > 0:
			for i in eval(self.misurazioni):
				if misurazioni == '':
					try:
						misurazioni += ("<b>Tipo di misura: %s, Unita' di musura: %s, Quantita': %s") % (str(i[0]), str(i[2]), str(i[1]))
					except:
						pass
				else:
					try:
						misurazioni += ("<br/><b>Measure Type: %s, Units: %s, Quantity: %s") % (str(i[0]), str(i[2]), str(i[1]))
					except:
						pass
		misurazioni = Paragraph("<b>Measureaments</b><br/>"  + misurazioni, styNormal)

		#7 row
		tecnologie = ''
		if eval(self.tecnologie) > 0:
			for i in eval(self.tecnologie):
				if tecnologie == '':
					try:
						tecnologie += ("<b>Tipo tecnologia: %s, Posizione: %s, Tipo quantita': %s, Unita' di musura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]),str(i[4]))
					except:
						pass
				else:
					try:
						tecnologie += ("<br/><b>Technology: %s, Position: %s, Quantity Type': %s, Units: %s, Quantity: %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]),str(i[4]))
					except:
						pass
		tecnologie = Paragraph("<b>Technology</b><br/>"  + tecnologie, styNormal)

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
						rif_biblio += ("<b>Author: %s, Year: %s, Title: %s, Pag.: %s, Fig.:") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]),str(i[4]))
					except:
						pass

		rif_biblio = Paragraph("<b>Bibliography</b><br/>"  + rif_biblio, styNormal)

		#9 row
		riferimenti_stratigrafici = Paragraph("<b>Stratigraphic Reletionship</b>",styNormal)

		#10 row
		area = Paragraph("<b>Area</b><br/>" + self.area,styNormal)
		us = Paragraph("<b>SU</b><br/>" + self.us,styNormal)

		#11 row
		riferimenti_magazzino = Paragraph("<b>Store</b>",styNormal)

		#12 row
		lavato  = Paragraph("<b>Woshed</b><br/>" + self.lavato,styNormal)
		nr_cassa = Paragraph("<b>Nr. Box</b><br/>" + self.nr_cassa,styNormal)
		luogo_conservazione = Paragraph("<b>Preservation Place</b><br/>" + self.luogo_conservazione,styNormal)

		#schema
		cell_schema =  [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
						[intestazione, '01', '02', '03', '04','05', '06', '07', intestazione2, '09'],
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
						[lavato, '01', '02', nr_cassa, '04', '05', luogo_conservazione, '07', '08', '09'], #12 row ok
						['https://sites.google.com/site/pyarchinit/', '01', '02', '03', '04','05', '06', '07','08', '09'] #13 row
						]


		#table style
		table_style=[

					('GRID',(0,0),(-1,-1),0.5,colors.black),
					#0 row
					('SPAN', (0,0),(7,0)),  #intestazione
					('SPAN', (8,0),(9,0)), #intestazione

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

					#13 row
					('SPAN', (0,13),(9,13)),  #pie' di pagina
					('ALIGN',(0,13),(9,13),'CENTER')

					]

		t=Table(cell_schema, colWidths=50, rowHeights=None,style= table_style)

		return t
	
class generate_pdf:
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']
	
	PDF_path = ('%s%s%s') % (HOME, os.sep, "pyarchinit_PDF_folder")

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def build_Finds_sheets_en(self, records):
		import time
		elements = []
		for i in range(len(records)):
			single_finds_sheet = single_Finds_pdf_sheet(records[i])
			elements.append(single_finds_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'Form_Finds_'+time.strftime("%Y%m%d_%H_%M_%S_")+'.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f)
		doc.build(elements, canvasmaker=NumberedCanvas_Findssheet)
		f.close()

	
