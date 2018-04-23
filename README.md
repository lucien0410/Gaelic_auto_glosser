# Scotish Gaelic auto-glosser
* Yuan-Lu Chen 4/2018. Tucson, Arizona
* cheny@email.arizona.edu
* Compatible with python2 and python3
* assuming utf-8 encoding


## Citation:

Chen, Yuan-Lu, Andrew Carnie, Michael Hammond, Colleen Patton. (2018). Developing An Auto-Glosser for Scottish Gaelic Using a Corpus of Interlinear Glossed. The 10th Celtic Linguistics Conference. Maynooth, Ireland. September 4–5.

@unpublished{gaelic_igt,
title= {Developing An Auto-Glosser for Scottish Gaelic Using a Corpus of Interlinear Glossed Text},
author = {Chen, Yuan-Lu and Carnie, Andrew and Hammond, Michael and Patton, Colleen},
year = {2018},
note= {The 10th Celtic Linguistics Conference},
URL= {url link to talk abstract if any}
}    


## Prerequisite:
	I assumed that *python* and *NLTK* are already installed.  
	
# Usage
## Step 1: Replace incorrect apostrophes with "'"
	In your command line, enter:
		"python correct_Apostrophe.py FILE_NAME"
	For example:
	 	"python correct_Apostrophe.py Demo_Galic.txt"
	This step will yield a new file called "mod_FILE_NAME"; 
	For the current example, we will have "mod_Demo_Gaelic.txt"

## Step 2: Train the glosser and auto-gloss
	In your command line, enter:
		"python auto_gloss.py mod_FILE_NAME"
	For example:
		"python auto_gloss.py mod_Christine_Primrose_Portugal.txt"
	This step will yield a new file called "gloss_lines_of_FILE_NAME"; 
	For the current example, we will have "gloss_lines_of_mod_Christine_Primrose_Portugal.txt"  

## Step 3: Combine the original file and the gloss lines file
	In your command line, enter:
		"python interlinearize.py FILE_NAME gloss_lines_of_FILE_NAME"
	For example:
		"python interlinearize.py mod_Christine_Primrose_Portugal.txt gloss_lines_of_mod_Christine_Primrose_Portugal.txt" 
	This step will yield a new file called "auto_glossed_FILE_NAME"; 
	For the current example, we will have "auto_glossed_mod_Christine_Primrose_Portugal.txt"  

