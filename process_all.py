import read_files
from genpdf_half_page import genPdf
import os

if __name__ == "__main__":
	recipes_root = '/Users/shaynes/Documents/Dropbox/Recipes/prd'
	recipes = []
	for root, dirs, files in os.walk(recipes_root):
		for name in files:
			if name.split('.')[1] != 'rmd':
				continue
			
			recipeText = read_files.readInFile(recipes_root + "/" + name)
			recipe = read_files.parseRecipe(recipeText)
			
			recipes.append(recipe)

	genPdf(recipes, 'all.pdf')
	os.system("open all.pdf")