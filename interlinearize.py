# coding=utf-8 
# python2.7
# Yuan-Lu Chen 04/2018
print ('''
Usage:
python interlinearize.py Gaelic_file Gloss_file
''')

import sys
gd_ori=open(sys.argv[1],'r').readlines()
gloss_ori=open(sys.argv[2],'r').readlines()

out=open('auto_glossed_'+sys.argv[1],'w')
for j,l in enumerate(gd_ori):
	gd=gd_ori[j]
	gd=gd.split()
	gd='\t'.join(gd)
	gloss=gloss_ori[j]
	gloss=gloss.split()
	gloss='\t'.join(gloss)
	out.write('<sen {0}>\n<GD>\t{1}\n<GLOSS>\t{2}\n<EN>\n</sen {0}>\n\n'.format(j,gd,gloss))

out.close()

print ('"auto_glossed_{}" is the auto-glossed output!\n'.format(sys.argv[1]))