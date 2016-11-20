import sys, getopt, re, os
import genpdf

def getArguments(argv):
	"""Get command line arguments"""
	inputfile = ""
	outputfile = ""

	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print("test.py -i <inputfile> -o <outputfile>")
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			print("test.py -i <inputfile> -o <outputfile>")
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

		if outputfile == "":
			outputfile = inputfile.rstrip("txt") + "pdf"

	return {"in": inputfile, "out":outputfile}

def generatePdf(recipe, outfile):
	c = canvas.Canvas(filename=outfile, pagesize=letter)
	width, height = letter
	c.translate(1.75*inch, 1*inch)
	c.setFont("Helvetica-Bold", 18)
	
	#Draw a grid for testing
	c.setStrokeColor(gray)
	c.grid([0, mbi(5)],[0, mbi(3), mbi(6), mbi(9)])
	
	#Place the title
	c.drawString(mbi(0.15),mbi(2.62),recipe['title'])
	c.drawString(mbi(0.15),mbi(2.62)+mbi(3),recipe['title'])
	c.drawString(mbi(0.15),mbi(2.62)+mbi(6),recipe['title'])
	
	
	#Place the ingredients
	textobject = c.beginText()
	textobject.setFont("Helvetica", 9)
	textobject.setTextOrigin(mbi(0.15),mbi(2.3))
	for ingredient in recipe['ingredients']:
		if ingredient != ' ':
			textobject.textLine(ingredient['thing'])
		else:
			textobject.textLine('')
	c.drawText(textobject)

	#Place the units
	textobject = c.beginText()
	textobject.setFont("Helvetica", 9)
	textobject.setTextOrigin(mbi(1.75), mbi(2.3))
	for ingredient in recipe['ingredients']:
		if ingredient != ' ':
			textobject.textLine(ingredient['m-unit'])
		else:
			textobject.textLine('')
	c.drawText(textobject)
	
	#Place the directions
	textobject = c.beginText()
	textobject.setFont("Helvetica", 9)
	textobject.setTextOrigin(mbi(2.75), mbi(2.3))
	for ingredient in recipe['directions']:
		if ingredient != ' ':
			textobject.textLine(ingredient)
		else:
			textobject.textLine('')
	c.drawText(textobject)
	
	c.save()

def readInFile(filename):
	f = open(filename, 'r')
	fileContents = list(f)
	
	# strip off the new line characters
	for i, string in enumerate(fileContents):
		fileContents[i] = fileContents[i].rstrip('\n')
	
	return fileContents

def parseIngredient(ingredient):
	"""Takes in a ingredient/unit string, returns them as a list"""
	ret = {}
	tre = re.compile(r"([\w, -]*\w) *[\(\[]") #match the thing
	ure = re.compile(r"\[([0-9 ./A-Za-z\(\),]*)\]") #match the customary (U.S.) unit
	mre = re.compile(r"\(([0-9 ./A-Za-z]*)\)")   #match the metric unit
	
	# add the thing to ret
	tMatch = tre.search(ingredient)
	if tMatch:
		ret['thing'] = tMatch.group(1)
	
	# add a customary (U.S.) unit to ret
	uMatch = ure.search(ingredient)
	if uMatch:
		ret['u-unit'] = uMatch.group(1)
	
	# add a metric unit to ret
	mMatch = mre.search(ingredient)
	if mMatch:
		ret['m-unit'] = mMatch.group(1)
		
	return ret
	
def parseRecipe(recipeText):
	"""Turns a recipe list into a recipe dictionary including title, ingredients, directions"""
	recipe = {}
	for i, line in enumerate(recipeText):
		if line == '# Title':
			titleLine = i + 1 
		elif line == '# Ingredients':
			ingredientsStart = i + 1
		elif line == '# Directions':
			directionsLine = i + 1
	
	# Parse ingredients
	ingredients = []
	for i, line in enumerate(recipeText[ingredientsStart:]):
		if line == '##':
			break
		if line != '-':
			x = parseIngredient(recipeText[i + ingredientsStart])
			ingredients.append(x)
		else:
			ingredients.append(' ')

	# Parse directions
	directions = []
	for i, line in enumerate(recipeText[directionsLine:]):
		if line == '##':
			break
		if line == '' or line == '-':
			continue
		directions.append(recipeText[i+directionsLine]) 
	
	recipe['title'] = recipeText[titleLine]
	recipe['ingredients'] = ingredients
	recipe['directions'] = directions

	return recipe

if __name__ == "__main__":
	
	# get input and output files
	# files['in'] contains the input file
	# files['out'] contains the output file
	files = getArguments(sys.argv[1:])
	
	# recipe will be a list containing the contents of the input file
	recipeText = readInFile(files["in"])
	recipe = parseRecipe(recipeText)
	
	genpdf.genPdf(recipe, files["out"])
	os.system("open " + files["out"])
	