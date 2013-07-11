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


class NumberedCanvas_Individuisheet(canvas.Canvas):
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
"""
class NumberedCanvas_Individuiindex(canvas.Canvas):
	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []

	def define_position(self, pos):
		self.page_position(pos)

	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		#add page info to each page (page x of y)
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)

	def draw_page_number(self, page_count):
		self.setFont("Helvetica", 8)
		self.drawRightString(270*mm, 10*mm, "Pag. %d di %d" % (self._pageNumber, page_count)) #scheda us verticale 200mm x 20 mm
	"""
class single_Individui_pdf_sheet:
	def __init__(self, data):
		self.sito = data[0]
		self.area = data[1]
		self.us = data[2]
		self.nr_individuo = data[3]
		self.data_schedatura = data[4]
		self.schedatore = data[5]
		self.sesso = data[6]
		self.eta_min = data[7]
		self.eta_max =  data[8]
		self.classi_eta = data[9]
		self.osservazioni = data[10]

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
		
		"""
		#format labels
		self.id_scheda_ind = data[0]
		self.sito = data[1]
		self.area = data[2]
		self.us = data[3]
		self.nr_individuo = data[4]
		self.data_schedatura = data[5]
		self.schedatore = data[6]
		self.sesso = data[7]
		self.eta_min = data[8]
		self.eta_max =  data[9]
		self.classi_eta = data[10]
		self.osservazioni = data[11]
		"""

		#0 row
		intestazione = Paragraph("<b>SCHEDA INDIVIDUI<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
		intestazione2 = Paragraph("<b>pyArchInit</b>", styNormal)

		#1 row
		sito = Paragraph("<b>Sito</b><br/>"  + str(self.sito), styNormal)
		area = Paragraph("<b>Area</b><br/>"  + str(self.area), styNormal)
		us = Paragraph("<b>US</b><br/>"  + str(self.us), styNormal)
		nr_inventario = Paragraph("<b>Nr. Individuo</b><br/>"  + str(self.nr_individuo), styNormal)

		#2 row
		sesso = Paragraph("<b>Sesso</b><br/>"  + self.sesso, styNormal)
		eta_min = Paragraph("<b>Eta' minima</b><br/>"  + self.eta_min, styNormal)
		eta_max = Paragraph("<b>Eta' massima</b><br/>"  + self.eta_max, styNormal)

		#3 row
		classi_eta = Paragraph("<b>Classi di eta'</b><br/>"  + self.classi_eta, styNormal)

		#4 row
		osservazioni = ''
		try:
			osservazioni = Paragraph("<b>Osservazioni</b><br/>" + str(self.osservazioni), styDescrizione)
		except:
			pass
		
		"""
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
						elementi_reperto += ("<br/>Elemento rinvenuto: %s, Unita' di musura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass

		elementi_reperto = Paragraph("<b>Elementi reperto</b><br/>"  + elementi_reperto, styNormal)

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
						misurazioni += ("<br/><b>Tipo di misura: %s, Unita' di musura: %s, Quantita': %s") % (str(i[0]), str(i[2]), str(i[1]))
					except:
						pass
		misurazioni = Paragraph("<b>Misurazioni</b><br/>"  + misurazioni, styNormal)

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
						tecnologie += ("<br/><b>Tipo tecnologia: %s, Posizione: %s, Tipo quantita': %s, Unita' di musura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]),str(i[4]))
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
						rif_biblio += ("<br/><b>Tipo tecnologia: %s, Posizione: %s, Tipo quantita': %s, Unita' di musura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]),str(i[4]))
					except:
						pass

		rif_biblio = Paragraph("<b>Riferimenti bibliografici</b><br/>"  + rif_biblio, styNormal)
		"""

		#12 row
		data_schedatura  = Paragraph("<b>Data schedatura</b><br/>" + self.data_schedatura,styNormal)
		schedatore = Paragraph("<b>Schedatore</b><br/>" + self.schedatore,styNormal)

		#schema
		cell_schema =  [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
						[intestazione, '01', '02', '03', '04','05', '06', '07', intestazione2, '09'],
						[sito, '01', '02', area, '04', us,'06', '07', nr_inventario, '09'], #1 row ok
						[sesso, '01', '02', eta_min,'04', '05',eta_max, '07', '08', '09'], #2 row ok
						[classi_eta, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #3 row ok
						[osservazioni, '01','02', '03', '04', '05','06', '07', '08', '09'], #4 row ok
						[data_schedatura, '01', '02', '03', '04', '05', schedatore, '07', '08', '09'], #5 row ok
						['https://sites.google.com/site/pyarchinit/', '01', '02', '03', '04','05', '06', '07','08', '09'] #6 row
						]


		#table style
		table_style=[

					('GRID',(0,0),(-1,-1),0.5,colors.black),
					#0 row
					('SPAN', (0,0),(7,0)),  #intestazione
					('SPAN', (8,0),(9,0)), #intestazione2

					#1 row
					('SPAN', (0,1),(2,1)),  #sito
					('SPAN', (3,1),(4,1)),  #area
					('SPAN', (5,1),(7,1)),  #us
					('SPAN', (8,1),(9,1)),  #nr_inventario

					#2 row
					('SPAN', (0,2),(2,2)),  #sesso
					('SPAN', (3,2),(5,2)),  #eta_min
					('SPAN', (6,2),(9,2)),  #eta_max
					('VALIGN',(0,2),(9,2),'TOP'), 

					#3 row
					('SPAN', (0,3),(9,3)), #classi_eta
					
					#4 row
					('SPAN', (0,4),(9,4)),  #osservazioni

					#5 row
					('SPAN', (0,5),(5,5)),  #data_schedatura
					('SPAN', (6,5),(9,5)),  #schedatore

					#13 row
					('SPAN', (0,6),(9,6)),  #pie' di pagina
					('ALIGN',(0,6),(9,6),'CENTER')

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

	def build_Individui_sheets(self, records):
		elements = []
		for i in range(len(records)):
			single_individui_sheet = single_Individui_pdf_sheet(records[i])
			elements.append(single_individui_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'scheda_Individui.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f)
		doc.build(elements, canvasmaker=NumberedCanvas_Individuisheet)
		f.close()
		
		
	"""
	def build_index_US(self, records, sito):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
		styH1 = styleSheet['Heading1']
		data = self.datestrfdate()
		lst = []
		lst.append(Paragraph("<b>ELENCO INDIVIDUI'</b><br/><b>Scavo: %s <br/>Data: %s <br/>Ditta esecutrice: adArte snc, Rimini</b>" % (sito, data), styH1))

		table_data = []
		for i in range(len(records)):
			exp_index = US_index_pdf_sheet(records[i])
			table_data.append(exp_index.getTable())
		
		styles = exp_index.makeStyles()
		table_data_formatted = Table(table_data,  colWidths=55.5)
		table_data_formatted.setStyle(styles)

		lst.append(table_data_formatted)
		lst.append(Spacer(0,12))

		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'indice_us.pdf')
		f = open(filename, "wb")

		doc = SimpleDocTemplate(f, pagesize=(29*cm, 21*cm), showBoundary=0)
		doc.build(lst, canvasmaker=NumberedCanvas_USindex)

		f.close()
	"""
