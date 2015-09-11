f = open('sudokutestset.text', 'r')

index = 1
for i in f:
	filename = "testdata/test%i.text" %index
	a = open(filename, 'w')
	a.write("order 9\t3\n")
	counter = 0
	for j in range(len(i)):
		if i[j] == ".":
			a.write("-1")
			a.write(" ")
		elif i[j].isdigit():
			reduction = int(i[j])-1
			a.write(str(reduction))
			a.write(" ")  			
		counter = counter + 1
		if counter%9 == 0: 
			a.write("\n")
	a.close()
	index = index + 1  