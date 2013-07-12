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


class NumberedCanvas_USsheet(canvas.Canvas):
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

class single_Struttura_pdf_sheet:
	#rapporti stratigrafici
	si_lega_a = ''
	uguale_a = ''
	copre = ''
	coperto_da = ''
	riempie = ''
	riempito_da = ''
	taglia = ''
	tagliato_da = ''
	si_appoggia_a = ''
	gli_si_appoggia = ''

	materiali_print = ''
	elementi_strutturali_print = ''
	rapporti_struttura_print = ''
	misure_struttura_print = ''

	def __init__(self, data):
		self.sito = 							data[0]
		self.sigla_struttura = 			data[1]
		self.numero_struttura = 		data[2]
		self.categoria_struttura = 		data[3]
		self.tipologia_struttura = 		data[4]
		self.definizione_struttura = 	data[5]
		self.descrizione = 				data[6]
		self.interpretazione = 			data[7]
		self.periodo_iniziale = 			data[8]
		self.fase_iniziale = 				data[9]
		self.periodo_finale = 				data[10]
		self.fase_finale = 				data[11]
		self.datazione_estesa = 		data[12]
		self.materiali_impiegati = 			data[13]
		self.elementi_strutturali = 			data[14]
		self.rapporti_struttura = 				data[15]
		self.misure_struttura = 				data[16]

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
		intestazione = Paragraph("<b>SCHEDA STRUTTURA<br/>" + str(self.datestrfdate()) + "</b>", styNormal)
		intestazione2 = Paragraph("<b>pyArchInit</b><br/>www.pyarchinit.blogspot.com", styNormal)

		#1 row
		sito = Paragraph("<b>Sito</b><br/>"  + str(self.sito), styNormal)
		sigla_struttura = Paragraph("<b>Sigla struttura</b><br/>"  + str(self.sigla_struttura), styNormal)
		numero_struttura = Paragraph("<b>Nr.</b><br/>"  + str(self.numero_struttura), styNormal)

		#2 row
		categoria = Paragraph("<b>Categoria</b><br/>"  + self.categoria_struttura, styNormal)
		tipologia = Paragraph("<b>Tipologia</b><br/>"  + self.tipologia_struttura, styNormal)
		definizione = Paragraph("<b>Definizione</b><br/>"  + self.definizione_struttura, styNormal)

		#3 row
		descrizione = ''
		try:
			descrizione = Paragraph("<b>Descrizione</b><br/>" + str(self.descrizione), styDescrizione)
		except:
			pass

		interpretazione = ''
		try:
			interpretazione = Paragraph("<b>Interpretazione</b><br/>" + str(self.interpretazione),styDescrizione)
		except:
			pass
		
		#4 row
		periodizzazione = Paragraph("<b>PERIODIZZAZIONE</b>",styNormal)

		#5 row
		iniziale = Paragraph("<b>INIZIALE</b>",styNormal)
		if self.periodo_iniziale == None:
			periodo_iniziale = Paragraph("<b>Periodo</b><br/>",styNormal)
		else:
			periodo_iniziale = Paragraph("<b>Periodo</b><br/>" + self.periodo_iniziale,styNormal)
		if self.fase_iniziale == None:
			fase_iniziale = Paragraph("<b>Fase</b><br/>",styNormal)
		else:
			fase_iniziale = Paragraph("<b>Fase</b><br/>" + self.fase_iniziale,styNormal)

		finale = Paragraph("<b>FINALE</b>",styNormal)

		if self.periodo_finale == None:
			periodo_finale = Paragraph("<b>Periodo</b><br/>",styNormal)
		else:
			periodo_finale = Paragraph("<b>Periodo</b><br/>" + self.periodo_finale,styNormal)
		if self.fase_finale == None:
			fase_finale = Paragraph("<b>Fase</b><br/>",styNormal)
		else:	
			fase_finale = Paragraph("<b>Fase</b><br/>" + self.fase_finale,styNormal)

		#6 row
		datazione_estesa =Paragraph("<b>DATAZIONE ESTESA</b><br/>" + self.datazione_estesa,styNormal)

		#7 row
		materiali_impiegati = ''
		if eval(self.materiali_impiegati) > 0 :
			for i in eval(self.materiali_impiegati):
				if materiali_impiegati == '':
					try:
						materiali_impiegati += ("%s") % (str(i[0]))
					except:
						pass
				else:
					try:
						materiali_impiegati += (", %s") % (str(i[0]))
					except:
						pass

		materiali_impiegati = Paragraph("<b>Materiali impiegati</b><br/>"  + materiali_impiegati, styNormal)

		#8 row
		elementi_strutturali = ''
		if eval(self.elementi_strutturali) > 0 :
			for i in eval(self.elementi_strutturali):
				if elementi_strutturali == '':
					try:
						elementi_strutturali += ("Tipologia elemento: %s, quantita: %s") % (str(i[0]), str(i[1]))
					except:
						pass
				else:
					try:
						elementi_strutturali += ("<br/>Tipologia elemento: %s, quantita: %s") % (str(i[0]), str(i[1])) 
					except:
						pass

		elementi_strutturali = Paragraph("<b>Elementi strutturali</b><br/>"  + elementi_strutturali, styNormal)

		#9 row
		rapporti_struttura = ''
		if eval(self.rapporti_struttura) > 0 :
			for i in eval(self.rapporti_struttura):
				if rapporti_struttura == '':
					try:
						rapporti_struttura += ("Tipo rapporto: %s, sito: %s, sigla: %s, nr.: %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]))
					except:
						pass
				else:
					try:
						rapporti_struttura += ("<br/>Tipo rapporto: %s, sito: %s, sigla: %s, nr.: %s") % (str(i[0]), str(i[1]), str(i[2]), str(i[3]))
					except:
						pass

		rapporti_struttura = Paragraph("<b>Rapporti struttura</b><br/>"  + rapporti_struttura, styNormal)


		#10 row
		misure_struttura = ''
		if eval(self.misure_struttura) > 0:
			for i in eval(self.misure_struttura):
				if misure_struttura == '':
					try:
						misure_struttura += ("<b>Tipo di misura: %s, Unita' di musura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass
				else:
					try:
						misure_struttura += ("<br/><b>Tipo di misura: %s, Unita' di musura: %s, Quantita': %s") % (str(i[0]), str(i[1]), str(i[2]))
					except:
						pass
		misure_struttura = Paragraph("<b>Misurazioni</b><br/>"  + misure_struttura, styNormal)

		#schema
		cell_schema =  [ #00, 01, 02, 03, 04, 05, 06, 07, 08, 09 rows
						[intestazione, '01', '02', '03', '04','05', '06', intestazione2, '08', '09'], #0 row ok
		 				[sito, '01', '02', '03', '04', sigla_struttura, '06', '07', numero_struttura, '09'], #1 row ok
						[categoria, '01', '02','03', tipologia,'05', '06', '07', definizione, '09'], #2 row ok
						[descrizione, '01','02', '03', '04', interpretazione, '06', '07', '08', '09'], #3 row ok
						[periodizzazione, '02', '03', '04', '05', '06', '06', '07', '08', '09'], #4 row
						[iniziale, '01', periodo_iniziale, '03', fase_iniziale, finale, '06',periodo_finale, '08', fase_finale], #5 row
						[datazione_estesa, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #6 row
						[rapporti_struttura, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #7 row
						[materiali_impiegati, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #8 row
						[elementi_strutturali, '01', '02', '03', '04', '05', '06', '07', '08', '09'], #9 row
						[misure_struttura, '01', '02', '03', '04', '05', '06', '07', '08', '09'] #10 row
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
					('SPAN', (8,1),(9,1)),  #dati identificativi

					#2 row
					('SPAN', (0,2),(3,2)),  #Definizione - interpretazone
					('SPAN', (4,2),(7,2)),  #definizione - intepretazione
					('SPAN', (8,2),(9,2)),  #definizione - intepretazione

					#3 row
					('SPAN', (0,3),(4,3)),  #conservazione - consistenza - colore
					('SPAN', (5,3),(9,3)),  #conservazione - consistenza - colore

					#4 row
					('SPAN', (0,4),(9,4)),  #inclusi - campioni - formazione
					
					#5 row
					('SPAN', (0,5),(1,5)),  #iniziale
					('SPAN', (2,5),(3,5)),  #periodo inizlae
					('SPAN', (5,5),(6,5)),  #fase iniziale
					('SPAN', (7,5),(8,5)),  #finale
					('VALIGN',(0,5),(0,5),'TOP'), 
					('VALIGN',(5,5),(5,5),'TOP'), 

					#6 row
					('SPAN', (0,6),(9,6)),  #Attivita - Struttura - Quota min - Quota max
					
					#7 row
					('SPAN', (0,7),(9,7)),  #Attivita - Struttura - Quota min - Quota max
					
					#8 row
					('SPAN', (0,8),(9,8)),  #Attivita - Struttura - Quota min - Quota max
					
					#9 row
					('SPAN', (0,9),(9,9)),  #Attivita - Struttura - Quota min - Quota max

					#10 row
					('SPAN', (0,10),(9,10)),  #Attivita - Struttura - Quota min - Quota max

					('VALIGN',(0,0),(-1,-1),'TOP')

					]

		t=Table(cell_schema, colWidths=50, rowHeights=None,style= table_style)

		return t


class US_index_pdf_sheet:
	si_lega_a = ''
	uguale_a = ''
	copre = ''
	coperto_da = ''
	riempie = ''
	riempito_da = ''
	taglia = ''
	tagliato_da = ''
	si_appoggia_a = ''
	gli_si_appoggia = ''


	def __init__(self, data):
		self.sito = 							data[0]
		self.area = 							data[1]
		self.us   = 							data[2]
		self.d_stratigrafica =					data[3]
		self.rapporti = 						data[17]

	def unzip_rapporti_stratigrafici(self):
		rapporti = eval(self.rapporti)

		rapporti.sort()

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


	def getTable(self):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styNormal.spaceBefore = 20
		styNormal.spaceAfter = 20
		styNormal.alignment = 0 #LEFT
		styNormal.fontSize = 9

		self.unzip_rapporti_stratigrafici()

		area = Paragraph("<b>Area</b><br/>" + str(self.area),styNormal)
		us = Paragraph("<b>US</b><br/>" + str(self.us),styNormal)
		d_stratigrafica = Paragraph("<b>Def. Stratigr.</b><br/>" + str(self.d_stratigrafica),styNormal)
		copre = Paragraph("<b>Copre</b><br/>" + str(self.copre),styNormal)
		coperto_da = Paragraph("<b>Coperto da</b><br/>" + str(self.coperto_da),styNormal)
		taglia = Paragraph("<b>Taglia</b><br/>" + str(self.taglia),styNormal)
		tagliato_da = Paragraph("<b>Tagliato da</b><br/>" + str(self.tagliato_da),styNormal)
		riempie = Paragraph("<b>Riempie</b><br/>" + str(self.riempie),styNormal)
		riempito_da = Paragraph("<b>Riempito da</b><br/>" + str(self.riempito_da),styNormal)
		si_appoggia_a = Paragraph("<b>Si appoggia a</b><br/>" + str(self.si_appoggia_a),styNormal)
		gli_si_appoggia = Paragraph("<b>Gli si appoggia</b><br/>" + str(self.gli_si_appoggia),styNormal)
		uguale_a = Paragraph("<b>Uguale a</b><br/>" + str(self.uguale_a),styNormal)
		si_lega_a = Paragraph("<b>Si lega a</b><br/>" + str(self.si_lega_a),styNormal)

		data = [area,
				us,
				d_stratigrafica,
				copre,
				coperto_da,
				taglia,
				tagliato_da,
				riempie,
				riempito_da,
				si_appoggia_a,
				gli_si_appoggia,
				uguale_a,
				si_lega_a]

		"""
		for i in range(20):
			data.append([area = Paragraph("<b>Area</b><br/>" + str(area),styNormal),
						us = Paragraph("<b>US</b><br/>" + str(us),styNormal),
						copre = Paragraph("<b>Copre</b><br/>" + str(copre),styNormal),
						coperto_da = Paragraph("<b>Coperto da</b><br/>" + str(coperto_da),styNormal),
						taglia = Paragraph("<b>Taglia</b><br/>" + str(taglia),styNormal),
						tagliato_da = Paragraph("<b>Tagliato da</b><br/>" + str(tagliato_da),styNormal),
						riempie = Paragraph("<b>Riempie</b><br/>" + str(riempie),styNormal),
						riempito_da = Paragraph("<b>Riempito da</b><br/>" + str(riempito_da),styNormal),
						si_appoggia_a = Paragraph("<b>Si appoggia a</b><br/>" + str(si_appoggia_a),styNormal),
						gli_si_appoggia = Paragraph("<b>Gli si appoggia</b><br/>" + str(gli_si_appoggi),styNormal),
						uguale_a = Paragraph("<b>Uguale a</b><br/>" + str(uguale_a),styNormal),
						si_lega_a = Paragraph("<b>Si lega a</b><br/>" + str(si_lega_a),styNormal)])
		"""
		#t = Table(data,  colWidths=55.5)

		return data

	def makeStyles(self):
		styles =TableStyle([('GRID',(0,0),(-1,-1),0.0,colors.black),('VALIGN', (0,0), (-1,-1), 'TOP')
		])  #finale

		return styles


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

	def build_Struttura_sheets(self, records):
		elements = []
		for i in range(len(records)):
			single_struttura_sheet = single_Struttura_pdf_sheet(records[i])
			elements.append(single_struttura_sheet.create_sheet())
			elements.append(PageBreak())
		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'scheda_Struttura.pdf')
		f = open(filename, "wb")
		doc = SimpleDocTemplate(f)
		doc.build(elements, canvasmaker=NumberedCanvas_USsheet)
		f.close()

	def build_index_US(self, records, sito):
		styleSheet = getSampleStyleSheet()
		styNormal = styleSheet['Normal']
		styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
		styH1 = styleSheet['Heading2']
		data = self.datestrfdate()
		lst = []
		lst.append(Paragraph("<b>ELENCO UNITA' STRATIGRAFICHE</b><br/><b>Scavo: %s <br/>Data: %s <br/>Ditta esecutrice: adArte snc, Rimini</b>" % (sito, data), styH1))

		table_data = []
		for i in range(len(records)):
			exp_index = US_index_pdf_sheet(records[i])
			table_data.append(exp_index.getTable())

		styles = exp_index.makeStyles()
		table_data_formatted = Table(table_data,  colWidths=60)
		table_data_formatted.setStyle(styles)

		lst.append(table_data_formatted)
		lst.append(Spacer(0,2))

		filename = ('%s%s%s') % (self.PDF_path, os.sep, 'indice_us.pdf')
		f = open(filename, "wb")

		doc = SimpleDocTemplate(f, pagesize=(29*cm, 21*cm), showBoundary=0)
		doc.build(lst, canvasmaker=NumberedCanvas_USindex)

		f.close()
