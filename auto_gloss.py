# coding=utf-8 
# python2.7
# auto_glosser
# Yuan-Lu Chen 04/2018

import nltk

from nltk.tokenize import RegexpTokenizer

from collections import Counter 

def flatten(forest):
	''' in:		flatten([[1],[2],[3]])
		out:	 [1, 2, 3]
	'''
	return [leaf for tree in forest for leaf in tree]

def uni(arr):   # delete reduplicates in an array
	return list(set(arr))

#tokenizers
tk_gd=RegexpTokenizer(r'[ +\,\?+\!+\.\*\n|–]', gaps=True)
tk_gl=RegexpTokenizer('[ +\n]', gaps=True)


# replace 'incorrect' glosses with correct glosses using the mapping created by Colleen 
def correct_gloss(labelled_sequences_with_noise):
	temp=open('gloss_dict.txt','r').readlines()
	cor_gloss_dict=[i.split() for i in temp]
	cor_gloss_dict=[(i[0],i[2]) for i in cor_gloss_dict if len(i)==3]
	cor_gloss_dict=dict(cor_gloss_dict)
	labelled_sequences=[]
	for i in labelled_sequences_with_noise:
		word = [k[0] for k in i]
		gloss = [k[1] for k in i]
		correct_gloss=[]
		for gg in gloss:
			if gg in cor_gloss_dict:
				gg=cor_gloss_dict[gg]
			correct_gloss.append(gg)
		labelled_sequences.append(zip(word,correct_gloss))
	return labelled_sequences


def ext_labelled_seq(gd_file, gl_file):
	diff_len=open('diff_len.log.txt','w')
	'''
	gd_file is the Gaelic line file; one sentence per line.
	gl_file is the gloss line file; one sentence per line.
	two file must have the same length
	'''
	gd=open(gd_file,'r').readlines()
	gl=open(gl_file,'r').readlines()
	if len(gd) != len(gl):
		print ('''
{} and {} do not have the same length.
gd_file is the Gaelic line file; one sentence per line.
gl_file is the gloss line file; one sentence per line.
two file must have the same length
		'''.format(gd_file, gl_file))
		return []
	labelled_sequences=[] # [[(gaelic_1,gloss_1),(gaelic_2,gloss_2),...],...]
	'''
	'gloss_dict.txt' is a dictrary that maps incorrect gloss to correct_gloss
	'''
	cor_gloss_dict=open('gloss_dict.txt','r').readlines()
	cor_gloss_dict=[i.split() for i in cor_gloss_dict]
	cor_gloss_dict=[(i[0],i[2]) for i in cor_gloss_dict if len(i)==3]
	cor_gloss_dict=dict(cor_gloss_dict)
	for i in range(0,len(gd)):
		#lower case and tokenize 
		temp_gd=tk_gd.tokenize(gd[i].lower())
		temp_gl=tk_gl.tokenize(gl[i].lower())
		#print gae_1[i]
		if len(temp_gd)==len(temp_gl): # make sure that the tokenizer works for both Gaelic and morpheme-translation
			labelled_sequences.append(zip(temp_gd,temp_gl))
		else: diff_len.write('{}\n{}\n{}\n'.format(i,temp_gd,temp_gl))
	'''
		#Gaelic words 	[[w1,w2, ...], ... [wn,wn+1, ...]] (i.e. symbol sequences)
		#glosses 	[[g1,g2, ...], ... [gn,gn+1, ...]] (i.e tag sequences)
		#symbols: set of symbolics
		#tag_set: set of tags 
	'''
	#remove empty sentences
	labelled_sequences=[i for i in labelled_sequences if len(i)>0]
	return labelled_sequences 	

def sym_sen_tag_sen_symbols_tag_set(labelled_sequences):
	sym_sen=[[i[0] for i in sen] for sen in labelled_sequences]
	tag_sen=[[i[1] for i in sen] for sen in labelled_sequences]
	symbols=uni(flatten(sym_sen))
	tag_set=uni(flatten(tag_sen))
	return sym_sen, tag_sen, symbols, tag_set 

def yield_tagger(tag_set, symbols, labelled_sequences):
	trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set, symbols)
	tagger = trainer.train_supervised(labelled_sequences)
	#reverse labelled_sequences to create a reversed tagger 
	reversed_labelled_seq=[list(reversed(i)) for i in labelled_sequences]
	reversed_tagger=trainer.train_supervised(reversed_labelled_seq)
	return tagger, reversed_tagger


from nltk.tag import brill, brill_trainer

def train_brill_tagger(initial_tagger, train_sents, **kwargs):
  templates = [
    brill.Template(brill.Pos([-1])),
    brill.Template(brill.Pos([1])),
    brill.Template(brill.Pos([-2])),
    brill.Template(brill.Pos([2])),
    brill.Template(brill.Pos([-2, -1])),
    brill.Template(brill.Pos([1, 2])),
    brill.Template(brill.Pos([-3, -2, -1])),
    brill.Template(brill.Pos([1, 2, 3])),
    brill.Template(brill.Pos([-1]), brill.Pos([1])),
    brill.Template(brill.Word([-1])),
    brill.Template(brill.Word([1])),
    brill.Template(brill.Word([-2])),
    brill.Template(brill.Word([2])),
    brill.Template(brill.Word([-2, -1])),
    brill.Template(brill.Word([1, 2])),
    brill.Template(brill.Word([-3, -2, -1])),
    brill.Template(brill.Word([1, 2, 3])),
    brill.Template(brill.Word([-1]), brill.Word([1])),
  ]
  trainer = brill_trainer.BrillTaggerTrainer(initial_tagger, templates, deterministic=True)
  return trainer.train(train_sents, **kwargs)



global gd_glosser


'''
to run derive_tagger(), execfile('hmm_necessary_functions.py') needs to be run first.
'''
def derive_tagger():
	global gd_glosser
	''' 
	use all the avaible trainging data to yield the optimal glosser
	to run derive_tagger(), execfile('hmm_necessary_functions.py') needs to be run first.
	
	!!! 'all.gd.txt', 'all.gloss.txt' are the raw training data.
	They are NOT available in this version for copyright restrictions. 
	Contact Dr. Andrew Carnie for more information (carnieATemailDOTarizonaDOTedu).     
	'''
	gd_file, gl_file= 'all.gd.txt', 'all.gloss.txt' 
	labelled_sequences = ext_labelled_seq(gd_file, gl_file) 
	labelled_sequences=correct_gloss(labelled_sequences) # fix incorrect gloss
	labelled_sequences.append([('mf','MF'),('cp','CP')])
	t0 = nltk.DefaultTagger('unknown')
	t1 = nltk.UnigramTagger(labelled_sequences, backoff=t0)
	t2 = nltk.BigramTagger(labelled_sequences, backoff=t1)
	t3 = nltk.TrigramTagger(labelled_sequences, backoff=t2)
	gd_glosser = train_brill_tagger(t3, labelled_sequences)
	return gd_glosser

import time
import sys

print ('Training the glosser...\n')
#gd_glosser = derive_tagger()

import cPickle as pickle

'''
Instead of training the glosser from scratch, 
I load the previously trained and pickled model. 
'''
glosser_pk= open("glosser_pk",'r') 
gd_glosser=pickle.load(glosser_pk)
#gd_glosser is the auto_glosser


#Now start auto-glossing 

#read input file
infile_name=sys.argv[1]
infile=open(infile_name,'r').readlines()

# gloss_lines_of_FILENAME.txt is the output
glossOnly=open('gloss_lines_of_'+infile_name,'w')

print ('Start glossing ...')
for j,l in enumerate(infile):
	k=infile[j].lower() 
	#use .lower() to convert the string into lower case; I ignore case information in the training data to make the data more generalized. 
	k=tk_gd.tokenize(k)
	k=gd_glosser.tag(k)
	k=[i[1] for i in k]
	k='\t'.join(k)
	glossOnly.write('{}\n'.format(k))

print ('Done! The output file is "{}"!'.format('gloss_lines_of_'+infile_name))

glossOnly.close()
glosser_pk.close()
