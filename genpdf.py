from reportlab.platypus import Paragraph, Frame, BaseDocTemplate, PageTemplate, FrameBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def mbi(x):
	"""Multiply by one inch"""
	return x * inch

def createFrames():
	debug = 1
	frames = []
	#Recipe 1
	frames.append(Frame(inch*1.75, inch*9.5, inch*5, inch*.5, showBoundary=debug))
	frames.append(Frame(inch*1.75, inch*7, inch*1.5, inch*2.5, showBoundary=debug))
	frames.append(Frame(inch*3.25, inch*7, inch*1, inch*2.5, showBoundary=debug))
	frames.append(Frame(inch*4.25, inch*7, inch*2.5, inch*2.5, showBoundary=debug))
	
	#Recipe 2
	frames.append(Frame(inch*1.75, inch*6.5, inch*5, inch*.5, showBoundary=debug))
	frames.append(Frame(inch*1.75, inch*4, inch*1.5, inch*2.5, showBoundary=debug))
	frames.append(Frame(inch*3.25, inch*4, inch*1, inch*2.5, showBoundary=debug))
	frames.append(Frame(inch*4.25, inch*4, inch*2.5, inch*2.5, showBoundary=debug))
	
	#Recipe 3
	frames.append(Frame(inch*1.75, inch*3.5, inch*5, inch*.5, showBoundary=debug))
	frames.append(Frame(inch*1.75, inch*1, inch*1.5, inch*2.5, showBoundary=debug))
	frames.append(Frame(inch*3.25, inch*1, inch*1, inch*2.5, showBoundary=debug))
	frames.append(Frame(inch*4.25, inch*1, inch*2.5, inch*2.5, showBoundary=debug))
	
	return frames

def addContent(recipes):
	styles = getSampleStyleSheet()
	styles.add(ParagraphStyle(name='Ingredients', fontName='Courier', fontSize=8, leading=8))
	styles.add(ParagraphStyle(name='Directions', fontName='Helvetica', spaceafter=10, fontSize=8, leading=8))
	#print(styles)
	styleDirections = styles['Directions']
	styleH = styles['Heading1']
	styleIngredients = styles['Ingredients']
	
	
	contentList = []
	for recipe in recipes:
		print("Processing: " + recipe['title'])
		#Title
		contentList.append(Paragraph(recipe['title'], styleH))
		contentList.append(FrameBreak())
		
		#Ingredients
		groupEnd = False
		for ingredient in recipe['ingredients']:
			if ingredient == ' ':
				groupEnd = True
				continue
			
			output = ingredient['thing']
			if groupEnd == True:
				output = '<para spacebefore=10>' + output + '</para>'
				groupEnd = False
			contentList.append(Paragraph(output, styleIngredients))
		contentList.append(FrameBreak())
		
		#Units
		for ingredient in recipe['ingredients']:
			if ingredient == ' ':
				groupEnd = True
				continue
			
			output = ingredient['m-unit']
			if groupEnd == True:
				output = '<para spacebefore=10>' + output + '</para>'
				groupEnd = False
			contentList.append(Paragraph(output, styleIngredients))
		contentList.append(FrameBreak())
		
		#Directions
		for line in recipe['directions']:
			output = line
			contentList.append(Paragraph('<para spaceafter=10>' + output + '</para>', styleDirections))
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