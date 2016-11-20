from reportlab.platypus import Paragraph, Frame, BaseDocTemplate, PageTemplate, FrameBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def mbi(x):
	"""Multiply by one inch"""
	return x * inch

def createFrames():
	debug = 0
	frames = []
	#Recipe 1
	frames.append(Frame(mbi(0.5), mbi(5.5), mbi(7.5), mbi(5), showBoundary=1))
	frames.append(Frame(mbi(0.6), mbi(9.75), mbi(7.4), mbi(0.75), showBoundary=debug))
	frames.append(Frame(mbi(0.6), mbi(5.5), mbi(2), mbi(4.25), showBoundary=debug))
	frames.append(Frame(mbi(2.6), mbi(5.5), mbi(1.65), mbi(4.25), showBoundary=debug))
	frames.append(Frame(mbi(4.25), mbi(5.75), mbi(3.65), mbi(4), showBoundary=debug))
	frames.append(Frame(mbi(4.25), mbi(5.5), mbi(3.65), mbi(0.25), bottomPadding=0, topPadding=0, showBoundary=debug))
	
	#Recipe 2
	frames.append(Frame(mbi(0.5), mbi(0.5), mbi(7.5), mbi(5), showBoundary=1))
	frames.append(Frame(mbi(0.6), mbi(4.75), mbi(7.4), mbi(0.75), showBoundary=debug))
	frames.append(Frame(mbi(0.6), mbi(0.5), mbi(2), mbi(4.25), showBoundary=debug))
	frames.append(Frame(mbi(2.6), mbi(0.5), mbi(1.65), mbi(4.25), showBoundary=debug))
	frames.append(Frame(mbi(4.25), mbi(0.75), mbi(3.65), mbi(4), showBoundary=debug))
	frames.append(Frame(mbi(4.25), mbi(0.5), mbi(3.65), mbi(0.25), bottomPadding=0, topPadding=0, showBoundary=debug))
	
	return frames

def addContent(recipes):
	pdfmetrics.registerFont(TTFont('Consolas','Consolas.ttf'))
	
	avenir_path = "/System/Library/Fonts/Avenir.ttc"
	pdfmetrics.registerFont(TTFont("Avenir-Book", avenir_path, subfontIndex=0))
	pdfmetrics.registerFont(TTFont("Avenir-BookOblique", avenir_path, subfontIndex=7))
	pdfmetrics.registerFontFamily("Avenir", normal="Avenir-Book", italic="Avenir-BookOblique")
	
	
	avenirNext_path = "/System/Library/Fonts/Avenir Next.ttc"
	#pdfmetrics.registerFont(TTFont("AvenirNext-Medium", avenirNext_path, subfontIndex=0))
	#pdfmetrics.registerFont(TTFont("AvenirNext-Regular", avenirNext_path, subfontIndex=1))
	#pdfmetrics.registerFont(TTFont("AvenirNext-UltraLight", avenirNext_path, subfontIndex=2))
	pdfmetrics.registerFont(TTFont("AvenirNext-x", avenirNext_path, subfontIndex=2))
	#pdfmetrics.registerFont(TTFont("AvenirNext-Bold", avenirNext_path, subfontIndex=7))
	pdfmetrics.registerFontFamily("AvenirNext")
	
	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='Ingredients', fontName='Consolas', fontSize=12, leading=14))
	styles.add(ParagraphStyle(name='IngredientsSmall', fontName='Consolas', fontSize=11, leading=14))
	styles.add(ParagraphStyle(name='Directions', fontName='Avenir-Book', spaceafter=10, fontSize=13, leading=15))
	styles.add(ParagraphStyle(name='DirectionsSmall', fontName='Avenir-Book', spaceafter=10, fontSize=11, leading=13))
	styles.add(ParagraphStyle(name='Adapted', fontName='Avenir-BookOblique', fontSize=9, leading=9, alignment=2))
	styles.add(ParagraphStyle(name='RecipeTitle', fontName='AvenirNext-x', fontSize=28))
	
	styleDirections = styles['Directions']
	styleDirectionsSmall = styles['DirectionsSmall']
	styleH = styles['RecipeTitle']
	styleAdapted = styles['Adapted']
	styleIngredients = styles['Ingredients']
	styleIngredientsSmall = styles['IngredientsSmall']
	
	
	contentList = []
	for recipe in recipes:
		print("Processing: " + recipe['title'])
		contentList.append(FrameBreak())
		
		#Title
		contentList.append(Paragraph(recipe['title'], styleH))
		contentList.append(FrameBreak())
		
		#Ingredients
		groupEnd = False
		for ingredient in recipe['ingredients']:
			if ingredient == ' ':
				groupEnd = True
				continue
			print(ingredient['thing'])
			output = ingredient['thing']
			styleToUse = styleIngredients
			if recipe['title'] == 'White Bean & Red Lentil Burgers':
				styleToUse = styleIngredientsSmall
			if groupEnd == True:
				output = '<para spacebefore=10>' + output + '</para>'
				groupEnd = False
			contentList.append(Paragraph(output, styleToUse))
		contentList.append(FrameBreak())
		
		#Units
		for ingredient in recipe['ingredients']:
			if ingredient == ' ':
				groupEnd = True
				continue
			output = ingredient['m-unit']
			if output == '':
				output = ingredient['u-unit']
			if groupEnd == True:
				output = '<para spacebefore=10>' + output + '</para>'
				groupEnd = False
			styleToUse = styleIngredients
			if recipe['title'] == 'White Bean & Red Lentil Burgers':
				styleToUse = styleIngredientsSmall
			contentList.append(Paragraph(output, styleToUse))
		contentList.append(FrameBreak())
		
		#Directions
		for line in recipe['directions']:
			output = line
			styleToUse = styleDirections
			if recipe['title'] == 'Lentil Walnut Loaf':
				styleToUse = styleDirectionsSmall
			contentList.append(Paragraph('<para spaceafter=10>' + output + '</para>', styleToUse))
		contentList.append(FrameBreak())
		
		#Adapted
		#contentList.append(Paragraph('', styleAdapted))
		contentList.append(FrameBreak())

	return contentList

def buildDocument(file, frames, content):
	pages = [PageTemplate(id=None, frames=frames)]
	document = BaseDocTemplate(file, pagesize = letter, pageTemplates=pages)
	document.build(content)
	
def genPdf(recipes, file):
	frames = createFrames()
	content = addContent(recipes)
	buildDocument(file, frames, content)