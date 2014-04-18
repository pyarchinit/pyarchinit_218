#! /usr/bin/env python
# -*- coding: utf-8 -*-


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
from pyarchinit_utility import Utility


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
	PU = Utility()
	#rapporti stratigrafici

	def __init__(self, data):
		self.sito =  								data[0]
		self.nr_scheda_taf =  				data[1]
		self.sigla_struttura =  				data[2]
		self.nr_struttura =  					data[3]
		self.nr_individuo =  					data[4]
		self.rito =  								data[5]
		self.descrizione_taf =  				data[6]
		self.interpretazione_taf = 			data[7]
		self.segnacoli =  						data[8]
		self.canale_libatorio_si_no = 		data[9]
		self.oggetti_rinvenuti_esterno =	data[10]
		self.stato_di_conservazione =		data[11]
		self.copertura_tipo =  				data[12]
		self.tipo_contenitore_resti = 		data[13]
		self.orientamento_asse = 			data[14]
		self.orientamento_azimut = 		data[15]
		self.corredo_presenza = 			data[16]
		self.corredo_tipo =  					data[17]
		self.corredo_descrizione = 			data[18]
		self.lunghezza_scheletro = 		data[19]
		self.posizione_scheletro =  		data[20]
		self.posizione_cranio =  			data[21]
		self.posizione_arti_superiori 	=	data[22]
		self.posizione_arti_inferiori =  		data[23]
		self.completo_si_no =  				data[24]
		self.disturbato_si_no =  			data[25]
		self.in_connessione_si_no = 	 	data[26]
		self.caratteristiche = 				data[27]
		self.periodo_iniziale = 				data[28]
		self.fase_iniziale =	 				data[29]
		self.periodo_finale = 					data[30]
		self.fase_finale = 					data[31]
		self.datazione_estesa = 			data[32]
		self.misure_tafonomia = 			data[33]

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
		intestazione2 = Paragraph("<b>pyArchInit</b><br/>pyarchinit", styNormal)

		#1 row
		sito = Paragraph("<b>Sito</b><br/>"  + str(self.sito), styNormal)
		sigla_struttura = Paragraph("<b>Sigla struttura</b><br/>"  + str(self.sigla_struttura)+str(self.nr_struttura), styNormal)
		nr_individuo = Paragraph("<b>Nr. Individuo</b><br/>"  + str(self.nr_individuo), styNormal)
		nr_scheda = Paragraph("<b>Nr. Scheda</b><br/>"  + str(self.nr_scheda_taf), styNormal)

		#2 row
		periodizzazione = Paragraph("<b>PERIODIZZAZIONE DEL RITO DI SEPOLTURA</b><br/>", styNormal)

		#3 row
		periodo_iniziale = Paragraph("<b>Periodo iniziale</b><br/>" + str(self.periodo_iniziale), styNormal)
		fase_iniziale = Paragraph("<b>Fase iniziale</b><br/>" + str(self.fase_iniziale), styNormal)
		periodo_finale = Paragraph("<b>Periodo finale</b><br/>" + str(self.periodo_finale), styNormal)
		fase_finale = Paragraph("<b>Fase finale</b><br/>" + str(self.fase_finale), styNormal)

		#4 row
		datazione_estesa = Paragraph("<b>Datazione estesa</b><br/>" + str(self.datazione_estesa), styNormal)

		#5 row
		elementi_strutturali = Paragraph("<b>ELEMENTI STRUTTURALI</b></b>",styNormal)

		#6row
		tipo_contenitore_resti = Paragraph("<b>Tipo contenitore resti</b><br/>"  + str(self.tipo_contenitore_resti), styNormal)
		tipo_copertura = Paragraph("<b>Tipo copertura</b><br/>"  + str(self.copertura_tipo), styNormal)
		segnacoli = Paragraph("<b>Segnacoli</b><br/>"  + str(self.segnacoli), styNormal)
		canale_libatorio = Paragraph("<b>Canale libatorio</b><br/>"  + str(self.canale_libatorio_si_no), styNormal)

		#7 row
		dati_deposizionali = Paragraph("<b>DATI DEPOSIZIONALI INUMATO<b></b>",styNormal)

		#8 row
		rito = Paragraph("<b>Rito</b><br/>"  + self.rito, styNormal)
		orientamento_asse = Paragraph("<b>Orientamento asse</b><br/>"  + str(self.orientamento_asse), styNormal)
		if str(self.orientamento_azimut) == "None":
			orientamento_azimut = Paragraph("<b>Azimut</b><br/>", styNormal)
		else:
			orientamento_azimut_conv = self.PU.conversione_numeri(self.orientamento_azimut)
			orientamento_azimut = Paragraph("<b>Azimut</b><br/>"  + orientamento_azimut_conv + "°", styNormal)
		posizione_cranio = Paragraph("<b>Posizione cranio</b><br/>"  + str(self.posizione_cranio), styNormal)

		#9 row
		posizione_scheletro = Paragraph("<b>Posizione scheletro</b><br/>"  + str(self.posizione_scheletro), styNormal)
		if str(self.lunghezza_scheletro) == "None":
			lunghezza_scheletro = Paragraph("<b>Lunghezza scheletro</b><br/>", styNormal)
		else:
			lunghezza_scheletro_conv = self.PU.conversione_numeri(self.lunghezza_scheletro)
			lunghezza_scheletro = Paragraph("<b>Lunghezza scheletro</b><br/>"  + lunghezza_scheletro_conv +" m", styNormal)
		posizione_arti_superiori = Paragraph("<b>Posizione arti superiori</b><br/>"  + str(self.posizione_arti_superiori), styNormal)
		posizione_arti_inferiori = Paragraph("<b>Posizione arti inferiori</b><br/>"  + str(self.posizione_arti_inferiori), styNormal)

		#10 row
		dati_postdeposizionali = Paragraph("<b>DATI POSTDEPOSIZIONALI<b></b>",styNormal)

		#11 row
		stato_conservazione = Paragraph("<b>Stato di conservazione</b><br/>"  + str(self.stato_di_conservazione), styNormal)
		disturbato = Paragraph("<b>Disturbato</b><br/>"  + str(self.segnacoli), styNormal)
		completo = Paragraph("<b>Completo</b><br/>"  + str(self.canale_libatorio_si_no), styNormal)
		in_connessione = Paragraph("<b></b><br/>"  + str(self.oggetti_rinvenuti_esterno), styNormal)

		#12 row
		caratteristiche_tafonomiche = ''
		caratteristiche_list = eval(self.caratteristiche)
		if len(caratteristiche_list) > 0 :
			for i in caratteristiche_list:
				if caratteristiche_tafonomiche == '':
					caratteristiche_tafonomiche = ("Tipo caratteristica: %s, posizione: %s") % (str(i[0]), str(i[1]))
				else:
					caratteristiche_tafonomiche += ("<br/>Tipo caratteristica: %s, posizione: %s") % (str(i[0]), str(i[1]))

		caratteristiche_tafonomiche_txt = Paragraph("<b>CARATTERISTICHE TAFONOMICHE</b><br/>"  + caratteristiche_tafonomiche, styNormal)


		#13 row
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
		
		#14 row
		corredo = Paragraph("<b>CORREDO</b></b>",styNormal)

		#15 row
		corredo_presente = Paragraph("<b>Presenza</b><br/>" + str(self.corredo_presenza),styDescrizione)
		
		#16 row
		corredo_descrizione = Paragraph("<b>Descrizione</b><br/>" + str(self.corredo_descrizione),styDescrizione)

		#17 row
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

		corredo_tipo_txt = Paragraph("<b>Singoli oggetti di corredo</b><br/>"  + corredo_tipo, styNormal)

		#schema
		cell_schema =  [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
						[intestazione, '01', '02', '03', '04','05', '06', intestazione2, '08', '09'], #0 row  ok
						[sito, '01', '02', '03', '04', sigla_struttura, '06', '07',nr_individuo,nr_scheda], #1 row ok
						[periodizzazione, '01', '02', '03', '04', '07', '06', '07','08', '09'], #2 row ok
						[periodo_iniziale, '01', '02', fase_iniziale, '04', periodo_finale, '06', fase_finale,'08','09'], #3 row ok
						[datazione_estesa, '01', '02', '03', '04', '07', '06', '07','08', '09'], #4 row ok
						[elementi_strutturali, '01', '02', '03', '04', '07', '06', '07','08', '09'], #5 row ok
						[tipo_contenitore_resti, '01', '02', tipo_copertura,'04', segnacoli,'06', canale_libatorio, '08'], #6 row ok
						[dati_deposizionali, '01', '02','03','04', '05','06', '07', '08','09'], #7 row ok
						[rito, '01', '02',orientamento_asse,'04', orientamento_azimut,'06', 'posizione_cranio', '08','09'], #8 row ok
						[posizione_scheletro, '01', lunghezza_scheletro, '03', posizione_arti_superiori,'05','06', posizione_arti_inferiori, '08','09'], #9 row ok
						[dati_postdeposizionali, '01', '02','03','04', '05','06', '07', '08','09'], #10 row ok
						[stato_conservazione, '01', '02', disturbato,'04', completo,'06', in_connessione, '08'], #11 row ok
						[caratteristiche_tafonomiche_txt, '01', '02','03','04', '05','06', '07', '08','09'], #12 row ok
						[descrizione, '01','02', '03', '04', interpretazione, '06', '07', '08', '09'], #13 row ok
						[corredo, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #14 row ok
						[corredo_presente,'01', '02', '03', '04','05', '06', '07', '08', '09'], #15 ow
						[corredo_descrizione,'01', '02', '03', '04','05', '06', '07', '08', '09'], #16 row
						[corredo_tipo_txt,'01', '02', '03', '04','05', '06', '07', '08', '09'] #17 row
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
					('SPAN', (0,2),(9,2)),  #Periodizzazione
	
					#3 row
					('SPAN', (0,3),(2,3)),  #
					('SPAN', (3,3),(4,3)),  #
					('SPAN', (5,3),(6,3)),  #
					('SPAN', (7,3),(9,3)),  #
					
					#4 row
					('SPAN', (0,4),(9,4)),  #datazione estesa
##################################
					#5 row
					('SPAN', (0,5),(9,5)),  #Elementi strutturali

					#6 row
					('SPAN', (0,6),(2,6)),  #
					('SPAN', (3,6),(4,6)),  #
					('SPAN', (5,6),(6,6)),  #
					('SPAN', (7,6),(9,6)),  #

					#7 row
					('SPAN', (0,7),(9,7)),  #

					#8 row
					('SPAN', (0,8),(2,8)),  #
					('SPAN', (3,8),(4,8)),  #
					('SPAN', (5,8),(6,8)),  #
					('SPAN', (7,8),(9,8)),  #

					#6 row
					('SPAN', (0,9),(1,9)),  #
					('SPAN', (2,9),(3,9)),  #
					('SPAN', (4,9),(6,9)),  #
					('SPAN', (7,9),(9,9)),  #

					#10 row
					('SPAN', (0,10),(9,10)),  #

					#8 row
					('SPAN', (0,11),(2,11)),  #
					('SPAN', (3,11),(4,11)),  #
					('SPAN', (5,11),(6,11)),  #
					('SPAN', (7,11),(9,11)),  #

					#9 row
					('SPAN', (0,12),(9,12)),  #

					#10 row
					('SPAN', (0,13),(4,13)),  #
					('SPAN', (5,13),(9,13)),  #

					#11 row
					('SPAN', (0,14),(9,14)),  #

					#12 row
					('SPAN', (0,15),(9,15)),  #

					#13 row
					('SPAN', (0,16),(9,16)),  

					#14 row
					('SPAN', (0,17),(9,17)),  #

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