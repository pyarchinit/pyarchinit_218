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


class NumberedCanvas_TAFONOMIAsheet(canvas.Canvas):
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


class single_Tafonomia_pdf_sheet:
	#rapporti stratigrafici

	def __init__(self, data):
		self.sito =  							data[0]
		self.nr_scheda_taf =  			data[1]
		self.sigla_struttura =  			data[2]
		self.nr_struttura =  				data[3]
		self.nr_individuo =  				data[4]
		self.rito =  							data[5]
		self.descrizione_taf =  			data[6]
		self.interpretazione_taf = 		data[7]
		self.segnacoli =  					data[8]
		self.canale_libatorio_si_no = 	data[9]
		self.oggetti_rinvenuti_esterno =  data[10]
		self.stato_di_conservazione = data[11]
		self.copertura_tipo =  			data[12]
		self.tipo_contenitore_resti = 	data[13]
		self.orientamento_asse = 		data[14]
		self.orientamento_azimut = 	data[15]
		self.corredo_presenza = 		data[16]
		self.corredo_tipo =  				data[17]
		self.corredo_descrizione = 		data[18]
		self.lunghezza_scheletro = 	data[19]
		self.posizione_scheletro =  	data[20]
		self.posizione_cranio =  		data[21]
		self.posizione_arti_superiori =  data[22]
		self.posizione_arti_inferiori =  	data[23]
		self.completo_si_no =  			data[24]
		self.disturbato_si_no =  		data[25]
		self.in_connessione_si_no =  	data[26]
		self.caratteristiche = 			data[27]

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
		intestazione = Paragraph("<b>SCHEDA TAFONOMICA<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
		intestazione2 = Paragraph("<b>pyArchInit</b><br/>www.pyarchinit.blogspot.com", styNormal)

		#1 row
		sito = Paragraph("<b>Sito</b><br/>"  + str(self.sito), styNormal)
		sigla_struttura = Paragraph("<b>Sigla struttura</b><br/>"  + str(self.sigla_struttura)+str(self.nr_struttura), styNormal)
		nr_individuo = Paragraph("<b>Nr. Individuo</b><br/>"  + str(self.nr_individuo), styNormal)
		nr_scheda = Paragraph("<b>Nr. Scheda</b><br/>"  + str(self.nr_scheda_taf), styNormal)

		#2 row
		rito = Paragraph("<b>Rito</b><br/>"  + self.rito, styNormal)
		tipo_contenitore_resti = Paragraph("<b>Tipo contenitore resti</b><br/>"  + str(self.tipo_contenitore_resti), styNormal)
		tipo_copertura = Paragraph("<b>Tipo copertura</b><br/>"  + str(self.copertura_tipo), styNormal)
		orientamento_asse = Paragraph("<b>Orientamento asse</b><br/>"  + str(self.orientamento_asse), styNormal)
		if str(self.orientamento_azimut) == "None":
			orientamento_azimut = Paragraph("<b>Azimut</b><br/>", styNormal)
		else:
			orientamento_azimut = Paragraph("<b>Azimut</b><br/>"  + str(self.orientamento_azimut), styNormal)

		#3 row
		segnacoli = Paragraph("<b>Segnacoli</b><br/>"  + str(self.segnacoli), styNormal)
		canale_libatorio = Paragraph("<b>Canale libatorio</b><br/>"  + str(self.canale_libatorio_si_no), styNormal)
		oggetti_rinv_esterno = Paragraph("<b>Oggetti rinvenuti all'esterno</b><br/>"  + str(self.oggetti_rinvenuti_esterno), styNormal)
		stato_conservazione = Paragraph("<b>Stato di conservazione</b><br/>"  + str(self.stato_di_conservazione), styNormal)

		#4 row
		if str(self.lunghezza_scheletro) == "None":
			lunghezza_scheletro = Paragraph("<b>Lunghezza scheletro</b><br/>", styNormal)
		else:
			lunghezza_scheletro = Paragraph("<b>Lunghezza scheletro</b><br/>"  + str(self.lunghezza_scheletro), styNormal)
		posizione_scheletro = Paragraph("<b>Posizione scheletro</b><br/>"  + str(self.posizione_scheletro), styNormal)
		posizione_cranio = Paragraph("<b>Posizione cranio</b><br/>"  + str(self.posizione_scheletro), styNormal)

		#5 row
		posizione_arti_superiori = Paragraph("<b>Posizione arti superiori</b><br/>"  + str(self.posizione_arti_superiori), styNormal)
		posizione_arti_inferiori = Paragraph("<b>Posizione arti inferiori</b><br/>"  + str(self.posizione_arti_inferiori), styNormal)

		#6 row
		descrizione = ''
		try:
			descrizione = Paragraph("<b>Descrizione</b><br/>" + str(self.descrizione_taf), styDescrizione)
		except:
			pass

		interpretazione = ''
		try:
			interpretazione = Paragraph("<b>Interpretazione</b><br/>" + str(self.interpretazione_taf),styDescrizione)
		except:
			pass
		
		#7 row
		corredo = Paragraph("<b>Corredo</b></b>",styNormal)
		corredo_presente = Paragraph("<b>Corredo presente</b><br/>" + str(self.corredo_presenza),styDescrizione)

		#8 row
		corredo_tipo = ''
		if eval(self.corredo_tipo) > 0 :
			for i in eval(self.corredo_tipo):
				if corredo_tipo == '':
					try:
						corredo_tipo += ("Nr. reperto %s, tipo corredo: %s, descrizione: %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass
				else:
					try:
						corredo_tipo += ("<br/>Nr. reperto %s, tipo corredo: %s, descrizione: %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass

		corredo_tipo_txt = Paragraph("<b>Corredo tipo</b><br/>"  + corredo_tipo, styNormal)

		#9 row
		caratteristiche_tafonomiche = ''
		if eval(self.caratteristiche) > 0 :
			for i in eval(self.caratteristiche):
				if caratteristiche_tafonomiche == '':
					try:
						caratteristiche_tafonomiche += ("Tipo caratteristica %s, posizione: %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass
				else:
					try:
						caratteristiche_tafonomiche += ("<br/>Tipo caratteristica %s, posizione: %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass

		caratteristiche_tafonomiche_txt = Paragraph("<b>Caratteristiche tafonomiche</b><br/>"  + caratteristiche_tafonomiche, styNormal)

		#schema
		cell_schema =  [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
						[intestazione, '01', '02', '03', '04','05', '06', intestazione2, '08', '09'], #0 row ok
		 				[sito, '01', '02', '03', '04', sigla_struttura, '06', '07',nr_individuo,nr_scheda], #1 row ok
						[rito, '01', '02',tipo_contenitore_resti,'04', tipo_copertura,'06', orientamento_asse, '08',orientamento_azimut], #2 row ok
						[segnacoli, '01', '02',canale_libatorio,'04', oggetti_rinv_esterno,'06', stato_conservazione, '08','09'], #3 row ok
						[lunghezza_scheletro, '01', '02',posizione_scheletro,'04', '05', posizione_cranio,'07', '08','09'], #4row ok
						[posizione_arti_superiori, '01','02', '03', '04', posizione_arti_inferiori, '06', '07', '08', '09'], #5 row ok
						[descrizione, '01','02', '03', '04', interpretazione, '06', '07', '08', '09'], #6 row ok
						[corredo,'01', '02', '03', '04',corredo_presente, '06', '07', '08', '09'], #7 row
						[corredo_tipo_txt, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #8 row
						[caratteristiche_tafonomiche_txt, '01', '02', '03', '04', '05', '06', '07', '08', '09'] #9 row
						]

		#table style
		table_style=[
					('GRID',(0,0),(-1,-1),0.5,colors.black),
					#0 row
					('SPAN', (0,0),(6,0)),  #intestazione
					('SPAN', (7,0),(9,0)),  #intestazione

					#1 row
					('SPAN', (0,1),(4,1)),  #dati identificativi
					('SPAN', (5,1),(7,1)),  #dati identificativi
					('SPAN', (8,1),(8,1)),  #dati identificativi
					('SPAN', (9,1),(9,1)),  #dati identificativi

					#2 row
					('SPAN', (0,2),(2,2)),  #Definizione - interpretazone
					('SPAN', (3,2),(4,2)),  #definizione - intepretazione
					('SPAN', (5,2),(6,2)),  #definizione - intepretazione
					('SPAN', (7,2),(8,2)),  #definizione - intepretazione
					('SPAN', (9,2),(9,2)),  #definizione - intepretazione

					#3 row
					('SPAN', (0,3),(2,3)),  #conservazione - consistenza - colore
					('SPAN', (3,3),(4,3)),  #conservazione - consistenza - colore
					('SPAN', (5,3),(6,3)),  #conservazione - consistenza - colore
					('SPAN', (7,3),(9,3)),  #conservazione - consistenza - colore

					#4 row
					('SPAN', (0,4),(2,4)),  #inclusi - campioni - formazione
					('SPAN', (3,4),(5,4)),  #inclusi - campioni - formazione
					('SPAN', (6,4),(9,4)),  #inclusi - campioni - formazione

					#5 row
					('SPAN', (0,5),(4,5)),  #iniziale
					('SPAN', (5,5),(9,5)),  #periodo inizlae
					('VALIGN',(0,5),(0,5),'TOP'), 
					('VALIGN',(5,5),(5,5),'TOP'), 

					#6 row
					('SPAN', (0,6),(4,6)),  #Attivita - Struttura - Quota min - Quota max
					('SPAN', (5,6),(9,6)),  #Attivita - Struttura - Quota min - Quota max

					#7 row
					('SPAN', (0,7),(4,7)),  #Attivita - Struttura - Quota min - Quota max
					('SPAN', (5,7),(9,7)),  #Attivita - Struttura - Quota min - Quota max

					#8 row
					('SPAN', (0,8),(9,8)),  #Attivita - Struttura - Quota min - Quota max
					
					#9 row
					('SPAN', (0,9),(9,9)),  #Attivita - Struttura - Quota min - Quota max

					('VALIGN',(0,0),(-1,-1),'TOP')

					]

		t=Table(cell_schema, colWidths=50, rowHeights=None,style= table_style)

		return t

class generate_tafonomia_pdf:
	if os.name == 'posix':
		HOME = os.environ['HOME']
	elif os.name == 'nt':
		HOME = os.environ['HOMEPATH']

	PDF_path = ('%s%s%s') % (HOME, os.sep, "pyarchinit_PDF_folder")

	def datestrfdate(self):
		now = date.today()
		today = now.strftime("%d-%m-%Y")
		return today

	def build_Tafonomia_sheets(self, records):
		elements = []
		for i in range(len(records)):
			single_tafonomia_sheet = single_Tafonomia_pdf_sheet(records[i])
			elements.append(single_tafonomia_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'scheda_Tafonomica.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f)
		doc.build(elements, canvasmaker=NumberedCanvas_TAFONOMIAsheet)
		f.close()