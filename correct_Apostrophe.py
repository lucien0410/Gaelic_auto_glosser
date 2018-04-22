# encoding=utf8
import sys
inp=sys.argv[1]


f=open(inp,'r').readlines()

f=[i.replace("`","'") for i in f]
f=[i.replace("’","'") for i in f]
f=[i.replace("‘","'") for i in f]

with open('mod_'+inp,'w') as ff:
	for i in f:
		ff.write(i)

print ('"mod_{}" is your output!'.format(inp))

