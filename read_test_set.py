import os
f = open('puzzles.txt', 'r')

index = 1
a = [line for line in f]
b = [line for i, line in enumerate(a) if i % 2 == 0]
c = [line for i, line in enumerate(a) if i % 2 == 1]
d = zip(b,c)
#print d

for i  in d:
	print i
	location = i[1][:-1]
	print location
	#a.write(i[1])
	if not os.path.exists(location):
		os.makedirs(location)
	filename = "%s/test%i.text" %(location, index)
	a = open(filename, 'w')
	a.write("order 9\t3\n")
	counter = 0
	for j in range(len(i[0])):
		if(counter == 0 and i[0][j] == " "):
			continue
		a.write(i[0][j])
		#if( i[j] != " ")
		#a.write(" ")  			
		if(i[0][j].isdigit()):
			counter = counter + 1
		if counter%9 == 0 and counter != 0: 
			a.write("\n")
			counter = 0
	
	a.close()
	index = index + 1 

	 